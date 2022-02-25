import utils
import requests
import grades
import os
import loginDialog
import grades

from PyQt5 import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

class MenuBar(QMenuBar):
    def __init__(self, window) -> None:
        super().__init__()
        
        self.window = window
        self.grades = window.grades
        self.credentials = (True, {})
        
        
        self.FileMenu = self.addMenu("File")
        self.NewAction = self.FileMenu.addAction("New")
        self.OpenAction = self.FileMenu.addAction("Open")
        self.SaveAction = self.FileMenu.addAction("Save")
        self.FileMenu.addSeparator()
        self.refreshChartAction = self.FileMenu.addAction("Refresh Time Chart")
        self.refreshAction = self.FileMenu.addAction("Refresh Grade Editor")
        self.FileMenu.addSeparator()
        self.QuitAction = self.FileMenu.addAction("Quit")
        
        self.InsertMenu = self.addMenu("Insert")
        self.newSubjectAction = self.InsertMenu.addAction("New Subject")
        self.newGradeAction = self.InsertMenu.addAction("New Grade")
        self.InsertMenu.addSeparator()
        
        self.ImportMenu = self.InsertMenu.addMenu("Import")
        self.jsonImportAction = self.ImportMenu.addAction("From Json File")
        self.yamlmportAction = self.ImportMenu.addAction("From Yaml File")
        self.configImportAction = self.ImportMenu.addAction("From Config File")
        self.registerImportAction = self.ImportMenu.addAction("From https://www.digitalesregister.it/")
        
        self.ExportMenu = self.InsertMenu.addMenu("Export")
        self.jsonExportAction = self.ExportMenu.addAction("To Json File")
        self.yamlExportAction = self.ExportMenu.addAction("To Yaml File")
        self.registerExportAction = self.ExportMenu.addAction("To https://www.digitalesregister.it/")
        
        self.HelpMenu = self.addMenu("Help")
        self.HelpAction =  self.HelpMenu.addAction("Help")
        self.IssuesAction =  self.HelpMenu.addAction("Issues/Report a Bug")
        self.AboutAction =  self.HelpMenu.addAction("About the application")
        
        self.NewAction.triggered.connect(self.newProject)
        self.registerImportAction.triggered.connect(self.registerImport)
        self.jsonImportAction.triggered.connect(self.jsonImport)
        self.yamlmportAction.triggered.connect(self.yamlImport)
        self.configImportAction.triggered.connect(self.configImport)
        self.jsonExportAction.triggered.connect(self.jsonExport)
        self.yamlExportAction.triggered.connect(self.yamlExport)
    
    def confirmDiscard(self):
        if grades.Subject.edited:
            res =  QMessageBox.warning(self, "My Application", "There are unsaved changes.\nDo you want to save your changes?", 
                                   QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel, QMessageBox.Save)
            if res == QMessageBox.Save:
                self.saveProject()
            elif res == QMessageBox.Cancel:
                return False
        return grades.Subject.settings.value("path", False)
    
    def newProject(self):
        if self.confirmDiscard():
            self.window.grades = []
            self.window.refreshTabs()
            grades.Subject.settings.setValue("path", "")
                
    def saveProject(self):
        if grades.Subject.settings.value("path", "") == "":
            path = QFileDialog.getSaveFileName(self, "Save File", grades.Subject.settings.value("path", ""), "JSON (*.json)")
            grades.Subject.saveToJson(path, self.window.grades)
            grades.Subject.settings.setValue("path", path)
            
    def registerImport(self):
        if not self.confirmDiscard():
            return
        
        self.credentials = loginDialog.loginDialog.getCredentials(**self.credentials[1])
        if not self.credentials[0]:
            return

        domain = grades.Subject.settings.value("loginDialogDefaultDomain", defaultValue="")
        URL_API = f'https://{domain}/v2/api'
        URL_LOGIN = f'{URL_API}/auth/login'
        URL_GRADES = f'{URL_API}/student/all_subjects'
        
        login_payload = dict(username=self.credentials[1]["username"], password=self.credentials[1]["password"])
        
        login = utils.Exeption_handler(requests.post, silent=True, message="there was an error while trying to log you in", **{"url": URL_LOGIN, "json": login_payload})
        if not login[0]:
            return
        
        cookies = login[1].cookies
        semester = grades.Subject.settings.value("loginDialogDefaultSemester", defaultValue=0)
        params = [["semesterWechsel", str(1 if semester in [0, 2] else 2)]]
        
        message="there was an error with the communication to the server"
        kwargs = {"url": URL_GRADES, "cookies": cookies}
        reqst = utils.Exeption_handler(requests.get, silent=True, message=message, params=params, **kwargs)
        if not reqst[0]:
            return
        data = utils.Exeption_handler(reqst[1].json, silent=True, message="there was an error decoding the servers reponse")
        if not data[0]:
            return
        
        if semester == 2:
            message="there was an error with the communication to the server"
            kwargs = {"url": URL_GRADES, "cookies": cookies}
            params = [["semesterWechsel", 2]]
            reqst = utils.Exeption_handler(requests.get, silent=True, message=message, params=params, **kwargs)
            if not reqst[0]:
                return
            new_data = utils.Exeption_handler(reqst[1].json, silent=True, message="there was an error decoding the servers reponse")
            if not new_data[0]:
                return
            
            for i in data[1]["subjects"]:
                data0 = {x["subjectId"]: x for x in new_data[1]["subjects"]}
                if i["subjectId"] in data0.keys():
                    i["grades"].extend(data0[i["subjectId"]]["grades"])
                else:
                    data[1]["subjects"].append(i)

        self.window.grades = grades.Subject.getFromRequestResponse(data[1])
        # for i in self.window.grades:
        #     i.chart = self.window.timeChartTab 
        #     self.window.timeChartTab.addPlot(i._id)
        #     i.update() 
        self.window.refreshTabs()
    
    def jsonImport(self):
        if self.confirmDiscard() or (path := QFileDialog.getOpenFileName(filter="Json files (*.json);;Text files (*.txt);;All files (*)", caption="select json file to import", directory=grades.Subject.settings.value("dialogPath", os.path.expanduser('~')))[0]):
             self.window.grades = grades.Subject.readFromJson(path)
             self.window.refreshTabs()
             
    def yamlImport(self):
        if self.confirmDiscard() or (path := QFileDialog.getOpenFileName(filter="Yaml files (*.yaml);;Text files (*.txt);;All files (*)", caption="select yaml file to import", directory=grades.Subject.settings.value("dialogPath", os.path.expanduser('~')))[0]):
             self.window.grades = grades.Subject.readFromYaml(path)
             self.window.refreshTabs()
             
    def configImport(self):
        if self.confirmDiscard() or (path := QFileDialog.getOpenFileName(filter="Config files (*.ini);;Text files (*.txt);;All files (*)", caption="select config file to import", directory=grades.Subject.settings.value("dialogPath", os.path.expanduser('~')))[0]):
             self.gwindow.grades = grades.Subject.readFromYaml(path)
             self.window.refreshTabs()
    
    def jsonExport(self):
        if self.confirmDiscard() or (path := QFileDialog.getSaveFileName(filter="Json files (*.json);;Text files (*.txt);;All files (*)", caption="select save location", directory=grades.Subject.settings.value("dialogPath", os.path.expanduser('~')))[0]):
             grades.Subject.saveToJson(path, self.grades)
             
    def yamlExport(self):
        if self.confirmDiscard() or (path := QFileDialog.getSaveFileName(filter="Yaml files (*.yaml);;Text files (*.txt);;All files (*)", caption="select save location", directory=grades.Subject.settings.value("dialogPath", os.path.expanduser('~')))[0]):
             grades.Subject.saveToYaml(path, self.grades)