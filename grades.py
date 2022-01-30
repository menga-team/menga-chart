from cgitb import enable
from os import system
import time
import random

from datetime import datetime
import numpy as np
import json

class Subject(dict):
    def __init__(self, **kwargs):
        self.enabled = True
        self.chart = None
        self["name"] = ""
        self.color = (255, 0, 0)
        self.visible = True
        self.view_mode = 1
        self.mode = 1
        self.execute_on_update = []

        for i in kwargs.keys():
            self[i] = kwargs[i]
    
    @staticmethod
    def getFromDict(data):
        grades = []
        for i in data["subjects"]:
            if len(i["grades"]) > 0:
                grade = Subject()
                grade["name"] = i["subject"]["name"]
                # grade["dates"] = []
                grade["grades"] = []
                # grade["weights"] = []
                # grade["averages"] = []
                # grade["mask"] = []
                for item in i["grades"]:
                    grade["grades"].append({
                        "date": int(time.mktime(datetime.strptime(item["date"], r"%Y-%m-%d").timetuple())),
                        "grade": float(item["grade"]),
                        "weight": int(item["weight"]),
                        "mask": True
                    })

                    # grade["dates"].append(item["date"])
                    # grade["grades"].append(float(item["grade"]))
                    # grade["weights"].append(item["weight"])
                    # grade["mask"].append(True)
                
                # for x in range(1, len(grade["grades"])+1):
                #     psum = sum([(grade["grades"][:x][z] * grade["weights"][:x][z]) for z in range(len(grade["grades"][:x]))])
                #     wsum = sum(grade["weights"][:x])
                #     grade["averages"].append(psum / wsum)
                # grade["average"] = round(grade["averages"][len(grade["averages"])-1], 2)
                grade.sort_grades()

                grades.append(grade)
        
        # print(grades)
        return grades

    @staticmethod
    def getFromJson(path):
        return Subject.getFromDict(json.load(open(".sample.json")))

    @staticmethod
    def getFromDaWeb(User):
        return Subject.getFromDict(User.request_grades().json())

    def get_average(self, filtering=True):
        self.sort_grades()
        grades = self.get_grades(True)
        weights = self.get_weights(True)
        psum = sum([(grades[z] * weights[z]) for z in range(len(grades))])
        wsum = sum(weights)
        return round(psum / wsum, 2)
 
    def get_averages(self, filtering=True):
        self.sort_grades()
        avrg = []
        grades = self.get_grades(True)
        weights = self.get_weights(True)
        for x in range(1, len(grades)+1):
            psum = sum([(grades[:x][z] * weights[:x][z]) for z in range(len(grades[:x]))])
            wsum = sum(weights[:x])
            avrg.append((psum / wsum) if wsum != 0 else 0)
        return avrg

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
    
    def update(self): 
        self.chart.update_legend()
        for i in self.execute_on_update:
            i()

        if self.chart is None:
            raise Exception("chart attribute is not set")
            return
        
        if not self.visible:
            self.chart.plotItems1[self["name"]].setData((), ())
            self.chart.plotItems2[self["name"]].setData((), ())
            return
        timestamps = self.get_dates(True)
        # unixTimestamps = [time.mktime(datetime.strptime(x, r"%Y-%m-%d").timetuple()) for x in timestamps]

        if self.mode == 0:
            self.chart.plotItems1[self["name"]].setData(self.get_dates(True), self.get_grades(True))
            self.chart.plotItems2[self["name"]].setData((), ())
        elif self.mode == 1:
            self.chart.plotItems1[self["name"]].setData((), ())
            self.chart.plotItems2[self["name"]].setData(self.get_dates(True), self.get_averages())
        elif self.mode == 2:
            self.chart.plotItems1[self["name"]].setData(self.get_dates(True), self.get_grades(True))
            self.chart.plotItems2[self["name"]].setData(self.get_dates(True), self.get_averages())
        else:
            raise Exception("invalid grade viewmode in chart. eihter 0, 1 or 2")
    
    def generate_color(self):
        if self["name"] != "":
            random.seed(self["name"])
            return (random.randint(0,255), random.randint(0,255), random.randint(0,255))
        return (255, 0, 0)
    
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
        self.visible = False
        self.update()
    
    def sort_grades(self):
        self["grades"].sort(key=lambda x: x["date"])

    