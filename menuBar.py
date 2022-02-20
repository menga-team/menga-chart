from PyQt5 import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

class MenuBar(QMenuBar):
    def __init__(self, window) -> None:
        super().__init__()
        
        self.window = window
        
        
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
        self.jsonImportAction = self.ExportMenu.addAction("To Json File")
        self.yamlImportAction = self.ExportMenu.addAction("To Yaml File")
        self.configImportAction = self.ExportMenu.addAction("To Config File")
        self.registerImportAction = self.ExportMenu.addAction("To https://www.digitalesregister.it/")
        
        self.HelpMenu = self.addMenu("Help")
        self.HelpAction =  self.HelpMenu.addAction("Help")
        self.IssuesAction =  self.HelpMenu.addAction("Issues/Report a Bug")
        self.AboutAction =  self.HelpMenu.addAction("About the application")