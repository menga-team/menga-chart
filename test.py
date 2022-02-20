# -*- coding: utf-8 -*-
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *


class MainWindow(QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.resize(200, 100)

        self.settings = QSettings()

        self.label_display = QLabel(self)
        self.label_display.setGeometry(0, 0, 100, 10)

        try: self.label_display.setText(self.settings.value('context'))
        except: self.label_display.setText('TEST')

        self.editLine = QLineEdit(self)
        self.editLine.setGeometry(0, 20, 100, 20)

        self.button = QPushButton(self)
        self.button.clicked.connect(self.buttonEvent)
        self.button.setGeometry(0, 40, 100, 20)
        self.button.setText('Enter')

    def buttonEvent(self):
        self.settings.setValue('context', self.editLine.text())
        self.label_display.setText(self.settings.value('context'))


if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())