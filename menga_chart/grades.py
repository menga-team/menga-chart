from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from datetime import datetime
import time
import sys
import random
import yaml
import configparser
import json

try:
    import utils
except ImportError:
    from menga_chart import utils


class Subject(dict):
    # theese setting are actually global, but i just put them here to trigger myself once i write the documentation about it. Fuck you, past me.
    settings = QSettings("menga", "grade-chart")
    edited = False

    def __init__(self, **kwargs):
        """arguably the core or at least the datacenter of the entire application. it represents a Subject and contains all the according logic, data, garde, events, cheese etc...
        """

        for i in kwargs.keys():
            self[i] = kwargs[i]

        class SubjectEvent(QObject):
            """yes ik its awful but since i can only decalre a pyqtSignal inside a QObject and dictioanry and QObjects are incompatible this is the only way

            Args:
                QObject (QObject): a QOcbject indeed
            """
            chartUpdate = pyqtSignal()
            colorUpdate = pyqtSignal()
            selfDestruct = pyqtSignal()

        # reference to the chart is neeeded for updating the colored lines on it
        self.chart = None
        self._id = random.randint(-sys.maxsize, sys.maxsize)
        # i cant destroy the object from witin, so i just mark it as useless and delete it eventually from ooutside
        self.deleteLater = False
        # declare the defaultvalues of the disctionary. These do not overwrite already present items
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
        """parses a the json in the request returned from the digitasl register servers website

        Args:
            data (dict): raw dictionary from the request

        Returns:
            list: list containing all Subjects
        """
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
        """reads the Subject array from a yaml file at the specified path

        Args:
            path (str): yaml file to open

        Returns:
            list: list containing all Subjects
        """
        message = "There was an error reading the json file"
        def func(): return [Subject(**i) for i in yaml.safe_load(open(path))]
        data = utils.Exeption_handler(func, silent=True, message=message)
        if data[0]:
            return data[1]
        else:
            return []

    @staticmethod
    def readFromJson(path):
        """reads the Subject array from a json file at the specified path

        Args:
            path (str): json file to open

        Returns:
            list: list containing all Subjects
        """
        message = "There was an error reading the json file"
        def func(): return [Subject(**i) for i in json.load(open(path))]
        data = utils.Exeption_handler(func, silent=True, message=message)
        if data[0]:
            return data[1]
        else:
            return []

    @staticmethod
    def readFromQ():
        """reads the Subject array directly from the applications settings

        Returns:
            list: list containing all Subjects
        """
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
        """reads the Subject array from a external config file

        Args:
            path (str): config file to open

        Returns:
            list: list containing all Subjects
        """
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
        """exports the grades to a json file

        Args:
            path (str): path tho the json file save location
            grades (list): list containing the grades we want to save
        """
        message = "There was an error saving the json file"
        def func(): return json.dump(grades, open(path, "w"))
        utils.Exeption_handler(func, silent=True, message=message)

    @staticmethod
    def saveToYaml(path, grades):
        """exports the grades to a yaml file

        Args:
            path (str): path tho the yaml file save location
            grades (list): list containing the grades we want to save
        """
        message = "There was an error saving the yaml file"
        def func(): return yaml.dump([dict(**i)
                                      for i in grades], open(path, "w"))
        utils.Exeption_handler(func, silent=True, message=message)

    @staticmethod
    def writeToQ(grades):
        """saves the grades to the application settings

        Args:
            grades (list): list containing the grades we want to save
        """
        message = "There was an error retrieving the application settings"
        def func(): return Subject.settings.setValue(
            "grades", json.dumps(grades, indent=2))
        utils.Exeption_handler(func, silent=True, message=message)

    def updatePen(self):
        """to execute when we want to update the plotlines pen
        """
        self.chart.plotItems1[self._id].setPen(**self["pen"])
        self.chart.plotItems1[self._id].setPen(**self["pen"])
        self.sig.colorUpdate.emit()
        self.update()

    def update(self, changed=True):
        """to execute when we modified the Subjects data and need to update the ui accordingly

        Args:
            changed (bool, optional): True if the data has been modified else false. If True will modifiy the saved status of the project. Defaults to True.

        Raises:
            Exception: "chart attribute is not set" for some obscure reason the chart reference is null
            Exception: "invalid grade viewmode in chart. eihter 0, 1 or 2" for some obscure reason the viewmode reference is not 0, 1 or 2
        """
        # set the global edited attribute to changed if it isnt already True
        if not Subject.edited:
            Subject.edited = changed

        # yes i know, why am i returning None when self.chart is None when i appositly declared an exception for it in the next lines? i don't know. i just here to document stuff not shoot myself in the foot
        if self.chart is None:
            return
        
        self.sig.chartUpdate.emit()

        # yes i am raising an exception and then immediatly returnning for no reason since the exception raising has already halted the programm and im proud of it
        if self.chart is None:
            raise Exception("chart attribute is not set")
            return

        # If the Subject is iinvisible clear the plotline to also make them invisible 
        if not self["visible"]:
            self.chart.plotItems1[self._id].setData((), ())
            self.chart.plotItems2[self._id].setData((), ())
            return
        # unixTimestamps = [time.mktime(datetime.strptime(x, r"%Y-%m-%d").timetuple()) for x in timestamps]

        # self["mode"] controlls if the avergae, the absolute grades or both are shown 
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
        """generates a Qcolor for the pen

        Returns:
            QColor: generated QColor
        """
        # take as random seed the subjects name so Subjects with the same name always ave the same color
        random.seed(self["name"], 2)

        # list of colors that are morally acceptable to be displayed on a probably either black or white background
        colors = ["aqua", "aquamarine", "blue", "blueviolet", "brown", "crimson", "cyan", "darkblue", "deeppink", "deepskyblue", "firebrick", "forestgreen", "fuchsia", "gold", "green", "greenyellow", "hotpink", "indigo", "khaki", "lavender",
                  "lightblue", "lightgreen", "lightpink", "lime", "magenta", "navy", "olive", "orange", "orangered", "pink", "purple", "red", "salmon", "sandybrown", "skyblue", "steelblue", "tomato", "turquoise", "violet", "yellow", "yellowgreen"]

        color = colors[random.randint(0, len(colors) - 1)]
        qtcolor = QColor(color)
        return qtcolor.red(), qtcolor.green(), qtcolor.blue(), qtcolor.alpha()

    def get_average(self, filtering=True):
        """returns the avergae of all grades in the Subject. returns Zero if there are not enough grades

        Args:
            filtering (bool, optional): If True only includes grades that are visible. Defaults to True.

        Returns:
            float: global avergae of the grade
        """
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
        """returns a list of every snapshot of the Subjects averrgae after each grade has been added

        Args:
            filtering (bool, optional): If true only includes grades that are visible. Defaults to True.

        Returns:
            list: list of avergaes in chronological order
        """
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
        """sets the grade value of a specific grade, sorts them chronologically and updates the Subject.

        Args:
            i (int): index of said grade
            value (float): value to be set
        """
        self.sort_grades()
        self["grades"][i]["grade"] = value
        self.update()

    def set_weight_value(self, i, value):
        """sets the wheught of a specific grade, sorts them chronologically and updates the Subject.

        Args:
            i (int): index of said grade
            value (float): value to be set
        """
        self.sort_grades()
        self["grades"][i]["weight"] = value
        self.update()

    def set_date_value(self, i, value):
        """sets the date of a specific grade, sorts them chronologically and updates the Subject.

        Args:
            i (int): index of said grade
            value (float): date in unix epoch to be set
        """
        self.sort_grades()
        self["grades"][i]["date"] = int(value)
        self.update()

    def get_grades(self, filter=True):
        """sorts all gardes in chronological order and returns a list of grade value

        Args:
            filter (bool, optional): If True only includes visible grades. Defaults to True.

        Returns:
            list: list containing the grade values in chronological order
        """
        self.sort_grades()
        return [i["grade"] for i in self["grades"] if i["mask"] or not filter]

    def get_weights(self, filter=True):
        """sorts all gardes in chronological order and returns a list of the weights

        Args:
            filter (bool, optional): If True only includes visible grades. Defaults to True.

        Returns:
            list: list containing the weights in chronological order
        """
        self.sort_grades()
        return [i["weight"] for i in self["grades"] if i["mask"] or not filter]

    def get_dates(self, filter=True):
        """sorts all gardes in chronological order and returns a list of the dates

        Args:
            filter (bool, optional): If True only includes visible grades. Defaults to True.

        Returns:
            list: list containing the dates in chronological order
        """
        self.sort_grades()
        return [i["date"] for i in self["grades"] if i["mask"] or not filter]

    def get_masks(self, ):
        """sorts all gardes in chronological order and returns a list of the masks (visibility)

        Args:
            filter (bool, optional): If True only includes visible grades. Defaults to True.

        Returns:
            list: list containing the masks (visibility) in chronological order
        """
        self.sort_grades()
        return [i["mask"] for i in self["grades"] if i["mask"]]

    def self_destruct(self):
        """execute this if you want to delete the Subject
        """
        self["visible"] = False
        self.deleteLater = True
        self.sig.selfDestruct.emit()
        self.update()

    def sort_grades(self):
        """sorts the grades in chronological order"""
        self["grades"].sort(key=lambda x: x["date"])
    
    @staticmethod
    def getAverage(grades, SubjectMode=True):
        """calculates the average of all avergaes or ALL and i mean ALL grades

        Args:
            grades (list): list containing all Subjects we want to process
            SubjectMode (bool, optional): If True calculates the avergae of all Subjects averages, else packs all individual grades toghether and calculates a average form that. (there is a diffrence trust me). Defaults to True.

        Returns:
            _type_: _description_
        """
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
