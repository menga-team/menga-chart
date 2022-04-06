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
        self.app = app
        self.show()
        # i literally just noticed that it still says "Graaph" on the windowtitle.
        # welp, not fixing it now and shame on anyone who tries to do it
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

        self.tabs = QTabWidget()
        self.tabs.setContentsMargins(0, 0, 0, 0)
        self.timeChartTab = charts.TimeChart(self.grades, self)
        self.gradeEditorTab = gradeEditor.gradeEditor(
            self.grades, self.timeChartTab)
        self.CSVTab = QWidget()
        # self.tabs.resize(300,200)
        self.tabs.addTab(self.gradeEditorTab, "Grade Editor")
        self.tabs.addTab(self.timeChartTab, "Time chart")
        # self.tabs.addTab(self.CSVTab,"CSV view"
        
        self.menubar = menuBar.MenuBar(self)
        
        self.statLayout = QHBoxLayout()
        self.pathLabel = QLabel()
        self.averageLabel = QLabel()
        self.changedLabel = QLabel()
        self.statLayout.addWidget(self.pathLabel)
        self.statLayout.addStretch()
        self.statLayout.addWidget(self.averageLabel)
        self.statLayout.addWidget(self.changedLabel)
        self.updateStats()
        
        for i in self.grades:
            i.sig.chartUpdate.connect(self.updateStats)
        
        self.temp = QWidget()
        self.templayout = QVBoxLayout()
        self.templayout.addWidget(self.tabs)
        self.templayout.addLayout(self.statLayout)
        self.temp.setLayout(self.templayout)

        self.setCentralWidget(self.temp)
        self.setMenuBar(self.menubar)
        app.exec()

        grades.Subject.writeToQ(self.grades)

    def refreshTabs(self):
        i = self.tabs.currentIndex()
        self.tabs.clear()
        self.timeChartTab = charts.TimeChart(self.grades, self)
        self.gradeEditorTab = gradeEditor.gradeEditor(
            self.grades, self.timeChartTab)
        # self.tabs.resize(300,200)
        self.tabs.addTab(self.gradeEditorTab, "Grade Editor")
        self.tabs.addTab(self.timeChartTab, "Time chart")
        # self.tabs.addTab(self.CSVTab,"CSV view")
        self.tabs.setCurrentIndex(i)

    def updateStats(self):
        path = grades.Subject.settings.value("paths", ["New Project"])[0]
        if path == "":
            path = "New Project"
        self.pathLabel.setText(path)
        self.averageLabel.setText(str(grades.Subject.getAverage(self.grades)))
        
        p = QPalette()
        if grades.Subject.edited:
            self.changedLabel.setText("UNSAVED")
            p.setColor(QPalette.WindowText, Qt.red)
        else: 
            self.changedLabel.setText("SAVED")
            p.setColor(QPalette.WindowText, Qt.green)
        self.changedLabel.setPalette(p)
            