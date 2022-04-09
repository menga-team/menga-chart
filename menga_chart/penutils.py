
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5 import *

from qtwidgets import AnimatedToggle


class penIcon(QToolButton):

    def __init__(self, subj) -> None:
        """A toolbutton that changes color based on its pen and displays the current thiccness

        Args:
            subj (Subject): The subject that holds the pen
        """        
        super().__init__()

        self.subj = subj

        self.clicked.connect(self.setColor)
        self.updateCosmetic()
        self.subj.sig.colorUpdate.connect(self.updateCosmetic)

    def setColor(self):
        """starts the penDialog
        """
        self.subj["pen"] = penDialog.getPen(self.subj["pen"], self)
        self.subj.updatePen()

    def updateCosmetic(self):
        """updates the buttons appearence and label to match the subjects pens properties
        """
        p = QPalette()
        p.setColor(self.backgroundRole(), QColor.fromRgb(
            *self.subj["pen"]["color"]))
        self.setText(str(self.subj["pen"]["width"]))

        # what is being done here is some fancy rgb color shit that decides if the label should be light or dark based on the backgroundcolor
        # P.S. thk u so fucking much u literally saved me from braindrainage "https://stackoverflow.com/questions/1855884/determine-font-color-based-on-background-color"
        if (0.299 * self.subj["pen"]["color"][0] + 0.587 * self.subj["pen"]["color"][1] + 0.114 * self.subj["pen"]["color"][2]) > 0.5:
            p.setColor(QPalette.ButtonText, Qt.black)

        else:
            p.setColor(QPalette.ButtonText, Qt.white)

        self.setPalette(p)

    # def paintEvent(self, a0) -> None:
    #     painter = QPainter(self)
    #     painter.fillRect(self.rect(), QColor.fromRgb(*self.pen["color"]))


class penDialog(QDialog):
    def __init__(self, pen, icon):
        """Dialog that enables a limited but okisch selection of the attributes the pen should have

        Args:
            pen (dict): the pen we want to modify
            icon (penIcon): The parent button that started the Dialog
        """
        super().__init__(icon)

        self.pen = pen.copy()
        self.icon = icon

        # initialize ui
        self.layout = QGridLayout()
        self.button_box = QDialogButtonBox(
            QDialogButtonBox.Cancel | QDialogButtonBox.Ok)
        self.spinLayout = QHBoxLayout()
        self.cosmetics_toggle = AnimatedToggle()
        self.widthSlider = QSlider(Qt.Horizontal)
        self.widthSpinBox = QSpinBox()
        self.colorButton = QToolButton()
        self.colorDialog = QColorDialog()

        # setup the button box
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

        # setup the cosmetics toggle
        self.cosmetics_toggle.setMaximumWidth(70)
        
        # setup the widthSlider
        self.widthSlider.setValue(self.pen["width"]) 
        self.widthSlider.setMinimum(0)
        self.widthSlider.setMaximum(50)
        self.widthSlider.setValue(self.pen["width"]) # y tf did i write this comand 2 times
        self.widthSlider.valueChanged.connect(self.onSliderChange)

        # setup the widthSlider
        self.widthSpinBox.setSingleStep(1)
        self.widthSpinBox.setValue(self.pen["width"])
        self.widthSpinBox.valueChanged.connect(self.onSpinBoxChange)

        # setup the colorDialog
        self.colorDialog.setOption(QColorDialog.NoButtons)
        self.colorDialog.setOption(QColorDialog.ShowAlphaChannel)
        self.colorDialog.setOption(QColorDialog.DontUseNativeDialog)
        
        # setup the colorButton
        self.colorButton.clicked.connect(self.setColor)
        self.colorButton.setIcon(self.colorButton.style(
        ).standardIcon(QStyle.SP_DialogResetButton))

        # self.colorDialog.setCurrentColor(QColor(self.pen["color"][0], self.pen["color"][1], self.pen["color"][2], self.pen["color"][3]))

        # compose the spinlayout
        self.spinLayout.addWidget(self.widthSlider)
        self.spinLayout.addWidget(self.widthSpinBox)

        # compose the ui
        self.layout.addWidget(QLabel("Cosmetc: "), 0, 0)
        self.layout.addWidget(self.cosmetics_toggle, 0, 1)
        self.layout.addWidget(QLabel("Width: "), 1, 0)
        self.layout.addLayout(self.spinLayout, 1, 1)
        self.layout.addWidget(QLabel("Color: "), 2, 0)
        self.layout.addWidget(self.colorButton, 2, 1)
        self.layout.addWidget(self.button_box, 3, 1)

        self.updateCosmetic()
        self.setWindowTitle("new Pen")
        self.setLayout(self.layout)

    def onSliderChange(self):
        """executed when the widthslider changes position
        """
        self.pen["width"] = self.widthSlider.value()
        self.widthSpinBox.setValue(self.widthSlider.value())
        self.updateCosmetic()

    def onSpinBoxChange(self):
        """executed when the spin box changes value
        """
        self.pen["width"] = self.widthSpinBox.value()
        self.widthSlider.setValue(self.widthSpinBox.value())
        self.updateCosmetic()

    def setColor(self):
        """opens a colorDialog and sets the new color to the pen
        """
        self.pen["color"] = self.colorDialog.getColor(QColor.fromRgb(
            *self.pen["color"]), parent=self.colorButton).getRgb()
        self.updateCosmetic()

    def updateCosmetic(self):
        """updates the ui to match the pencolor
        """
        p = self.colorButton.palette()
        p.setColor(self.colorButton.backgroundRole(),
                   QColor.fromRgb(*self.pen["color"]))
        self.colorButton.setPalette(p)

    # def reject(self) -> None:
    #     return super().accept()

    @staticmethod
    def getPen(pen, icon):
        """conveniency method that generates a pen dialog and starts it

        Args:
            pen (dict): the pen we want to modify
            icon (penIcon): The parent button that started the Dialog

        Returns:
            dict: the edited or unedited pen
        """
        d = penDialog(pen, icon)
        if d.exec():
            return d.pen
        return pen
