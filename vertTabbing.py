from tkinter.tix import ButtonBox
from PyQt5 import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from qtwidgets import AnimatedToggle
from newGrade import newGradeDialog
from penutils import penIcon

class VertTabButton(QPushButton):
    def __init__(self, stack, tab_widget, buttonlayout, buttonGroup, subj):
        super().__init__()

        self.stack = stack
        self.tab_widget = tab_widget
        self.buttonlayout = buttonlayout
        self.buttonGroup = buttonGroup
        self.subj = subj

        self.subj.sig.chartUpdate.connect(self.update_stats)

        self.layout = QVBoxLayout()
        self.button_layout = QHBoxLayout()
        self.label_layout = QHBoxLayout()
        self.name_label = QLabel()
        self.penButton = penIcon(self.subj)
        self.visibility_switch = AnimatedToggle()
        self.mode_combobox = QComboBox()
        self.remove_button = QToolButton()
        self.add_grade_button = QToolButton()

        self.mode_combobox.addItems(("precise", "average", "both"))
        self.mode_combobox.setCurrentIndex(subj["mode"])
        self.mode_combobox.activated.connect(lambda: self.update_mode())

        self.visibility_switch.setMinimumWidth(70)
        self.visibility_switch.stateChanged.connect(self.toggle_visibility)
        self.visibility_switch.setChecked(bool(subj["visible"]))
        
        self.add_grade_button.clicked.connect(newGradeDialog.getGrade)
        self.add_grade_button.setIcon(self.add_grade_button.style().standardIcon(QStyle.SP_FileDialogNewFolder))

        self.remove_button.setIcon(self.remove_button.style().standardIcon(QStyle.SP_DialogCloseButton))
        self.remove_button.clicked.connect(self.on_self_destruct)

        self.layout.addWidget(self.name_label)
        self.layout.addLayout(self.button_layout)
        self.button_layout.addWidget(self.visibility_switch, alignment=Qt.AlignCenter)
        self.button_layout.addWidget(self.mode_combobox, alignment=Qt.AlignCenter)
        self.button_layout.addWidget(self.add_grade_button, alignment=Qt.AlignCenter)
        self.button_layout.addWidget(self.penButton, alignment=Qt.AlignCenter)
        self.button_layout.addWidget(self.remove_button, alignment=Qt.AlignCenter)

        self.setFlat(True)
        self.setCheckable(True)
        self.clicked.connect(self.on_click)
        # self.setSizePolicy(QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed))
        self.setMinimumHeight(90)
        self.setLayout(self.layout)
    
    def on_self_destruct(self):
        self.tab_widget.self_destruct()
        if len(self.stack.children()) > 0:
            self.buttonlayout.itemAt(0).widget().click()
    
    def on_click(self):
        # for i in [self.buttonlayout.itemAt(i).widget() for i in range(self.buttonlayout.count())]:
        #     i.setChecked(False)
        # self.setChecked(True)
        
        self.stack.setCurrentWidget(self.tab_widget)

    def toggle_visibility(self):
        self.subj["visible"] = self.visibility_switch.isChecked()
        visible = self.subj["visible"]
        for i in self.tab_widget.singleGradeEditors:
            i.grade_spin.setEnabled(visible)
            i.weight_spin.setEnabled(visible)
            i.toggle.setEnabled(visible)
            i.remove_button.setEnabled(visible)
        self.subj.update()

    def update_mode(self):
        self.subj["mode"] = self.mode_combobox.currentIndex()
        self.subj.update()

    def add_grade(self):
        self.tab_widget.addGrade(self.subj)

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
        self.buttonGroup = QButtonGroup()
        self.button_layout = QVBoxLayout()
        self.scroll = QScrollArea()
        self.widget = QWidget()

        self.widget.setLayout(self.button_layout)

        self.scroll.setMinimumWidth(300)
        self.scroll.setWidget(self.widget)        
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll.setWidgetResizable(True)
        # policy = self.scroll.sizePolicy()
        # policy.setHorizontalPolicy(QSizePolicy.Expanding)
        # self.scroll.setSizePolicy(policy)

        self.button_layout.setAlignment(Qt.AlignTop)
        
        self.buttonGroup.setExclusive(True)

        self.setContentsMargins(0, 0, 0, 0)

        self.addWidget(self.scroll, alignment=Qt.AlignLeft)
        self.addLayout(self.stack)

    def addTab(self, widget, subj):
        self.stack.addWidget(widget)
        button = VertTabButton(self.stack, widget, self.button_layout, self.buttonGroup, subj)
        widget.tab_button = button
        self.button_layout.insertWidget(0, button)
        self.buttonGroup.addButton(button)
        
        if len(self.stack.children()) < 2:
            button.click()