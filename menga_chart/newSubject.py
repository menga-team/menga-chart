from PyQt5 import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

try:
    from menga_chart import gradeEditor
    from menga_chart import grades
except ImportError:
    from menga_chart import gradeEditor
    from menga_chart import grades


class newSubjectDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.subj = grades.Subject()

        self.layout = QVBoxLayout()
        self.button_box = QDialogButtonBox(
            QDialogButtonBox.Cancel | QDialogButtonBox.Ok)
        self.subject_editor = gradeEditor.gradeEditorTab(self.subj)

        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

        self.layout.addWidget(self.subject_editor)
        self.layout.addWidget(self.button_box)

        self.subject_editor.removeSubjectButton.setParent(None)

        self.setWindowTitle("new Subject")
        self.setLayout(self.layout)

    @staticmethod
    def getSubject():
        d = newSubjectDialog()
        if d.exec():
            return d.subj
        return None
