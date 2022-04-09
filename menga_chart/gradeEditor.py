from PyQt5 import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from menga_chart.vertTabbing import *
from qtwidgets import AnimatedToggle
from menga_chart.newGrade import newGradeDialog


class singleGradeEditor(QHBoxLayout):
    def __init__(self, subj, grade, tab) -> None:
        super().__init__()

        d = QDateTime()

        self.grade = grade
        self.subj = subj
        self.tab = tab

        self.toggle = AnimatedToggle()
        self.grade_spin = QDoubleSpinBox()
        self.weight_spin = QSpinBox()
        self.remove_button = QToolButton()
        self.date_editor = QDateEdit()

        self.toggle.setChecked(self.grade["mask"])
        self.toggle.stateChanged.connect(self.toggle_visibilty)
        self.toggle.setMinimumWidth(70)

        self.grade_spin.setSingleStep(0.5)
        self.grade_spin.setMaximum(10.25)
        self.grade_spin.setMinimum(-0.25)
        self.grade_spin.setValue(self.grade["grade"])
        self.grade_spin.valueChanged.connect(lambda: subj.set_grade_value(
            self.subj["grades"].index(self.grade), self.grade_spin.value()))

        self.weight_spin.setSingleStep(5)
        self.weight_spin.setMaximum(100)
        self.weight_spin.setMinimum(-0)
        self.weight_spin.setValue(self.grade["weight"])
        self.weight_spin.valueChanged.connect(lambda: subj.set_weight_value(
            self.subj["grades"].index(self.grade), self.weight_spin.value()))

        self.date_editor.setDisplayFormat("dd/MM/yyyy")
        self.date_editor.setDate(
            QDateTime.fromTime_t(self.grade["date"]).date())
        self.date_editor.dateChanged.connect(lambda: [d.setDate(self.date_editor.date(
        )), subj.set_date_value(self.subj["grades"].index(self.grade), d.toSecsSinceEpoch())])
        self.date_editor.setCalendarPopup(True)

        self.remove_button.setIcon(
            self.remove_button.style().standardIcon(QStyle.SP_DialogCloseButton))
        self.remove_button.clicked.connect(self.self_destruct)

        self.setAlignment(Qt.AlignLeft)

        self.addWidget(self.toggle)
        self.addWidget(QLabel("Grade: "))
        self.addWidget(self.grade_spin)
        self.addWidget(QLabel("weight: "))
        self.addWidget(self.weight_spin)
        self.addWidget(QLabel("date: "))
        self.addWidget(self.date_editor)
        self.addWidget(self.remove_button)

    def toggle_visibilty(self):
        self.grade_spin.setEnabled(self.toggle.isChecked())
        self.weight_spin.setEnabled(self.toggle.isChecked())
        self.date_editor.setEnabled(self.toggle.isChecked())
        self.grade["mask"] = self.toggle.isChecked()
        self.subj.update()

    def self_destruct(self):
        self.subj["grades"].remove(self.grade)
        self.subj.update()
        for i in [self.itemAt(i).widget() for i in range(self.count())]:
            i.setParent(None)
        self.setParent(None)
        # self.setParent(None)
        # self.deleteLater()
        # self.tab.update_single_editors()


