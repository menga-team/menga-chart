from PyQt5 import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

import requests
import os
import webbrowser

try:
    import __init__ as menga_chart
    import gradeEditor
    import charts
    import aboutDialog
    import loginDialog
    import grades
    import grades
    import utils
except ImportError:
    import menga_chart
    from menga_chart import gradeEditor
    from menga_chart import charts
    from menga_chart import aboutDialog
    from menga_chart import loginDialog
    from menga_chart import grades
    from menga_chart import grades
    from menga_chart import utils


class MenuBar(QMenuBar):
    def __init__(self, window) -> None:
        """holds the menubar. just so u know, this class ids fucking massive. it also handles project saving and expoorting ologic, server communication, etc

        Args:
            window (window): parent window
        """        
        super().__init__()

        # initialize ui
        self.window = window
        self.grades = window.grades
        self.credentials = (True, {})

        # > 
        self.FileMenu = self.addMenu("File")
        # > File >
        self.NewAction = self.FileMenu.addAction("New", self.newProject)
        self.OpenAction = self.FileMenu.addAction("Open", self.openProject)
        self.OpenRecentAction = self.FileMenu.addMenu("Open Recent")
        self.SaveAction = self.FileMenu.addAction("Save", self.saveProject)
        self.SaveAsAction = self.FileMenu.addAction("Save As", self.saveAs)
        self.FileMenu.addSeparator()
        self.refreshChartAction = self.FileMenu.addAction("Refresh Time Chart", self.refreshTimeChart)
        self.refreshAction = self.FileMenu.addAction("Refresh Grade Editor", self.refreshGradeEditor)
        self.FileMenu.addSeparator()
        self.QuitAction = self.FileMenu.addAction("Quit", self.window.app.quit)

        # > 
        self.InsertMenu = self.addMenu("Insert")
        # > Insert >
        self.newSubjectAction = self.InsertMenu.addAction("New Subject", self.window.gradeEditorTab.addSubject)
        self.InsertMenu.addSeparator()
        self.ImportMenu = self.InsertMenu.addMenu("Import")
        # > Insert > Import
        self.jsonImportAction = self.ImportMenu.addAction("From Json File", self.jsonImport)
        self.yamlmportAction = self.ImportMenu.addAction("From Yaml File", self.yamlImport)
        self.configImportAction = self.ImportMenu.addAction("From Config File", self.configImport)
        self.registerImportAction = self.ImportMenu.addAction(
            "From https://www.digitalesregister.it/", self.registerImport)
        self.ExportMenu = self.InsertMenu.addMenu("Export")
        # > Insert > Export
        self.jsonExportAction = self.ExportMenu.addAction("To Json File", self.jsonExport)
        self.yamlExportAction = self.ExportMenu.addAction("To Yaml File", self.yamlExport)
        self.registerExportAction = self.ExportMenu.addAction(
            "To https://www.digitalesregister.it/", self.registerExport)
        # > 
        self.HelpMenu = self.addMenu("Help")
        # > Help >
        self.HelpAction = self.HelpMenu.addAction("Help", lambda: webbrowser.open(menga_chart.url))
        self.IssuesAction = self.HelpMenu.addAction("Issues/Report a Bug", lambda: webbrowser.open(menga_chart.url + "/issues"))
        self.AboutAction = self.HelpMenu.addAction("About the application", aboutDialog.aboutDialog.displayDialog)

        self.updateRecentProjects()

    def confirmDiscard(self):
        """asks the user if he wants to save, discard or cancel the current project if needed

        Returns:
            bool: if the current project may be overwritten or not
        """
        if grades.Subject.edited or grades.Subject.settings.value("paths", list(""))[0]:
            res = QMessageBox.warning(self, "ONG!!", "There are unsaved changes.\nDo you want to save your changes?",
                                      QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel, QMessageBox.Save)
            if res == QMessageBox.Save:
                return self.saveProject()
            elif res == QMessageBox.Cancel:
                return False
            elif res == QMessageBox.Discard:
                return True
        else:
            return True
    
    def addPath(self, path):
        """adds a new apth to the recent projects

        Args:
            path (str): path to the new project
        """
        paths = grades.Subject.settings.value("paths", [])
        if path in paths:
            paths.remove(path)
        paths.insert(0, path)
        grades.Subject.settings.setValue("paths", paths)
        self.updateRecentProjects()
    
    def updateRecentProjects(self):
        """regenerates the recent projects QMenu
        """
        self.OpenRecentAction.clear()
        paths = grades.Subject.settings.value("paths", []).copy()
        for i in range(len(paths)):
            action = self.OpenRecentAction.addAction(paths[i])
            # thank u so fucking much: https://stackoverflow.com/questions/20390323/pyqt-dynamic-generate-qmenu-action-and-connect
            action.triggered.connect(lambda chk, i=i: self.openProject(paths[i]))
        pass
        

    def refreshTimeChart(self):
        """deletes the TimeChart from memory and then regenerates it while preserving the index the user was on at the point of regenerating
        """
        # we have to also delete the Tab widget else we cant destroy the c++ object stored in memory
        i = self.window.tabs.currentIndex()
        self.window.tabs.clear()
        self.window.timeChartTab = charts.TimeChart(
            self.window.grades, self.window)
        self.window.tabs.addTab(self.window.gradeEditorTab, "Grade Editor")
        self.window.tabs.addTab(self.window.timeChartTab, "Time chart")
        self.window.tabs.setCurrentIndex(i)

    def refreshGradeEditor(self):
        """deletes the GradeEditor from memory and then regenerates it while preserving the index the user was on at the point of regenerating
        """
        # we have to also delete the Tab widget else we cant destroy the c++ object stored in memory
        i = self.window.tabs.currentIndex()
        self.window.tabs.clear()
        self.window.gradeEditorTab = gradeEditor.gradeEditor(
            self.window.grades, self.window.timeChartTab)
        self.window.tabs.addTab(self.window.gradeEditorTab, "Grade Editor")
        self.window.tabs.addTab(self.window.timeChartTab, "Time chart")
        self.window.tabs.setCurrentIndex(i)

    def newProject(self):
        """opens a new project
        """
        if self.confirmDiscard():
            self.window.grades = []
            self.window.refreshTabs()
            self.addPath("")
            grades.Subject.edited = False
            self.window.updateStats()

    def saveProject(self, DontSkipDialog=False):
        """saves the current project. Also ahndles the Dialog

        Args:
            DontSkipDialog (bool, optional): currently useless Defaults to False.

        Returns:
            _type_: _description_
        """
        if grades.Subject.settings.value("paths", list(""))[0] == "":
            path = QFileDialog.getSaveFileName(
                self, "Save File", grades.Subject.settings.value("paths", list(""))[0], "JSON (*.json)")[0]
            if path:
                grades.Subject.saveToJson(path, self.window.grades)
                self.addPath(path)
                grades.Subject.edited = False
                self.window.updateStats()
                return True
        return False

    def saveAs(self):
        """also saves the project, but here the file dialog is shown regardless if the project is save dor not
        """
        path = QFileDialog.getSaveFileName(
            self, "Save File", grades.Subject.settings.value("paths", list(""))[0], "JSON (*.json)")[0]
        if path:
            grades.Subject.saveToJson(path, self.window.grades)
            self.addPath(path)
            grades.Subject.edited = False
            self.window.updateStats()

    def openProject(self, path=None):
        """opens a josn file the user can select via the fil dialog as a project

        Args:
            path (_type_, optional): default path in the file dialog. Defaults to None.
        """
        filter = "Json files (*.json);;Text files (*.txt);;All files (*)"
        caption = "select json file to open"
        directory = grades.Subject.settings.value(
            "dialogPath", os.path.expanduser('~'))
        if  self.confirmDiscard() and (path != None or (path := QFileDialog.getOpenFileName(filter=filter, caption=caption, directory=directory)[0])):
            self.window.grades = grades.Subject.readFromJson(path)
            self.addPath(path)
            grades.Subject.edited = False
            self.window.updateStats()
            self.window.refreshTabs()

    def registerImport(self):
        """Imports grades form the digital register website
        """
        # cancel if user does not save the changes
        if not self.confirmDiscard():
            return

        # get credentials
        self.credentials = loginDialog.loginDialog.getCredentials(
            **self.credentials[1])
        # retunrn if empty
        if not self.credentials[0]:
            return

        domain = grades.Subject.settings.value(
            "loginDialogDefaultDomain", defaultValue="")
        URL_API = f'https://{domain}/v2/api'
        URL_LOGIN = f'{URL_API}/auth/login'
        URL_GRADES = f'{URL_API}/student/all_subjects'

        login_payload = dict(
            username=self.credentials[1]["username"], password=self.credentials[1]["password"])

        # request cookies for authentication
        login = utils.Exeption_handler(
            requests.post, silent=True, message="there was an error while trying to log you in", **{"url": URL_LOGIN, "json": login_payload})
        if not login[0]:
            return

        cookies = login[1].cookies
        semester = grades.Subject.settings.value(
            "loginDialogDefaultSemester", defaultValue=0)
        params = [["semesterWechsel", str(1 if semester in [0, 2] else 2)]]

        message = "there was an error with the communication to the server"
        kwargs = {"url": URL_GRADES, "cookies": cookies}
        # request grades data form the server
        reqst = utils.Exeption_handler(
            requests.get, silent=True, message=message, params=params, **kwargs)
        if not reqst[0]:
            return
        data = utils.Exeption_handler(
            reqst[1].json, silent=True, message="there was an error decoding the servers reponse")
        if not data[0]:
            return
        
        if semester == 2:
            # if both semester have bee requested we have to send an addition request for the second semester
            message = "there was an error with the communication to the server"
            kwargs = {"url": URL_GRADES, "cookies": cookies}
            params = [["semesterWechsel", 2]]
            reqst = utils.Exeption_handler(
                requests.get, silent=True, message=message, params=params, **kwargs)
            if not reqst[0]:
                return
            new_data = utils.Exeption_handler(
                reqst[1].json, silent=True, message="there was an error decoding the servers reponse")
            if not new_data[0]:
                return
            # merge both semesters
            for i in data[1]["subjects"]:
                data0 = {x["subjectId"]: x for x in new_data[1]["subjects"]}
                if i["subjectId"] in data0.keys():
                    i["grades"].extend(data0[i["subjectId"]]["grades"])
                else:
                    data[1]["subjects"].append(i)

        grades.Subject.edited = True
        self.window.grades = grades.Subject.getFromRequestResponse(data[1])
        # for i in self.window.grades:
        #     i.chart = self.window.timeChartTab
        #     self.window.timeChartTab.addPlot(i._id)
        #     i.update()
        self.window.refreshTabs()

    def jsonImport(self):
        """handels the Dialog and surrounding logic for the json importing"""
        filter = "Json files (*.json);;Text files (*.txt);;All files (*)"
        caption = "select json file to import"
        directory = grades.Subject.settings.value(
            "dialogPath", os.path.expanduser('~'))
        if self.confirmDiscard() and (path := QFileDialog.getOpenFileName(filter=filter, caption=caption, directory=directory)[0]):
            self.window.grades = grades.Subject.readFromJson(path)
            self.window.refreshTabs()
            grades.Subject.edited = True
            print(path)

    def yamlImport(self):
        """handels the Dialog and surrounding logic for the yaml importing"""
        filter = "Yaml files (*.yaml);;Text files (*.txt);;All files (*)"
        caption = "select yaml file to import"
        directory = grades.Subject.settings.value(
            "dialogPath", os.path.expanduser('~'))
        if (path := self.confirmDiscard()) and (path := QFileDialog.getOpenFileName(filter=filter, caption=caption, directory=directory)[0]):
            self.window.grades = grades.Subject.readFromYaml(path)
            grades.Subject.edited = True
            self.window.refreshTabs()

    def configImport(self):
        """handels the Dialog and surrounding logic for the config importing"""
        filter = "Config files (*.ini);;Text files (*.txt);;All files (*)"
        caption = "select config file to import"
        directory = grades.Subject.settings.value(
            "dialogPath", os.path.expanduser('~'))
        if (path := self.confirmDiscard()) and (path := QFileDialog.getOpenFileName(filter=filter, caption=caption, directory=directory)[0]):
            self.gwindow.grades = grades.Subject.readFromYaml(path)
            grades.Subject.edited = True
            self.window.refreshTabs()

    def jsonExport(self):
        """handels the Dialog and surrounding logic for the json exporting"""
        filter = "Json files (*.json);;Text files (*.txt);;All files (*)"
        caption = "select save location"
        directory = grades.Subject.settings.value(
            "dialogPath", os.path.expanduser('~'))
        if (path := self.confirmDiscard()) and (path := QFileDialog.getSaveFileName(filter=filter, caption=caption, directory=directory)[0]):
            grades.Subject.saveToJson(path, self.grades)

    def yamlExport(self):
        """handels the Dialog and surrounding logic for the yaml exporting"""
        filter = "Yaml files (*.yaml);;Text files (*.txt);;All files (*)"
        caption = "select save location"
        directory = grades.Subject.settings.value(
            "dialogPath", os.path.expanduser('~'))
        if (path := self.confirmDiscard()) and (path := QFileDialog.getSaveFileName(filter=filter, caption=caption, directory=directory)[0]):
            grades.Subject.saveToYaml(path, self.grades)

    def registerExport(self):
        """Ohhohohoho, I wonder what this does"""
        self.credentials = loginDialog.loginDialog.getCredentials(
            **self.credentials[1])
        if not self.credentials[0]:
            return
        domain = grades.Subject.settings.value(
            "loginDialogDefaultDomain", defaultValue="")
        res = QMessageBox.warning(self, "Watch out!",
                                  "You are about to exoprt the \n" +
                                  f"current grade configuration to {domain}\n" +
                                  ".\nANY EXISTING GRADES ON THE PLATFORM WILL BE OVERWRITTEN!!!",
                                  QMessageBox.Ok | QMessageBox.Cancel, QMessageBox.Ok)
        if res == QMessageBox.Ok:
            # oh hullo. good to see u here. prolly means u found this little easter egg.
            # i was planning to stream it from a sevrer directly to the desktop application usiong a QvideoWidget...
            # ... but in the end i just couldnt be bothered.
            webbrowser.open("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
