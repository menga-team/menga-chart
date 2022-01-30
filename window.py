from PyQt5 import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

import charts
import grades
import netIntegration
import gradeEditor
import json

class Window(QWidget):
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
        self.grades = grades.Subject.getFromJson(".sample.json")

        for i in self.grades:
            print(json.dumps(i, indent=2))
        
        self.menubar = QMenuBar()
        self.actionFile = self.menubar.addMenu("File")
        self.actionOptions = self.menubar.addMenu("Options")
        self.actionHelp = self.menubar.addMenu("Help")
        
        self.fileActions = [
            self.actionFile.addAction("New"),
            self.actionFile.addAction("Open"),
            self.actionFile.addAction("Save"),
            self.actionFile.addSeparator(),
            self.actionFile.addAction("Import"),
            self.actionFile.addAction("Export"),
            self.actionFile.addSeparator(),
            self.actionFile.addAction("Quit"),
        ]
        self.helpActions = [
            self.actionHelp.addAction("Help"),
            self.actionHelp.addAction("Issues/Report a Bug"),
            self.actionHelp.addAction("About the application"),
        ]
        
        self.tabs = QTabWidget()
        self.tabs.setContentsMargins(0, 0, 0, 0)
        self.timeChartTab = charts.TimeChart(self.grades)
        self.gradeEditorTab = gradeEditor.gradeEditor(self.grades, self.timeChartTab)
        self.CSVTab = QWidget()
        # self.tabs.resize(300,200)
        self.tabs.addTab(self.gradeEditorTab,"Grade Editor")
        self.tabs.addTab(self.timeChartTab,"Time chart")
        # self.tabs.addTab(self.CSVTab,"CSV view")
        
        self.layout = QVBoxLayout()
        
        self.layout.addWidget(self.menubar)
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)
        
        # self.raise_()
        app.exec()