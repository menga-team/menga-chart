from cgitb import enable
from mimetypes import init
from os import system
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import time
import sys
import random

from datetime import datetime
import numpy as np
import json

class Subject(dict):
    
    settings = QSettings("menga", "grade-chart")
    
    def __init__(self, **kwargs):

        class SubjectEvent(QObject):
            chartUpdate = pyqtSignal()
            colorUpdate = pyqtSignal()
            selfDestruct = pyqtSignal()

        self.chart = None
        self._id = random.randint(-sys.maxsize, sys.maxsize)
        self.deleteLater = False
        self["grades"] = []
        self["name"] = ""
        self["visible"] = True
        self["mode"] = 1
        self["pen"] = {}
        self["pen"]["color"] = self.generate_color()
        self["pen"]["cosmetic"] = True
        self["pen"]["width"] = 2
        self["pen"]["dynamicColor"] = True

        self.sig = SubjectEvent()

        for i in kwargs.keys():
            self[i] = kwargs[i]

    @staticmethod
    def getFromDict(data):
        grades = []
        for i in data:
            grade = Subject()
            grade["name"] = i["subject"]["name"]
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
    def getFromJson(path):
        return Subject.getFromDict(json.load(open(".sample.json")))

    @staticmethod
    def getFromDaWeb(User):
        return Subject.getFromDict(User.request_grades().json())
        
    @staticmethod
    def readFromQ():
        try: return [Subject(**i) for i in json.loads(Subject.settings.value("grades"))]
        except: return []
    
    @staticmethod
    def writeToQ(grades):
        Subject.settings.setValue("grades", json.dumps(grades, indent=2))

    def updatePen(self):
        self.chart.plotItems1[self._id].setPen(**self["pen"])
        self.chart.plotItems1[self._id].setPen(**self["pen"])
        self.sig.colorUpdate.emit()
        self.update()

    def update(self):
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
