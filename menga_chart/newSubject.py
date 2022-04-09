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
        """Dialog taht generates a new Subject
        """
        super().__init__()
        
        # initialize new Subject
        self.subj = grades.Subject()

        # initilize ui
        self.layout = QVBoxLayout()
        self.button_box = QDialogButtonBox(
            QDialogButtonBox.Cancel | QDialogButtonBox.Ok)
        # we can actually recycle the grade editor tab to make it possible to add new grades to the subject before actually adding it, wich i think is really cool
        self.subject_editor = gradeEditor.gradeEditorTab(self.subj)

        # set up the button box
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

        # compose the ui
        self.layout.addWidget(self.subject_editor)
        self.layout.addWidget(self.button_box)

        # remove the RemoveSubject button from the subjecteditor in the dialog to avoid any embarassing bugs
        self.subject_editor.removeSubjectButton.setParent(None)

        self.setWindowTitle("new Subject")
        self.setLayout(self.layout)

    @staticmethod
    def getSubject():
        """conveniency method that generates a Subject dialog and starts it

        Args:
            subj (Subject): subject to wich the new grade will be added

        Returns:
            any: Subject or None if the user has cancelled the action
        """
        d = newSubjectDialog()
        if d.exec():
            return d.subj
        return None
