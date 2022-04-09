from PyQt5 import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

try:
    import charts
    import grades
    import gradeEditor
    import menuBar
except ImportError:
    from menga_chart import charts
    from menga_chart import grades
    from menga_chart import gradeEditor
    from menga_chart import menuBar


class Window(QMainWindow):
    def __init__(self, app):
        """Its the main window and parent of all Widgets and Dialog in the application.

        Args:
            app (QApp): needed to styart the programm
        """
        super().__init__()
        self.app = app
        # show() initilizes the ui engine and indicates wich Widget or window ist the on that we want to actually render as parent
        self.show()
        # i literally just noticed that it still says "Graaph" on the windowtitle.
        # welp, not fixing it now and shame on anyone who tries to do it
        self.setWindowTitle('Graaph')

        # move to schreen centre (holy shit i already documented this part?!?!)
        self.resize(800, 800)
        qtRectangle = self.frameGeometry()
        centerPoint = QDesktopWidget().availableGeometry().center()
        qtRectangle.moveCenter(centerPoint)
        self.move(qtRectangle.topLeft())

        # self.grades = grades.Grade.getFromDaWeb(netIntegration.user(json.loads(open(".credentials.json"))))
        self.grades = grades.Subject.readFromQ()

        # for i in self.grades:
        #     print(json.dumps(i, indent=2))

        # initilize tabs and ui
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
        
        # initlize and compodse even more ui shit n stuff
        self.statLayout = QHBoxLayout()
        self.pathLabel = QLabel()
        self.averageLabel = QLabel()
        self.changedLabel = QLabel()
        self.statLayout.addWidget(self.pathLabel)
        self.statLayout.addStretch()
        self.statLayout.addWidget(self.averageLabel)
        self.statLayout.addWidget(self.changedLabel)
        self.updateStats()
        
        # connect the chartupdate event in every label
        for i in self.grades:
            i.sig.chartUpdate.connect(self.updateStats)
        
        self.temp = QWidget()
        self.templayout = QVBoxLayout()
        self.templayout.addWidget(self.tabs)
        self.templayout.addLayout(self.statLayout)
        self.temp.setLayout(self.templayout)

        # set the central widget, menubar and finally starts the eventloop of the application by calling exec()
        self.setCentralWidget(self.temp)
        self.setMenuBar(self.menubar)
        app.exec()

        # save the grades to the application settings
        grades.Subject.writeToQ(self.grades)

    def refreshTabs(self):
        """basically reload the entire application ecxcept the menubar and statsbar
        """
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
        """updates the data on the bottom bar.
        """
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
            