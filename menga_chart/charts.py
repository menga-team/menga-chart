from PyQt5 import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from pyqtgraph.Qt import QtGui

from datetime import datetime
from random import randint
import pyqtgraph as pg


class TimeChart(pg.PlotWidget):
    """widget inheriting from a Plotwidget

    Args:
        pg (PlotWidget): .
    """
    def __init__(self, grades, window):
        super().__init__(axisItems={'bottom': pg.DateAxisItem()})
        self.showGrid(x=True, y=True)
        self.setBackground(QPalette().window().color())
        
        # initialize the floating label that follows the cursor
        self.display_text = pg.TextItem(text='', color=(
            QPalette().windowText().color()), anchor=(1, 1))
        self.display_text.setParentItem(self.plotItem.vb)

        # in the future the label will stick to the grade points when you hoover near them. this is the minimum distance form the points
        self.snap_radius = 5
        
        # we need to acceess the paretn window in the future, so we save it here
        self.window = window
        
        self.grades = grades
        for i in self.grades:
            # save the chart in every grade so we can access it later
            i.chart = self
            # connect a few events
            i.sig.chartUpdate.connect(self.collectGarbage)
            i.sig.chartUpdate.connect(self.update_legend)

        # initilize plotitems dictionary
        self.plotItems1 = {}
        self.plotItems2 = {}

        # execute "onMove" when the cursor moves over the chart
        self.scene().sigMouseMoved.connect(self.onMove)

        # setup the legend up right.
        self.legend = pg.LegendItem((80, 60), offset=(70, 20))
        self.legend.setParentItem(self.graphicsItem())

        for subj in self.grades:
            # initilize all cdurrently present poltpoints.
            self.plotItems1[subj._id] = self.plot(
                (), (), symbol="o", pen=subj["pen"])
            self.plotItems2[subj._id] = self.plot(
                (), (), symbol="+", pen=subj["pen"])

        # update the chart with the new points 
        for subj in self.grades:
            subj.update(False)

    def collectGarbage(self):
        """delete grades that have been marked as redundant
        """
        temp = []
        for i in self.grades:
            if i.deleteLater:
                temp.append(i)
        for i in temp:
            self.grades.remove(i)

    def addPlot(self, id):
        """adds a new subjects grades to the plotitem

        Args:
            id (int): id of the subject
        """
        # pen = (len(self.grades) - self.grades.index(subj) + 1, self.grades.index(subj) + 1)
        pen = randint(0, 100)
        self.plotItems1[id] = self.plot((), (), pen=pen, symbol="o")
        self.plotItems2[id] = self.plot((), (), pen=pen, symbol="+")

    def update_legend(self):
        """update the legend
        """
        # uhm yes we clear it and regenerate it anew. i know its inefficent and stuff, but i just couldnet be bothered at the time
        self.legend.clear()
        # print(json.dumps(self.grades, indent=2))
        # print(len(self.grades))
        for subj in self.grades:
            if subj["visible"]:
                self.legend.addItem(
                    self.plotItems1[subj._id], f"{subj['name']} [{subj.get_average(True)}, {len(subj['grades'])}]")
        # self.update()

    # def update(self):
    #     for subj in self.grades:
    #         timestamps = subj["dates"]
    #         unixTimestamps = [time.mktime(datetime.strptime(x, r"%Y-%m-%d").timetuple()) for x in timestamps]

    #         p1 = self.plot(unixTimestamps, subj["grades"], pen=pen, symbol="o")

    #         p2 = self.plot(unixTimestamps, subj.get_averages(), pen=pen, symbol="+")

    #         self.legend.addItem(p1, f"{subj['name']}, {subj.get_average()}")

    def onMove(self, pos):
        """the mehtod updates the content of the label and moves it near the cursor. in the future it will handle that snapping thingy

        Args:
            pos (QPoint): position the label is set to
        """
        # this is sooooo obsolete. need to rewrite properly sometime soon
        graph_pos = self.plotItem.vb.mapSceneToView(pos)
        self.display_text.setText('x=%s\nY=%s' % (datetime.utcfromtimestamp(
            int(graph_pos.x())).strftime('%Y-%m-%d'), int(graph_pos.y() * 4) / 4))
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

# i just now notidced it. Tho rn im just documenting stuff so for now it stays here even though it doesent do anything
class CSVview:
    pass
