from cgitb import enable
from os import system
import time
import random

from datetime import datetime
import numpy as np

class Subject(dict):
    def __init__(self, **kwargs):
        self.enabled = True
        self.chart = None
        self["name"] = ""
        self.color = (255, 0, 0)

        for i in kwargs.keys():
            self[i] == kwargs[i]
            
    @staticmethod
    def getFromDaWeb(User):
        data =  User.request_grades().json()
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
                        "date": item["date"],
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

                grades.append(grade)
        
        # print(grades)
        return grades

    def get_average(self, filtering=True):
        grades = self.get_grades(True)
        weights = self.get_weights(True)
        psum = sum([(grades[z] * weights[z]) for z in range(len(grades))])
        wsum = sum(weights)
        return round(psum / wsum, 2)
 
    def get_averages(self, filtering=True):
        avrg = []
        grades = self.get_grades(True)
        weights = self.get_weights(True)
        for x in range(1, len(grades)+1):
            psum = sum([(grades[:x][z] * weights[:x][z]) for z in range(len(grades[:x]))])
            wsum = sum(weights[:x])
            avrg.append((psum / wsum) if wsum != 0 else 0)
        return avrg
    

    def set_grade_value(self, i, value):
        # print(scope, index, spinbox.value())
        self["grades"][i]["grade"] = value
        # print(self["grades"], value, i)
        self.update()

    def set_weight_value(self, i, value):
        # print(scope, index, spinbox.value())
        self["grades"][i]["weight"] = value
        # print(self["weights"], value, i)
        self.update()
    
    def update(self):
        if self.chart is None:
            raise Exception("chart attribute is not set")
            return

        timestamps = self.get_dates(True)
        unixTimestamps = [time.mktime(datetime.strptime(x, r"%Y-%m-%d").timetuple()) for x in timestamps]
    
        self.chart.plotItems1[self["name"]].setData(unixTimestamps, self.get_grades(True))
        self.chart.plotItems2[self["name"]].setData(unixTimestamps, self.get_averages())
    
    def generate_color(self):
        if self["name"] != "":
            random.seed(self["name"])
            return (random.randint(0,255), random.randint(0,255), random.randint(0,255))
        return (255, 0, 0)
    
    def get_grades(self, filter=True):
        return [i["grade"] for i in self["grades"] if i["mask"] or not filter]

    def get_weights(self, filter=True):
        return [i["weight"] for i in self["grades"] if i["mask"] or not filter]

    def get_dates(self, filter=True):
        return [i["date"] for i in self["grades"] if i["mask"] or not filter]

    def get_masks(self, ):
        return [i["mask"] for i in self["grades"] if i["mask"]]