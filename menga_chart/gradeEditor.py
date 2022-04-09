from PyQt5 import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from qtwidgets import AnimatedToggle

try:
    import vertTabbing
    import newGrade
    import penutils
except ImportError:
    from menga_chart import vertTabbing
    from menga_chart import newGrade
    from menga_chart import penutils


class singleGradeEditor(QHBoxLayout):
    """layout that contains the ui components for modifing its assigned grade
    """
    def __init__(self, subj, grade, tab) -> None:
        """layout that contains the ui components for modifing its assigned grade

        Args:
            subj (Subject): parent Subject of grade.
            grade (dict): child dictionary of Subject that represents the grade the singleGradeEditor controlls. 
            tab (gradeEditorTab): basically the parent widget, but its a gradeEditorTab.
        """        
        super().__init__()

        # only for internal temporary use
        d = QDateTime()

        self.grade = grade
        self.subj = subj
        self.tab = tab

        # initiliaze ui components
        self.toggle = AnimatedToggle()
        self.grade_spin = QDoubleSpinBox()
        self.weight_spin = QSpinBox()
        self.remove_button = QToolButton()
        self.date_editor = QDateEdit()

        # set up visibilty toggle
        self.toggle.setChecked(self.grade["mask"])
        self.toggle.stateChanged.connect(self.toggle_visibilty)
        # set the minmum width to 70, as it looks shit otherwise
        self.toggle.setMinimumWidth(70)

        # setup the gradespin
        self.grade_spin.setSingleStep(0.5)
        self.grade_spin.setMaximum(10.25)
        self.grade_spin.setMinimum(-0.25)
        self.grade_spin.setValue(self.grade["grade"])
        # update the grade when the value is modiofied
        self.grade_spin.valueChanged.connect(lambda: subj.set_grade_value(
            self.subj["grades"].index(self.grade), self.grade_spin.value()))

        # setup the wheight spin
        self.weight_spin.setSingleStep(5)
        self.weight_spin.setMaximum(100)
        self.weight_spin.setMinimum(-0) # -0 cuz why not
        self.weight_spin.setValue(self.grade["weight"])
        # update the grade when the value is modiofied
        self.weight_spin.valueChanged.connect(lambda: subj.set_weight_value(
            self.subj["grades"].index(self.grade), self.weight_spin.value()))

        # setup the date_editor
        self.date_editor.setDisplayFormat("dd/MM/yyyy")
        self.date_editor.setDate(
            QDateTime.fromTime_t(self.grade["date"]).date())
        # when the date is modified update the grades date.
        # here we also use the QDateTime we declare earlier to convert a datestring to unixepoch
        self.date_editor.dateChanged.connect(lambda: [d.setDate(self.date_editor.date(
        )), subj.set_date_value(self.subj["grades"].index(self.grade), d.toSecsSinceEpoch())])
        self.date_editor.setCalendarPopup(True)

        # setup the remove button
        self.remove_button.setIcon(
            self.remove_button.style().standardIcon(QStyle.SP_DialogCloseButton))
        self.remove_button.clicked.connect(self.self_destruct)

        self.setAlignment(Qt.AlignLeft)

        # compose the ui
        self.addWidget(self.toggle)
        self.addWidget(QLabel("Grade: "))
        self.addWidget(self.grade_spin)
        self.addWidget(QLabel("weight: "))
        self.addWidget(self.weight_spin)
        self.addWidget(QLabel("date: "))
        self.addWidget(self.date_editor)
        self.addWidget(self.remove_button)

    def toggle_visibilty(self):
        """handles the updating etc when the visibitly is toggled
        """
        self.grade_spin.setEnabled(self.toggle.isChecked())
        self.weight_spin.setEnabled(self.toggle.isChecked())
        self.date_editor.setEnabled(self.toggle.isChecked())
        self.grade["mask"] = self.toggle.isChecked()
        self.subj.update()

    def self_destruct(self):
        """the method is invoked when we want to delete the grade. it basically shuts down the widget   
        """
        self.subj["grades"].remove(self.grade)
        self.subj.update()
        # we have to set every parent of every childwidget inside thee label to None so it deletes its c++ object in the memory
        # if we dont do it, we end up only deleting the python and the ui glitches trying to calculate objects that actually dont exist anymore 
        for i in [self.itemAt(i).widget() for i in range(self.count())]:
            i.setParent(None)
        self.setParent(None)
        # self.setParent(None)
        # self.deleteLater()
        # self.tab.update_single_editors()


