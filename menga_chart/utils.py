from PyQt5 import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

# lmao this was the first try at a vertical tab widget.
# it kind of reminds me of myself.
# ig were both failures
# class VertTabBar(QTabBar):
#     def tabSizeHint(self, index):
#         s = QTabBar.tabSizeHint(self, index)
#         s.transpose()
#         return s

#     def paintEvent(self, event):
#         painter = QStylePainter(self)
#         opt = QStyleOptionTab()

#         for i in range(self.count()):
#             self.initStyleOption(opt, i)
#             painter.drawControl(QStyle.CE_TabBarTabShape, opt)
#             painter.save()

#             s = opt.rect.size()
#             s.transpose()
#             r = QRect(QPoint(), s)
#             r.moveCenter(opt.rect.center())
#             opt.rect = r

#             rect = self.tabRect(i)
#             c = rect.center()
#             painter.translate(c)
#             painter.rotate(90)
#             painter.translate(-c)
#             v = QPoint(10, 0)
#             painter.translate(v)
#             painter.drawControl(QStyle.CE_TabBarTabLabel, opt)
#             painter.restore()

# class VertTabWidget(QTabWidget):
#     def __init__(self, *args, **kwargs):
#         QTabWidget.__init__(self, *args, **kwargs)
#         self.TabBar = VertTabBar()
#         self.setTabBar(self.TabBar)
#         self.setTabPosition(QTabWidget.West)
#         self.switches = []

#     def addTab(self, *args):
#         super().addTab(*args)
#         switch = QToolButton()
#         self.switches.append(switch)

#         # planning o slap a switch on every tab so u can quickly turn on and of any itmes. comletly broken for now lmao
#         # self.TabBar.setTabButton(self.TabBar.count()-1, QTabBar.RightSide, switch)


def Exeption_handler(func, *args, silent=False, message=None, **kwargs):
    """this method is just a way to execute a function in the most overprtected way possible
    it wraps in in a try catch and displays a ErrorDialog in case an error occurs

    Args:
        func (func): fucntion to execute
        silent (bool, optional): if True errors will not be raised, just the dialog be shown. Defaults to False.
        message (str, optional): errormessage to show in case the execution fails. Defaults to None.

    Raises:
        e: _description_

    Returns:
        _type_: _description_
    """
    try:
        return True, func(*args, **kwargs)
    except Exception as e:
        if message is not None:
            message = f"{str(e)}\n\n[{message}]"
        else:
            message = str(e)
        error_dialog = QErrorMessage()
        error_dialog.showMessage(message)
        error_dialog.exec()
        if not silent:
            raise e
        return False, message
