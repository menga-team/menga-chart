from PyQt5 import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from qtwidgets import AnimatedToggle


class newGradeDialog(QDialog):
    def __init__(self, subj):
        """Dialog to add new Grades

        Args:
            subj (Subject): subject to wich we are adding the new grade
        """
        super().__init__()

        # initialize the ui
        self.layout = QGridLayout()
        self.toggle = AnimatedToggle()
        self.grade_spin = QDoubleSpinBox()
        self.weight_spin = QSpinBox()
        self.date_editor = QDateEdit()
        self.button_box = QDialogButtonBox(
            QDialogButtonBox.Cancel | QDialogButtonBox.Ok)
        self.grade = {}
        self.subj = subj

        #setup the visibility toggle
        self.toggle.setChecked(True)
        # self.toggle.stateChanged.connect(self.toggle_clicked)
        self.toggle.setMaximumWidth(70)

        # setup the grade spinner
        self.grade_spin.setSingleStep(0.5)
        self.grade_spin.setMaximum(10.25)
        self.grade_spin.setMinimum(-0.25)
        self.grade_spin.setValue(7.5)
        # self.grade_spin.valueChanged.connect(self.grade_spin_edited)
        
        # setup the weight spinner
        self.weight_spin.setSingleStep(5)
        self.weight_spin.setMaximum(100)
        self.weight_spin.setMinimum(-0)
        self.weight_spin.setValue(100)
        # self.weight_spin.valueChanged.connect(self.weight_spin)
        
        # setup the date editor
        self.date_editor.setDisplayFormat("dd/MM/yyyy")
        self.date_editor.setDate(QDate.currentDate())
        # self.date_editor.dateChanged.connect(self.date_edited)
        self.date_editor.setCalendarPopup(True)

        # setup the button box
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

        # compose the ui
        self.layout.addWidget(QLabel("visible:"), 0, 0)
        self.layout.addWidget(self.toggle, 0, 1)
        self.layout.addWidget(QLabel("set grade:"), 1, 0)
        self.layout.addWidget(self.grade_spin, 1, 1)
        self.layout.addWidget(QLabel("set weight:"), 2, 0)
        self.layout.addWidget(self.weight_spin, 2, 1)
        self.layout.addWidget(QLabel("set date:"), 3, 0)
        self.layout.addWidget(self.date_editor, 3, 1)
        self.layout.addWidget(self.button_box, 4, 1)

        self.setWindowTitle("new Grade")
        self.setLayout(self.layout)
        # self.setWindowFlag(Qt.FramelessWindowHint)
        # centre = (self.x() + (self.frameGeometry().width() // 2) - (self.width() // 2),
        #           self.y() + (self.frameGeometry().height() // 2) - (self.height() // 2))
        # self.move(centre[0], centre[1])

    # def toggle_clicked(self):
    #     self.grade["visible"] = self.toggle.isChecked()

    # def grade_spin_edited(self):
    #     self.grade["grade"] = self.grade_spin.value()

    # def weight_spin_edited(self):
    #     self.grade["weight"] = self.weight_spin.value()

    # def date_edited(self):
    #     d = QDateTime()
    #     d.setDate(self.date_editor.date())
    #     self.grade["date"] = d.toSecsSinceEpoch()

    def accept(self) -> None:
        """overriden method to ensure the grade is saved before returning "super().accept()"

        Returns:
            _type_: literally "return super().accept()"
        """        
        d = QDateTime()
        d.setDate(self.date_editor.date())
        self.grade["date"] = d.toSecsSinceEpoch()
        self.grade["weight"] = self.weight_spin.value()
        self.grade["grade"] = self.grade_spin.value()
        self.grade["mask"] = self.toggle.isChecked()
        return super().accept()

    @staticmethod
    def getGrade(subj):
        """conveniency method that generates a grade dialog and starts it

        Args:
            subj (Subject): subject to wich the new grade will be added

        Returns:
            any: grade or None if the user has cancelled the action
        """
        d = newGradeDialog(subj)
        if d.exec():
            return d.grade
        return None