class gradeEditorTab(QWidget):
    def __init__(self, subj) -> None:
        """the tab that contains and manages the singleGradeEditors inside it and surrounding ui to edit its Subject

        Args:
            subj (Subject): Subject assigned to the tab
        """
        super().__init__()

        self.subj = subj
        self.tab_button = None

        # list of all singleGradeEditors on schreen
        self.singleGradeEditors = []

        # initilize ui components
        self.colorGenToggle = AnimatedToggle()
        self.name_label = QLineEdit()
        self.name_box = QHBoxLayout()
        self.layout = QVBoxLayout()
        self.item_layout = QVBoxLayout()
        self.penIcon = penutils.penIcon(self.subj)
        self.addGradeButton = QPushButton()
        self.removeSubjectButton = QPushButton()

        # setup the cologeneration toggle
        self.colorGenToggle.setMinimumWidth(70)
        self.colorGenToggle.setChecked(self.subj["pen"]["dynamicColor"])
        self.colorGenToggle.stateChanged.connect(
            self.dynamic_color_generation_toggled)

        # setup the name label
        self.name_label.setText(subj["name"])
        self.name_label.setToolTip(subj["name"])
        self.name_label.textChanged.connect(self.name_change)
        # self.name_label.setSizePolicy(QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum))

        # setup the itemslayout
        self.item_layout.setAlignment(Qt.AlignTop)

        # setup the addGradeButton
        self.addGradeButton.clicked.connect(self.addGrade)
        self.addGradeButton.setIcon(
            self.addGradeButton.style().standardIcon(QStyle.SP_FileDialogNewFolder))
        self.addGradeButton.setText("New Grade")

        # setup the remove Subject button
        self.removeSubjectButton.clicked.connect(self.self_destruct)
        self.removeSubjectButton.setIcon(
            self.removeSubjectButton.style().standardIcon(QStyle.SP_DialogCloseButton))
        self.removeSubjectButton.setText("Delete Subject")

        # composse the namebox label
        self.name_box.addWidget(self.colorGenToggle)
        self.name_box.addWidget(self.name_label)
        self.name_box.addWidget(self.penIcon)
        self.name_box.addWidget(self.removeSubjectButton,
                                alignment=Qt.AlignRight)
        self.name_box.addWidget(self.addGradeButton, alignment=Qt.AlignRight)

        self.layout.setAlignment(Qt.AlignTop)

        # compose the ui
        self.layout.addLayout(self.name_box)
        self.layout.addWidget(QLabel("<hr></hr>"))
        self.layout.addLayout(self.item_layout)

        # go through every label in the subject and genereate a singleGradeEditors for it
        for i in range(len(self.subj.setdefault("grades", []))):
            layout = singleGradeEditor(self.subj, self.subj["grades"][i], self)
            self.singleGradeEditors.append(layout)
            self.item_layout.addLayout(layout)

        self.setLayout(self.layout)

    def dynamic_color_generation_toggled(self):
        """executed when the colorGenToggle is pressed
        """
        self.subj["pen"]["dynamicColor"] = self.colorGenToggle.isChecked()
        self.name_label.setFocus(True)

    def name_change(self):
        """executed when the name textbox is modified. also changes the Subject color if necessary
        """
        self.subj["name"] = self.name_label.text()
        self.subj.update()
        if self.subj["pen"]["dynamicColor"]:
            self.subj["pen"]["color"] = self.subj.generate_color()
            self.subj.sig.colorUpdate.emit()

    def self_destruct(self):
        """executed when the Subjectremoval button is pressed.
        """
        # emit the selfDestruct signal
        self.subj.self_destruct()
        # we set our own and our tab_buttons parent to None to delete their c++ objects from memory 
        self.setParent(None)
        self.tab_button.setParent(None)

    def addGrade(self):
        """executed when addGradeButton is pressed, so it handles the dialog and ui modifications
        """
        grade = newGrade.newGradeDialog.getGrade(self.subj)
        
        # If the grade is None it just means the user has cancelled the action and we dont need to add anything
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

    # old method from th stone age
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
        """contains the Entire grade Editor ui, logic and stuff

        Args:
            grades (list): list of Subjects the GradeEditor is initilized with
            chart (TimeChart): reference to the TimeChart as we need it for updating the poltlines on it whena grade or subject is edited
        """
        super().__init__()

        self.grades = grades
        self.chart = chart

        # initilize the verticval tab system
        self.tabs = vertTabbing.VertTabLayout(self)

        # go through every Subject in the list and initialize its very own vertical tab.
        for subj in self.grades:
            self.tabs.addTab(gradeEditorTab(subj), subj)

        self.setLayout(self.tabs)

    def addSubject(self):
        """used to add new Subjects to system (also handles the dialog and ui modifications)
        """
        # we import it now as to not cause importt recursion errors
        from newSubject import newSubjectDialog
        subj = newSubjectDialog.getSubject()
        
        # the Subject is None if the user has cancelle the action so we can safely return the function without changin anything
        if subj is None:
            return
        subj.chart = self.chart
        self.grades.append(subj)
        self.chart.addPlot(subj._id)
        self.tabs.addTab(gradeEditorTab(subj), subj)
