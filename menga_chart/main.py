import sys

from PyQt5 import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

try: 
    import window
    import utils
except ImportError:
    from menga_chart import window
    from menga_chart import utils
    


# Check whether there is already a running QApplication (e.g., if running
# from an IDE).
app = QApplication.instance()
if not app:
    app = QApplication(sys.argv)

def main():
    utils.Exeption_handler(window.Window, app)


if __name__ == "__main__":
    main()


# import pyqtgraph.examples
# pyqtgraph.examples.run()
