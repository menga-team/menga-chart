import sys

from PyQt5 import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from menga_chart.window import *
from menga_chart.utils import *


# Check whether there is already a running QApplication (e.g., if running
# from an IDE).
app = QApplication.instance()
if not app:
    app = QApplication(sys.argv)

def main():
    Exeption_handler(Window, app)


if __name__ == "__main__":
    main()


# import pyqtgraph.examples
# pyqtgraph.examples.run()
