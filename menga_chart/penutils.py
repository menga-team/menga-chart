
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5 import *
from qtwidgets import AnimatedToggle


class penIcon(QToolButton):

    def __init__(self, subj) -> None:
        super().__init__()

        self.subj = subj

        self.clicked.connect(self.setColor)
        self.updateCosmetic()
        self.subj.sig.colorUpdate.connect(self.updateCosmetic)

    def setColor(self):
        self.subj["pen"] = penDialog.getPen(self.subj["pen"], self)
        self.subj.updatePen()

    def updateCosmetic(self):
        p = QPalette()
        p.setColor(self.backgroundRole(), QColor.fromRgb(
            *self.subj["pen"]["color"]))
        self.setText(str(self.subj["pen"]["width"]))

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
        super().__init__(icon)

        self.pen = pen.copy()
        self.icon = icon

        self.layout = QGridLayout()
        self.button_box = QDialogButtonBox(
            QDialogButtonBox.Cancel | QDialogButtonBox.Ok)
        self.spinLayout = QHBoxLayout()
        self.cosmetics_toggle = AnimatedToggle()
        self.widthSlider = QSlider(Qt.Horizontal)
        self.widthSpinBox = QSpinBox()
        self.colorButton = QToolButton()
        self.colorDialog = QColorDialog()

        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

        self.cosmetics_toggle.setMaximumWidth(70)
        self.widthSlider.setValue(self.pen["width"])

        self.widthSlider.setMinimum(0)
        self.widthSlider.setMaximum(50)
        self.widthSlider.setValue(self.pen["width"])
        self.widthSlider.valueChanged.connect(self.onSliderChange)

        self.widthSpinBox.setSingleStep(1)
        self.widthSpinBox.setValue(self.pen["width"])
        self.widthSpinBox.valueChanged.connect(self.onSpinBoxChange)

        self.colorDialog.setOption(QColorDialog.NoButtons)
        self.colorDialog.setOption(QColorDialog.ShowAlphaChannel)
        self.colorDialog.setOption(QColorDialog.DontUseNativeDialog)

        self.colorButton.clicked.connect(self.setColor)
        self.colorButton.setIcon(self.colorButton.style(
        ).standardIcon(QStyle.SP_DialogResetButton))

        # self.colorDialog.setCurrentColor(QColor(self.pen["color"][0], self.pen["color"][1], self.pen["color"][2], self.pen["color"][3]))

        self.spinLayout.addWidget(self.widthSlider)
        self.spinLayout.addWidget(self.widthSpinBox)

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
        self.pen["width"] = self.widthSlider.value()
        self.widthSpinBox.setValue(self.widthSlider.value())
        self.updateCosmetic()

    def onSpinBoxChange(self):
        self.pen["width"] = self.widthSpinBox.value()
        self.widthSlider.setValue(self.widthSpinBox.value())
        self.updateCosmetic()

    def setColor(self):
        self.pen["color"] = self.colorDialog.getColor(QColor.fromRgb(
            *self.pen["color"]), parent=self.colorButton).getRgb()
        self.updateCosmetic()

    def updateCosmetic(self):
        p = self.colorButton.palette()
        p.setColor(self.colorButton.backgroundRole(),
                   QColor.fromRgb(*self.pen["color"]))
        self.colorButton.setPalette(p)

    # def reject(self) -> None:
    #     return super().accept()

    @staticmethod
    def getPen(pen, icon):
        d = penDialog(pen, icon)
        if d.exec():
            return d.pen
        return pen
