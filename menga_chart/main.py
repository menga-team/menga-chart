import sys

from PyQt5 import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

# there are a few import prolems when tryng to make a python project executable from source and form module
try: 
    # first we try to import the needed code relativly in case its being run from source
    import window
    import utils
except ImportError:
    # if it fails we assume the user has executed the module and import from there
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
