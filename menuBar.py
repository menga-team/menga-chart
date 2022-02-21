import grades
import os

from PyQt5 import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

class MenuBar(QMenuBar):
    def __init__(self, window) -> None:
        super().__init__()
        
        self.window = window
        self.grades = window.grades
        self.dir = grades.Subject.settings.value("dialogPath", defaultValue=os.path.expanduser('~'))
        
        
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
        
        self.jsonImportAction.triggered.connect(self.jsonImport)
        self.yamlmportAction.triggered.connect(self.yamlImport)
        self.configImportAction.triggered.connect(self.configImport)
        self.jsonExportAction.triggered.connect(self.jsonExport)
        self.yamlExportAction.triggered.connect(self.yamlExport)
    
    def jsonImport(self):
        if path := QFileDialog.getOpenFileName(filter="Json files (*.json);;Text files (*.txt);;All files (*)", caption="select json file to import", directory=self.dir)[0]:
             self.window.grades = grades.Subject.readFromJson(path)
             self.window.refreshTabs()
             self.dir = path
             
    def yamlImport(self):
        if path := QFileDialog.getOpenFileName(filter="Yaml files (*.yaml);;Text files (*.txt);;All files (*)", caption="select yaml file to import", directory=self.dir)[0]:
             self.window.grades = grades.Subject.readFromYaml(path)
             self.window.refreshTabs()
             self.dir = path
             
    def configImport(self):
        if path := QFileDialog.getOpenFileName(filter="Config files (*.ini);;Text files (*.txt);;All files (*)", caption="select config file to import", directory=self.dir)[0]:
             self.gwindow.grades = grades.Subject.readFromYaml(path)
             self.window.refreshTabs()
             self.dir = path
    
    def jsonExport(self):
        if path := QFileDialog.getSaveFileName(filter="Json files (*.json);;Text files (*.txt);;All files (*)", caption="select save location", directory=self.dir)[0]:
             grades.Subject.saveToJson(path, self.grades)
             self.dir = path
             
    def yamlExport(self):
        if path := QFileDialog.getSaveFileName(filter="Yaml files (*.yaml);;Text files (*.txt);;All files (*)", caption="select save location", directory=self.dir)[0]:
             grades.Subject.saveToYaml(path, self.grades)
             self.dir = path