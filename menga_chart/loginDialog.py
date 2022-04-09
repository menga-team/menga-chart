from PyQt5 import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

import requests

try:
    import grades
    import schools
except ImportError:
    from menga_chart import grades
    from menga_chart import schools


class loginDialog(QDialog):
    def __init__(self, username="", password=""):
        super().__init__()

        self.creds = {"username": username, "password": password}
        self.thread = QThread()

        self.layout = QGridLayout()
        self.errorLabel = QLabel()
        self.domainEdit = QComboBox()
        self.userEdit = QLineEdit()
        self.passwordEdit = QLineEdit()
        self.testButton = QPushButton()
        self.semesterSpinbox = QComboBox()
        self.testButton = QPushButton()
        self.button_box = QDialogButtonBox(
            QDialogButtonBox.Cancel | QDialogButtonBox.Ok)

        self.errorLabel.setWordWrap(True)

        self.domainEdit.setEditable(True)
        self.domainEdit.addItems(schools.schools.keys())
        self.domainEdit.setCurrentText(grades.Subject.settings.value(
            "loginDialogDefaultDomain", defaultValue=".digitalesregister.it"))
        self.domainEdit.textHighlighted.connect(
            lambda x: self.domainEdit.setCurrentText(schools.schools[x]))
        self.domainEdit.textActivated.connect(
            lambda x: self.domainEdit.setCurrentText(schools.schools[x]))

        self.userEdit.setText(self.creds["username"])

        self.passwordEdit.setText(self.creds["password"])
        self.passwordEdit.setEchoMode(QLineEdit.Password)

        self.semesterSpinbox.addItems(("first", "second", "both"))
        self.semesterSpinbox.setCurrentIndex(
            int(grades.Subject.settings.value("loginDialogDefaultSemester", defaultValue=0)))

        self.testButton.setText("Test Connection")
        self.testButton.clicked.connect(self.testConnection)

        self.button_box.addButton(self.testButton, QDialogButtonBox.ResetRole)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

        self.layout.addWidget(QLabel("domain: "), 0, 0)
        self.layout.addWidget(self.domainEdit, 0, 1)
        self.layout.addWidget(QLabel("username: "), 1, 0)
        self.layout.addWidget(self.userEdit, 1, 1)
        self.layout.addWidget(QLabel("password: "), 2, 0)
        self.layout.addWidget(self.passwordEdit, 2, 1)
        self.layout.addWidget(QLabel("semester: "), 3, 0)
        self.layout.addWidget(self.semesterSpinbox, 3, 1)
        self.layout.addWidget(self.errorLabel, 4, 0, 1, 2)
        self.layout.addWidget(self.button_box, 5, 0, 1, 2)

        self.setWindowTitle("Login")
        self.setLayout(self.layout)

    def setMessage(self, message, state=0):
        p = QPalette()
        if state == 1:
            p.setColor(QPalette.WindowText,
                       self.palette().windowText().color())
        if state == 2:
            p.setColor(QPalette.WindowText, Qt.red)
        if state == 3:
            p.setColor(QPalette.WindowText, Qt.green)
        self.errorLabel.setPalette(p)
        self.errorLabel.setText(message)

    def accept(self) -> None:
        self.creds["username"] = self.userEdit.text()
        self.creds["password"] = self.passwordEdit.text()
        grades.Subject.settings.setValue(
            "loginDialogDefaultDomain", self.domainEdit.currentText())
        grades.Subject.settings.setValue(
            "loginDialogDefaultSemester", self.semesterSpinbox.currentIndex())
        return super().accept()

    def testConnection(self):
        if self.thread.isRunning():
            self.thread.quit()
        self.thread.run = self.requestThread
        self.thread.start()
        # utils.Exeption_handler()

    def requestThread(self):
        text = self.domainEdit.currentText()
        text.replace("https://", "")
        self.domainEdit.setCurrentText(text)
        try:
            url = f"https://{self.domainEdit.currentText()}/v2/api/auth/login"
            data = {"username": self.userEdit.text(
            ), "password": self.passwordEdit.text()}
            self.setMessage("sending Request", state=1)
            resp = requests.post(url, json=data)
            print(resp.json())
            if resp.json()["error"] is not None:
                self.setMessage(
                    f"Auth failed. Server responce: " + str(resp.json()), state=2)
            else:
                self.setMessage(f"Auth Successfull!", state=3)
        except Exception as e:
            self.setMessage(f"Request failed: " + str(e), state=2)

    @staticmethod
    def getCredentials(*args, **kwargs):
        d = loginDialog(*args, **kwargs)
        return d.exec(), d.creds
