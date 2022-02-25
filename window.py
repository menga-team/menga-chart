from PyQt5 import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

import charts
import grades
import gradeEditor
import json
import menuBar

class Window(QMainWindow):
    def __init__(self, app):
        super().__init__()
        self.show()
        self.setWindowTitle('Graaph')

        # move to schreen centre
        self.resize(800, 800)
        qtRectangle = self.frameGeometry()
        centerPoint = QDesktopWidget().availableGeometry().center()
        qtRectangle.moveCenter(centerPoint)
        self.move(qtRectangle.topLeft())

        # self.grades = grades.Grade.getFromDaWeb(netIntegration.user(json.loads(open(".credentials.json"))))
        self.grades = grades.Subject.readFromQ()

        # for i in self.grades:
        #     print(json.dumps(i, indent=2))
        
        self.menubar = menuBar.MenuBar(self)
        
        
        self.tabs = QTabWidget()
        self.tabs.setContentsMargins(0, 0, 0, 0)
        self.timeChartTab = charts.TimeChart(self.grades)
        self.gradeEditorTab = gradeEditor.gradeEditor(self.grades, self.timeChartTab)
        self.CSVTab = QWidget()
        # self.tabs.resize(300,200)
        self.tabs.addTab(self.gradeEditorTab,"Grade Editor")
        self.tabs.addTab(self.timeChartTab,"Time chart")
        # self.tabs.addTab(self.CSVTab,"CSV view")
        
        self.setCentralWidget(self.tabs)
        self.setMenuBar(self.menubar)
        app.exec()
        
        grades.Subject.writeToQ(self.grades)
        
        
    def refreshTabs(self):
        self.tabs.clear()
        self.timeChartTab = charts.TimeChart(self.grades)
        self.gradeEditorTab = gradeEditor.gradeEditor(self.grades, self.timeChartTab)
        # self.tabs.resize(300,200)
        self.tabs.addTab(self.gradeEditorTab,"Grade Editor")
        self.tabs.addTab(self.timeChartTab,"Time chart")
        # self.tabs.addTab(self.CSVTab,"CSV view")