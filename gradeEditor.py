from PyQt5 import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from qtwidgets import AnimatedToggle


class VertTabButton(QPushButton):
    def __init__(self, stack, tab_widget, buttonlayout, subj):
        super().__init__()

        self.stack = stack
        self.tab_widget = tab_widget
        self.buttonlayout = buttonlayout
        self.subj = subj

        self.subj.execute_on_update.append(self.update_stats)

        self.layout = QVBoxLayout()
        self.button_layout = QHBoxLayout()
        self.label_layout = QHBoxLayout()
        self.name_label = QLabel()
        self.visibility_switch = AnimatedToggle()
        self.mode_switch = AnimatedToggle()
        self.remove_button = QToolButton()
        self.add_grade_button = QToolButton()

        self.mode_switch.setFixedWidth(70)
        self.mode_switch.stateChanged.connect(self.toggle_mode)
        self.mode_switch.setChecked(subj.visible)

        self.visibility_switch.setMinimumWidth(70)
        self.visibility_switch.stateChanged.connect(self.toggle_visibility)
        self.visibility_switch.setChecked(bool(subj.mode))

        self.remove_button.setIcon(self.remove_button.style().standardIcon(QStyle.SP_DialogCloseButton))
        self.remove_button.clicked.connect(self.self_destruct)

        self.layout.addWidget(self.name_label)
        self.layout.addLayout(self.button_layout)
        self.button_layout.addWidget(self.visibility_switch, alignment=Qt.AlignCenter)
        self.button_layout.addWidget(self.mode_switch, alignment=Qt.AlignCenter)
        self.button_layout.addWidget(self.add_grade_button, alignment=Qt.AlignCenter)
        self.button_layout.addWidget(self.remove_button, alignment=Qt.AlignCenter)

        self.setCheckable(True)
        self.clicked.connect(self.on_click)
        # self.setSizePolicy(QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed))
        self.setMinimumHeight(90)
        self.setLayout(self.layout)
    
    def on_click(self):
        for i in [self.buttonlayout.itemAt(i).widget() for i in range(self.buttonlayout.count())]:
            i.setChecked(False)
        self.setChecked(True)
        self.stack.setCurrentWidget(self.tab_widget)

    def toggle_visibility(self):
        self.subj.visible = self.visibility_switch.isChecked()
        visible = self.subj.visible
        for i in self.tab_widget.singleGradeEditors:
            i.grade_spin.setEnabled(visible)
            i.weight_spin.setEnabled(visible)
            i.toggle.setEnabled(visible)
            i.remove_button.setEnabled(visible)
        self.subj.update()

    def toggle_mode(self):
        self.subj.mode = 1 if self.mode_switch.isChecked() else 0
        self.subj.update()

    def add_grade(self):
        pass

    def self_destruct(self):
        self.subj.self_destruct()
        del self.subj
        self.setParent(None)
        self.tab_widget.setParent(None)

    def update_stats(self):
        self.name_label.setText(f"{self.subj['name']} [{self.subj.get_average(True)}, {len(self.subj['grades'])}]")
    
    # def paintEvent(self, e) -> None:
    #     if self.isChecked():
    #         painter = QPainter(self)
    #         painter.fillRect(self.rect(), self.palette().highlight().color())
    #     # super().paintEvent(e)

class VertTabLayout(QHBoxLayout):
    def __init__(self):
        super().__init__()

        self.stack = QStackedLayout()
        self.button_layout = QVBoxLayout()
        self.scroll = QScrollArea()
        self.widget = QWidget()

        self.widget.setLayout(self.button_layout)

        self.scroll.setMinimumWidth(230)
        self.scroll.setWidget(self.widget)        
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll.setWidgetResizable(True)

        self.button_layout.setAlignment(Qt.AlignTop)

        self.setContentsMargins(0, 0, 0, 0)

        self.addWidget(self.scroll, alignment=Qt.AlignLeft)
        self.addLayout(self.stack)

    def addTab(self, widget, subj):
        self.stack.addWidget(widget)
        button = VertTabButton(self.stack, widget, self.button_layout, subj)
        self.button_layout.addWidget(button)


class singleGradeEditor(QHBoxLayout):
    def __init__(self, subj, index, tab) -> None:
        super().__init__()
        
        d = QDateTime()

        self.index = index
        self.subj = subj
        self.tab = tab
        self.grade = subj["grades"][self.index]

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
        self.grade_spin.valueChanged.connect(lambda: subj.set_grade_value(self.index, self.grade_spin.value()))

        self.weight_spin.setSingleStep(5)
        self.weight_spin.setMaximum(100)
        self.weight_spin.setMinimum(-0)
        self.weight_spin.setValue(self.grade["weight"])
        self.weight_spin.valueChanged.connect(lambda: subj.set_weight_value(self.index, self.weight_spin.value()))

        self.date_editor.setDisplayFormat("dd/MM/yyyy")
        self.date_editor.setDate(QDateTime.fromTime_t(self.grade["date"]).date())
        self.date_editor.dateChanged.connect(lambda: [d.setDate(self.date_editor.date()), subj.set_date_value(self.index, d.toSecsSinceEpoch())])
        self.date_editor.setCalendarPopup(True)

        self.remove_button.setIcon(self.remove_button.style().standardIcon(QStyle.SP_DialogCloseButton))
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

        self.singleGradeEditors = []

        self.name_box = QLineEdit()
        self.layout = QVBoxLayout()
        self.item_layout = QVBoxLayout()

        self.name_box.setText(subj["name"])
        self.name_box.setToolTip(subj["name"])
        self.name_box.textChanged.connect(self.name_change)
        self.name_box.setSizePolicy(QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum))
        
        self.item_layout.setAlignment(Qt.AlignTop)

        self.layout.setAlignment(Qt.AlignTop)

        self.layout.addWidget(self.name_box)
        self.layout.addWidget(QLabel("<hr></hr>"))
        self.layout.addLayout(self.item_layout)

        for i in range(len(self.subj["grades"])):
            layout = singleGradeEditor(self.subj, i, self)
            self.singleGradeEditors.append(layout)
            self.item_layout.addLayout(layout)

        self.setLayout(self.layout)
    
    def name_change(self):
        self.subj["name"] = self.name_box.toPlainText()
        self.subj.update()

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

        self.tabs = VertTabLayout()

        for subj in self.grades:
            self.tabs.addTab(gradeEditorTab(subj, chart), subj)


        self.setLayout(self.tabs)