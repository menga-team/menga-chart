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
        """main class for the loginDialog.

        Args:
            username (str, optional): default username. Defaults to "".
            password (str, optional): default password. Defaults to "".
        """
        super().__init__()

        self.creds = {"username": username, "password": password}
        # here we declare a QThread. Basically we need this to reliantly wait for a servers responce without freezing the entire application in the process
        self.thread = QThread()

        # initialize ui
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

        # setup errorlabel
        self.errorLabel.setWordWrap(True)
        
        # setup the domain edit
        self.domainEdit.setEditable(True)
        self.domainEdit.addItems(schools.schools.keys())
        self.domainEdit.setCurrentText(grades.Subject.settings.value(
            "loginDialogDefaultDomain", defaultValue=".digitalesregister.it"))
        # following lines are needed for the cool dropdown that present you all of the diffrent schools you can choose from
        self.domainEdit.textHighlighted.connect(
            lambda x: self.domainEdit.setCurrentText(schools.schools[x]))
        self.domainEdit.textActivated.connect(
            lambda x: self.domainEdit.setCurrentText(schools.schools[x]))

        # setup the username edit
        self.userEdit.setText(self.creds["username"])

        # setup the password edit
        self.passwordEdit.setText(self.creds["password"])
        self.passwordEdit.setEchoMode(QLineEdit.Password)

        # setup the semester spinbox
        self.semesterSpinbox.addItems(("first", "second", "both"))
        self.semesterSpinbox.setCurrentIndex(
            int(grades.Subject.settings.value("loginDialogDefaultSemester", defaultValue=0)))

        # setup the connection testing button
        self.testButton.setText("Test Connection")
        self.testButton.clicked.connect(self.testConnection)

        # setup the button box
        self.button_box.addButton(self.testButton, QDialogButtonBox.ResetRole)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

        # compose the ui
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
        """sets a message with a color to the errorlabel

        Args:
            message (str): message to be displayed
            state (int, optional): state=1 --> set to normal; state=2 --> set to error; state=3 --> set to success; else maintaince the last applied state. Defaults to 0.
        """
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
        """overridden accept method to set a few values efore returning

        Returns:
            _type_: literally "return super().accept()"
        """        
        self.creds["username"] = self.userEdit.text()
        self.creds["password"] = self.passwordEdit.text()
        grades.Subject.settings.setValue(
            "loginDialogDefaultDomain", self.domainEdit.currentText())
        grades.Subject.settings.setValue(
            "loginDialogDefaultSemester", self.semesterSpinbox.currentIndex())
        return super().accept()

    def testConnection(self):
        """tests the connection (obvly threaded)
        """
        # check if the htread is running and stop it if trrue
        if self.thread.isRunning():
            self.thread.quit()
        self.thread.run = self.requestThread
        self.thread.start()
        # utils.Exeption_handler()

    def requestThread(self):
        """method that actuaslly connects with the servers etc. Please dont from ruinning this unthreaded
        """
        # remove unnecessary "https://" from the domain and textedit
        text = self.domainEdit.currentText()
        text.replace("https://", "")
        self.domainEdit.setCurrentText(text)
        try:
            # setup the request data
            url = f"https://{self.domainEdit.currentText()}/v2/api/auth/login"
            data = {"username": self.userEdit.text(
            ), "password": self.passwordEdit.text()}
            self.setMessage("sending Request", state=1)
            # post the request
            resp = requests.post(url, json=data)
            print(resp.json())
            # if there was an error serverside (cookies expired, user not found, wrong password etc) the server will return a json with the error message, wich we then display
            if resp.json()["error"] is not None:
                self.setMessage(
                    f"Auth failed. Server responce: " + str(resp.json()), state=2)
            else:
                # in this case the authentication was a success
                self.setMessage(f"Auth Successfull!", state=3)
        except Exception as e:
            # in case the request itself failed (no connection, wrong paranmeters, wrong server etc)
            self.setMessage(f"Request failed: " + str(e), state=2)

    @staticmethod
    def getCredentials(*args, **kwargs):
        """convenience method that declared a loginDialog and starts it 

        Returns:
            tuple: (exit codes, dict with credentials)
        """
        d = loginDialog(*args, **kwargs)
        return d.exec(), d.creds
