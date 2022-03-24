from email import utils
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import time
import sys
import random
import utils
import yaml
import configparser

from datetime import datetime
import json


class Subject(dict):

    settings = QSettings("menga", "grade-chart")
    edited = False

    def __init__(self, **kwargs):

        for i in kwargs.keys():
            self[i] = kwargs[i]

        class SubjectEvent(QObject):
            chartUpdate = pyqtSignal()
            colorUpdate = pyqtSignal()
            selfDestruct = pyqtSignal()

        self.chart = None
        self._id = random.randint(-sys.maxsize, sys.maxsize)
        self.deleteLater = False
        self.setdefault("grades", [])
        self.setdefault("name", "")
        self.setdefault("visible", True)
        self.setdefault("mode", 1)
        self.setdefault("pen", {})
        self["pen"].setdefault("color", self.generate_color())
        self["pen"].setdefault("cosmetic", True)
        self["pen"].setdefault("width", 2)
        self["pen"].setdefault("dynamicColor", True)

        self.sig = SubjectEvent()

    @staticmethod
    def getFromRequestResponse(data):
        grades = []
        for i in data["subjects"]:
            grade = Subject(name=i["subject"]["name"])
            grade["grades"] = []
            for item in i["grades"]:
                grade["grades"].append({
                    "date": int(time.mktime(datetime.strptime(item["date"], r"%Y-%m-%d").timetuple())),
                    "grade": float(item["grade"]),
                    "weight": int(item["weight"]),
                    "mask": True
                })
            grade.sort_grades()
            grades.append(grade)
        return grades

    @staticmethod
    def readFromYaml(path):
        message = "There was an error reading the json file"
        def func(): return [Subject(**i) for i in yaml.safe_load(open(path))]
        data = utils.Exeption_handler(func, silent=True, message=message)
        if data[0]:
            return data[1]
        else:
            return []

    @staticmethod
    def readFromJson(path):
        message = "There was an error reading the json file"
        def func(): return [Subject(**i) for i in json.load(open(path))]
        data = utils.Exeption_handler(func, silent=True, message=message)
        if data[0]:
            return data[1]
        else:
            return []

    @staticmethod
    def readFromQ():
        message = "There was an error retrieving the application settings"
        def func(): return [Subject(**i)
                            for i in json.loads(Subject.settings.value("grades"))]
        data = utils.Exeption_handler(func, silent=True, message=message)
        if data[0]:
            # return []
            return data[1]
        else:
            return []

    @staticmethod
    def readFromQwithPath(path):
        def action():
            config = configparser.ConfigParser()
            config.readfp(open(path))
            return [Subject(**i) for i in json.loads(config.get("General", "grades", fallback="[]"))]
        message = "There was an error retrieving the application settings"
        data = utils.Exeption_handler(action, silent=True, message=message)
        if data[0]:
            return data[1]
        else:
            return []

    @staticmethod
    def saveToJson(path, grades):
        message = "There was an error saving the json file"
        def func(): return json.dump(grades, open(path, "w"))
        utils.Exeption_handler(func, silent=True, message=message)

    @staticmethod
    def saveToYaml(path, grades):
        message = "There was an error saving the yaml file"
        def func(): return yaml.dump([dict(**i)
                                      for i in grades], open(path, "w"))
        utils.Exeption_handler(func, silent=True, message=message)

    @staticmethod
    def writeToQ(grades):
        message = "There was an error retrieving the application settings"
        def func(): return Subject.settings.setValue(
            "grades", json.dumps(grades, indent=2))
        utils.Exeption_handler(func, silent=True, message=message)

    def updatePen(self):
        self.chart.plotItems1[self._id].setPen(**self["pen"])
        self.chart.plotItems1[self._id].setPen(**self["pen"])
        self.sig.colorUpdate.emit()
        self.update()

    def update(self, changed=True):
        if not Subject.edited:
            Subject.edited = changed

        if self.chart is None:
            return

        self.sig.chartUpdate.emit()

        if self.chart is None:
            raise Exception("chart attribute is not set")
            return

        if not self["visible"]:
            self.chart.plotItems1[self._id].setData((), ())
            self.chart.plotItems2[self._id].setData((), ())
            return
        # unixTimestamps = [time.mktime(datetime.strptime(x, r"%Y-%m-%d").timetuple()) for x in timestamps]

        if self["mode"] == 0:
            self.chart.plotItems1[self._id].setData(
                self.get_dates(True), self.get_grades(True))
            self.chart.plotItems2[self._id].setData((), ())
        elif self["mode"] == 1:
            self.chart.plotItems1[self._id].setData((), ())
            self.chart.plotItems2[self._id].setData(
                self.get_dates(True), self.get_averages())
        elif self["mode"] == 2:
            self.chart.plotItems1[self._id].setData(
                self.get_dates(True), self.get_grades(True))
            self.chart.plotItems2[self._id].setData(
                self.get_dates(True), self.get_averages())
        else:
            raise Exception(
                "invalid grade viewmode in chart. eihter 0, 1 or 2")

    def generate_color(self):
        random.seed(self["name"], 2)

        colors = ["aqua", "aquamarine", "blue", "blueviolet", "brown", "crimson", "cyan", "darkblue", "deeppink", "deepskyblue", "firebrick", "forestgreen", "fuchsia", "gold", "green", "greenyellow", "hotpink", "indigo", "khaki", "lavender",
                  "lightblue", "lightgreen", "lightpink", "lime", "magenta", "navy", "olive", "orange", "orangered", "pink", "purple", "red", "salmon", "sandybrown", "skyblue", "steelblue", "tomato", "turquoise", "violet", "yellow", "yellowgreen"]

        color = colors[random.randint(0, len(colors) - 1)]
        qtcolor = QColor(color)
        return qtcolor.red(), qtcolor.green(), qtcolor.blue(), qtcolor.alpha()

    def get_average(self, filtering=True):
        try:
            self.sort_grades()
            grades = self.get_grades(True)
            weights = self.get_weights(True)
            psum = sum([(grades[z] * weights[z]) for z in range(len(grades))])
            wsum = sum(weights)
            return round(psum / wsum, 2)
        except ZeroDivisionError:
            return 0

    def get_averages(self, filtering=True):
        try:
            self.sort_grades()
            avrg = []
            grades = self.get_grades(True)
            weights = self.get_weights(True)
            for x in range(1, len(grades)+1):
                psum = sum([(grades[:x][z] * weights[:x][z])
                           for z in range(len(grades[:x]))])
                wsum = sum(weights[:x])
                avrg.append((psum / wsum) if wsum != 0 else 0)
            return avrg
        except ZeroDivisionError:
            return []

    def set_grade_value(self, i, value):
        self.sort_grades()
        self["grades"][i]["grade"] = value
        self.update()

    def set_weight_value(self, i, value):
        self.sort_grades()
        self["grades"][i]["weight"] = value
        self.update()

    def set_date_value(self, i, value):
        self.sort_grades()
        self["grades"][i]["date"] = int(value)
        self.update()

    def get_grades(self, filter=True):
        self.sort_grades()
        return [i["grade"] for i in self["grades"] if i["mask"] or not filter]

    def get_weights(self, filter=True):
        self.sort_grades()
        return [i["weight"] for i in self["grades"] if i["mask"] or not filter]

    def get_dates(self, filter=True):
        self.sort_grades()
        return [i["date"] for i in self["grades"] if i["mask"] or not filter]

    def get_masks(self, ):
        self.sort_grades()
        return [i["mask"] for i in self["grades"] if i["mask"]]

    def self_destruct(self):
        self["visible"] = False
        self.deleteLater = True
        self.sig.selfDestruct.emit()
        self.update()

    def sort_grades(self):
        self["grades"].sort(key=lambda x: x["date"])
    
    @staticmethod
    def getAverage(grades, SubjectMode=True):
        if grades == []:
            return 0
        if SubjectMode:
            p = []
            for i in [i.get_average() for i in grades]:
                if i != 0:
                    p.append(i)
            if len(p) < 1:
                return 0
            return round(sum(p) / len(p), 2)
        else:
            subj = Subject()
            for i in grades:
                subj["grades"].extend(i["grades"])
            return subj.get_average()
