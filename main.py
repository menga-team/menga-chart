from ast import ExceptHandler
import sys
import time

import numpy as np

from PyQt5 import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from window import *
import utils

def main():
    utils.Exeption_handler(Window, app)


if __name__ == "__main__":
    # Check whether there is already a running QApplication (e.g., if running
    # from an IDE).
    app = QApplication.instance()
    if not app:
        app = QApplication(sys.argv)

    main()


# import pyqtgraph.examples
# pyqtgraph.examples.run()