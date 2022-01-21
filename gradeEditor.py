from PyQt5 import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from qtwidgets import AnimatedToggle


class VertTabButton(QPushButton):
    def __init__(self, stack, tab_widget, grade_count, name, average):
        super().__init__()

        self.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding))

        self.name = name
        self.average = average
        self.grade_count = grade_count
        self.stack = stack
        self.tab_widget = tab_widget

        self.layout = QGridLayout()
        self.name_label = QLabel(f"{self.name} [{self.average}, {self.grade_count}]")
        self.visibility_switch = AnimatedToggle()
        self.mode_switch = AnimatedToggle()
        self.remove_button = QToolButton()

        self.clicked.connect(self.on_click)

        self.layout.addWidget(self.name_label, 0, 0)

        self.setLayout(self.layout)
    
    def on_click(self):
        self.stack.setCurrentWidget(self.tab_widget)

    def toggle_visibility(self):
        pass

    def toggle_mode(self):
        pass
    
    def update_stats(self):
        self.name_label.setText(f"{self.name} [{self.average}, {self.grade_count}]")
    
    # def paintEvent(self, e) -> None:
    #     pass

class VertTabWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QHBoxLayout()
        self.stack = QStackedLayout()
        self.button_layout = QVBoxLayout()
        self.scroll = QScrollArea()

        self.scroll.setLayout(self.button_layout)

        self.layout.addWidget(self.scroll)
        self.layout.addLayout(self.stack)
        self.setLayout(self.layout)

    def addTab(self, widget, grade_count, name, average):
        self.stack.addWidget(widget)
        button = VertTabButton(self.stack, widget, grade_count, name, average)
        self.button_layout.addWidget(button)


class singleGradeEditor(QHBoxLayout):
    def __init__(self, subj, index, tab) -> None:
        super().__init__()

        self.index = index
        self.subj = subj
        self.tab = tab
        self.grade = subj["grades"][self.index]

        self.toggle = AnimatedToggle()
        self.grade_spin = QDoubleSpinBox()
        self.weight_spin = QSpinBox()
        self.remove_button = QToolButton()

        self.toggle.setChecked(self.grade["mask"])
        self.toggle.stateChanged.connect(self.toggle_visibilty)

        self.grade_spin.setSingleStep(0.5)
        self.grade_spin.setMaximum(10.25)
        self.grade_spin.setMinimum(-0.25)
        self.grade_spin.setValue(self.grade["grade"])
        self.grade_spin.valueChanged.connect(lambda: subj.set_grade_value(self.index, self.grade_spin.value()))


        self.weight_spin.setSingleStep(5)
        self.weight_spin.setMaximum(100)
        self.weight_spin.setMinimum(-0)
        self.weight_spin.setValue(self.grade["weight"])
        self.weight_spin.valueChanged.connect(lambda: subj.set_weight_value(self.index, self.weight_spin.value()))

        self.remove_button.setIcon(self.remove_button.style().standardIcon(QStyle.SP_DialogCloseButton))
        self.remove_button.clicked.connect(self.self_destruct)


        self.addWidget(self.toggle)
        self.addWidget(QLabel("Grade: "))
        self.addWidget(self.grade_spin)
        self.addWidget(QLabel("weight: "))
        self.addWidget(self.weight_spin)
        self.addWidget(self.remove_button)
    
    def toggle_visibilty(self):
        self.grade_spin.setEnabled(self.toggle.isChecked())
        self.weight_spin.setEnabled(self.toggle.isChecked())
        self.grade["mask"] = self.toggle.isChecked()
        self.subj.update()
    
    def self_destruct(self):
        del self.grade
        self.subj.update()
        self.parent().setParent(None)
        # self.setParent(None)
        # self.deleteLater()
        # self.tab.update_single_editors()


class gradeEditorTab(QWidget):
    def __init__(self, subj, chart) -> None:
        super().__init__()
        
        self.chart = chart
        self.subj = subj
        self.layout = QVBoxLayout()
        # self.update_single_editors()


        for i in range(len(self.subj["grades"])):
            layout = singleGradeEditor(self.subj, i, self)
            widget = QWidget()
            widget.setLayout(layout)
            self.layout.addWidget(widget)

        self.setLayout(self.layout)
    
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

        self.tabs = VertTabWidget()
        for subj in self.grades:
            self.tabs.addTab(gradeEditorTab(subj, chart), len(subj["grades"]), subj["name"], subj.get_average(True))


        self.layout = QHBoxLayout()
        self.layout.addWidget(self.tabs)

        self.setLayout(self.layout)