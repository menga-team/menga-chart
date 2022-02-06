from random import randint
import time
from datetime import datetime, timedelta

import numpy as np
import math
import pyqtgraph as pg
from PyQt5 import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from pyqtgraph.Qt import QtGui

class TimeChart(pg.PlotWidget):
    def __init__(self, grades):
        super().__init__(axisItems = {'bottom': pg.DateAxisItem()})
        self.showGrid(x=True, y=True)
        self.setBackground(QPalette().window().color())
        self.display_text= pg.TextItem(text='',color=(QPalette().windowText().color()),anchor=(1,1))
        self.display_text.setParentItem(self.plotItem.vb)
        
        self.snap_radius = 5
        
        self.grades = grades
        for i in self.grades:
            i.chart = self

        self.plotItems1 = {}
        self.plotItems2 = {}
        
        self.scene().sigMouseMoved.connect(self.onMove)

        self.legend = pg.LegendItem((80,60), offset=(70,20))
        self.legend.setParentItem(self.graphicsItem())
        

        for subj in self.grades:
            pen = (len(self.grades) - self.grades.index(subj) + 1, self.grades.index(subj) + 1)

            self.plotItems1[subj["name"]] = self.plot((), (), pen=pen, symbol="o")
            self.plotItems2[subj["name"]] = self.plot((), (), pen=pen, symbol="+")

        for subj in self.grades:
            subj.update()
    
    def addPlot(self, name):
        # pen = (len(self.grades) - self.grades.index(subj) + 1, self.grades.index(subj) + 1)
        pen = randint(0, 100)
        self.plotItems1[name] = self.plot((), (), pen=pen, symbol="o")
        self.plotItems2[name] = self.plot((), (), pen=pen, symbol="+")

    def update_legend(self):
        self.legend.clear()
        for subj in self.grades:
            if subj.visible:
                self.legend.addItem(self.plotItems1[subj["name"]], f"{subj['name']} [{subj.get_average(True)}, {len(subj['grades'])}]")
        # self.update()

    # def update(self):
    #     for subj in self.grades:
    #         timestamps = subj["dates"]
    #         unixTimestamps = [time.mktime(datetime.strptime(x, r"%Y-%m-%d").timetuple()) for x in timestamps]
        
    #         p1 = self.plot(unixTimestamps, subj["grades"], pen=pen, symbol="o")
        
    #         p2 = self.plot(unixTimestamps, subj.get_averages(), pen=pen, symbol="+")

    #         self.legend.addItem(p1, f"{subj['name']}, {subj.get_average()}")

                
            
    def onMove(self, pos):
        # this is sooooo obsolete. need to rewrite properly sometime soon
        graph_pos = self.plotItem.vb.mapSceneToView(pos)
        self.display_text.setText('x=%s\nY=%s'%(datetime.utcfromtimestamp(int(graph_pos.x())).strftime('%Y-%m-%d'),int(graph_pos.y() * 4) / 4))
        self.display_text.setPos(pos)
        
        # can't get snapping to work so im just gonna leave this here for a future me
        # log made a commit later: seems to have an issue with translating point from the graph back to pyqt cooordinates
        # wich is curios since the inverse conversion works just fine
        # 
        # self.setToolTip('x=%f\nY=%f'%(graph_pos.x(),graph_pos.y()))
        # if len(p1)!=0:
        # sanpped = False
        # # print(list(zip(self.x_data, self.y_data)))
        # for x_val, y_val in zip(self.x_data, self.y_data):
        #     # print(list((zip(x_val, y_val))))
        #     # print(x_val, y_val)
        #     # print(list(zip(x_val, y_val)))
        #     for x, y in zip(x_val, y_val):
        #         point_pos = self.plotItem.vb.mapFromView(QPoint(x, y)) 
        #         # point_pos = self.plotItem.vb.mapViewToDevice(QPoint(x, y)) 
        #         # point_pos = self.plotItem.vb.mapViewToScene(QPoint(x, y)) 
                
        #         # print(pos.x()- point_pos.x(), pos.y() - point_pos.y())
        #         if -21 < (pos.x() - point_pos.x()) < 21 and -21 < (pos.y() - point_pos.y()) < 21:
        #             print(point_pos.x(), point_pos.y())
                    
        #             self.display_text.setPos(QPoint(point_pos.x(), point_pos.y()))
        #             self.display_text.setText('x=%s\nY=%s'%(datetime.utcfromtimestamp(int(x)).strftime('%Y-%m-%d'),int(y * 4) / 4))
        
        #             sanpped = True
                    # break
            # if sanpped:
            #     break
                
            
        # else:
        #     self.toolTip.hideText()
        #     # display_text.hide()
        

class CSVview:
    pass