class gradeEditorTab(QWidget):
    def __init__(self, subj) -> None:
        super().__init__()

        self.subj = subj
        self.tab_button = None

        self.singleGradeEditors = []

        self.colorGenToggle = AnimatedToggle()
        self.name_label = QLineEdit()
        self.name_box = QHBoxLayout()
        self.layout = QVBoxLayout()
        self.item_layout = QVBoxLayout()
        self.penIcon = penIcon(self.subj)
        self.addGradeButton = QPushButton()
        self.removeSubjectButton = QPushButton()

        self.colorGenToggle.setMinimumWidth(70)
        self.colorGenToggle.setChecked(self.subj["pen"]["dynamicColor"])
        self.colorGenToggle.stateChanged.connect(
            self.dynamic_color_generation_toggled)

        self.name_label.setText(subj["name"])
        self.name_label.setToolTip(subj["name"])
        self.name_label.textChanged.connect(self.name_change)
        # self.name_label.setSizePolicy(QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum))

        self.item_layout.setAlignment(Qt.AlignTop)

        self.addGradeButton.clicked.connect(self.addGrade)
        self.addGradeButton.setIcon(
            self.addGradeButton.style().standardIcon(QStyle.SP_FileDialogNewFolder))
        self.addGradeButton.setText("New Grade")

        self.removeSubjectButton.clicked.connect(self.self_destruct)
        self.removeSubjectButton.setIcon(
            self.removeSubjectButton.style().standardIcon(QStyle.SP_DialogCloseButton))
        self.removeSubjectButton.setText("Delete Subject")

        self.name_box.addWidget(self.colorGenToggle)
        self.name_box.addWidget(self.name_label)
        self.name_box.addWidget(self.penIcon)
        self.name_box.addWidget(self.removeSubjectButton,
                                alignment=Qt.AlignRight)
        self.name_box.addWidget(self.addGradeButton, alignment=Qt.AlignRight)

        self.layout.setAlignment(Qt.AlignTop)

        self.layout.addLayout(self.name_box)
        self.layout.addWidget(QLabel("<hr></hr>"))
        self.layout.addLayout(self.item_layout)

        for i in range(len(self.subj.setdefault("grades", []))):
            layout = singleGradeEditor(self.subj, self.subj["grades"][i], self)
            self.singleGradeEditors.append(layout)
            self.item_layout.addLayout(layout)

        self.setLayout(self.layout)

    def dynamic_color_generation_toggled(self):
        self.subj["pen"]["dynamicColor"] = self.colorGenToggle.isChecked()
        self.name_label.setFocus(True)

    def name_change(self):
        self.subj["name"] = self.name_label.text()
        self.subj.update()
        if self.subj["pen"]["dynamicColor"]:
            self.subj["pen"]["color"] = self.subj.generate_color()
            self.subj.sig.colorUpdate.emit()

    def self_destruct(self):
        self.subj.self_destruct()
        self.setParent(None)
        self.tab_button.setParent(None)

    def addGrade(self):
        grade = newGradeDialog.getGrade(self.subj)
        if grade is None:
            return
        self.subj["grades"].append(grade)
        self.subj.sort_grades()

        layout = singleGradeEditor(self.subj, grade, self)
        self.singleGradeEditors.append(layout)
        self.item_layout.insertLayout(self.subj["grades"].index(grade), layout)
        self.subj.update()

        if self.tab_button is not None:
            self.tab_button.update_stats()

    # def update_single_editors(self):
    #     # self.layout = QVBoxLayout()
    #     # self.setLayout(self.layout)

    #     for i in range(len(self.subj["grades"])):
    #         layout = singleGradeEditor(self.subj, i, self)
    #         widget = QWidget()
    #         widget.setLayout(layout)
    #         self.layout.addWidget(widget)
    #     for i in [self.layout.itemAt(i).widget() for i in range(self.layout.count())]:
    #         i.setParent(None)
    #         i.deleteLater()
    #         # print(i)
    #     self.setLayout(self.layout)


class gradeEditor(QWidget):
    def __init__(self, grades, chart) -> None:
        super().__init__()

        self.grades = grades
        self.chart = chart

        self.tabs = VertTabLayout(self)

        for subj in self.grades:
            self.tabs.addTab(gradeEditorTab(subj), subj)

        self.setLayout(self.tabs)

    def addSubject(self):
        from newSubject import newSubjectDialog
        subj = newSubjectDialog.getSubject()
        if subj is None:
            return
        subj.chart = self.chart
        self.grades.append(subj)
        self.chart.addPlot(subj._id)
        self.tabs.addTab(gradeEditorTab(subj), subj)
