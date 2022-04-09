from PyQt5 import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from qtwidgets import AnimatedToggle

try:
    import newGrade
    import penutils
except ImportError:
    from menga_chart import newGrade
    from menga_chart import penutils


class VertTabButton(QPushButton):
    def __init__(self, stack, tab_widget, buttonlayout, buttonGroup, subj):
        """The Button on the side of the tab panel.`

        Args:
            stack (QStack): the stack on the other side of the oanel
            tab_widget (QWidget): the assigned tab widget to diplay when clicked
            buttonlayout (QVLayout): the paretn of the parent layout
            buttonGroup (QButtongroup): the button group that controlls the button
            subj (Subject): the subject that the button represents
        """
        super().__init__()

        self.stack = stack
        self.tab_widget = tab_widget
        self.buttonlayout = buttonlayout
        self.buttonGroup = buttonGroup
        self.subj = subj

        self.subj.sig.chartUpdate.connect(self.update_stats)

        # initilize the ui
        self.layout = QVBoxLayout()
        self.button_layout = QHBoxLayout()
        self.label_layout = QHBoxLayout()
        self.name_label = QLabel()
        self.penButton = penutils.penIcon(self.subj)
        self.visibility_switch = AnimatedToggle()
        self.mode_combobox = QComboBox()
        self.remove_button = QToolButton()
        self.add_grade_button = QToolButton()

        # setup the mode combobox
        self.mode_combobox.addItems(("precise", "average", "both"))
        self.mode_combobox.setCurrentIndex(subj["mode"])
        self.mode_combobox.activated.connect(lambda: self.update_mode())

        #  setup the visibility switch
        self.visibility_switch.setMinimumWidth(70)
        self.visibility_switch.stateChanged.connect(self.toggle_visibility)
        self.visibility_switch.setChecked(bool(subj["visible"]))

        # setup the add grade button
        self.add_grade_button.clicked.connect(newGrade.newGradeDialog.getGrade)
        self.add_grade_button.setIcon(
            self.add_grade_button.style().standardIcon(QStyle.SP_FileDialogNewFolder))

        # setup the remove subject button
        self.remove_button.setIcon(
            self.remove_button.style().standardIcon(QStyle.SP_DialogCloseButton))
        self.remove_button.clicked.connect(self.on_self_destruct)

        # compose the ui
        self.layout.addWidget(self.name_label)
        self.layout.addLayout(self.button_layout)
        self.button_layout.addWidget(
            self.visibility_switch, alignment=Qt.AlignCenter)
        self.button_layout.addWidget(
            self.mode_combobox, alignment=Qt.AlignCenter)
        self.button_layout.addWidget(
            self.add_grade_button, alignment=Qt.AlignCenter)
        self.button_layout.addWidget(self.penButton, alignment=Qt.AlignCenter)
        self.button_layout.addWidget(
            self.remove_button, alignment=Qt.AlignCenter)

        self.setFlat(True)
        self.setCheckable(True)
        self.clicked.connect(self.on_click)
        # self.setSizePolicy(QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed))
        # the minimum height is nexcessay to avoid weird bugs.
        self.setMinimumHeight(90)
        self.setLayout(self.layout)

    def on_self_destruct(self):
        """executed when we want to destroy the Subject and Button
        """
        self.tab_widget.self_destruct()
        # here we select the next button and click it to ensure that evn after the current button is removed there is always one clicked button
        if len(self.stack.children()) > 0:
            self.buttonlayout.itemAt(0).widget().click()

    def on_click(self):
        """is execuited when the button is clicked
        """
        # for i in [self.buttonlayout.itemAt(i).widget() for i in range(self.buttonlayout.count())]:
        #     i.setChecked(False)
        # self.setChecked(True)

        self.stack.setCurrentWidget(self.tab_widget)

    def toggle_visibility(self):
        """executed when the visibility swicth is flipped, it handles the logic of hiding entire Subjects from the human eye (pretty impressiv right?)
        """
        self.subj["visible"] = self.visibility_switch.isChecked()
        visible = self.subj["visible"]
        # disable all editing components since the Subject is disabled anyways
        for i in self.tab_widget.singleGradeEditors:
            i.grade_spin.setEnabled(visible)
            i.weight_spin.setEnabled(visible)
            i.toggle.setEnabled(visible)
            i.remove_button.setEnabled(visible)
        self.subj.update()

    def update_mode(self):
        """updates the viewmode on the plotchart"""
        self.subj["mode"] = self.mode_combobox.currentIndex()
        self.subj.update()

    def add_grade(self):
        """adds a new grade to the Subject"""
        self.tab_widget.addGrade(self.subj)

    def update_stats(self):
        """updates the statistics on the ButtonLabel
        """
        self.name_label.setText(
            f"{self.subj['name']} [{self.subj.get_average(True)}, {len(self.subj['grades'])}]")

    # def paintEvent(self, e) -> None:
    #     if self.isChecked():
    #         painter = QPainter(self)
    #         painter.fillRect(self.rect(), self.palette().highlight().color())
    #     # super().paintEvent(e)


class VertTabLayout(QHBoxLayout):
    def __init__(self, parent):
        """left panle of the ui that contains the tgabbuttons

        Args:
            parent (QWidget): parent widget came back with the milk
        """
        super().__init__()
        self.parent = parent 

        # initilize the ui
        self.stack = QStackedLayout()
        self.buttonGroup = QButtonGroup()
        self.button_layout = QVBoxLayout()
        self.button_sub_layout = QVBoxLayout()
        self.add_subject_button = QPushButton()
        self.scroll = QScrollArea()
        self.widget = QWidget()

        self.widget.setLayout(self.button_layout)

        # setup the scroll area
        self.scroll.setMinimumWidth(300)
        self.scroll.setWidget(self.widget)
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll.setWidgetResizable(True)
        # policy = self.scroll.sizePolicy()
        # policy.setHorizontalPolicy(QSizePolicy.Expanding)
        # self.scroll.setSizePolicy(policy)
        
        # setup the add Subject button
        self.add_subject_button.setIcon(self.add_subject_button.style().standardIcon(QStyle.SP_ToolBarVerticalExtensionButton))
        self.add_subject_button.clicked.connect(self.parent.addSubject)
        
        # compose the button layout
        self.button_layout.setAlignment(Qt.AlignTop)
        self.button_layout.addLayout(self.button_sub_layout)
        self.button_layout.addWidget(self.add_subject_button)
        
        # compose the rest of the ui 
        self.button_sub_layout.setAlignment(Qt.AlignTop)

        self.buttonGroup.setExclusive(True)

        self.setContentsMargins(0, 0, 0, 0)

        self.addWidget(self.scroll, alignment=Qt.AlignLeft)
        self.addLayout(self.stack)

    def addTab(self, widget, subj):
        """adds a new vertical tabwidget and button to my collection

        Args:
            widget (QWidget): widget we want to add
            subj (dict): The subject it willl controll (did i mention the widget has to be a gradeditortab?)
        """
        self.stack.addWidget(widget)
        button = VertTabButton(
            self.stack, widget, self.button_sub_layout, self.buttonGroup, subj)
        widget.tab_button = button
        self.button_sub_layout.insertWidget(0, button)
        self.buttonGroup.addButton(button)

        # if its the only button, click it to avoid embarassing situations
        if len(self.stack.children()) < 2:
            button.click()
