from PyQt5 import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

import random

try:
    import __init__ as menga_chart
except:
    import menga_chart


class aboutDialog(QDialog):
    """main class for the "about" dialooooooog that displays some information on the author etc.

    Args:
        QDialog (_type_): self
    """
    def __init__(self):
        super().__init__()
        
        # initialize layout and buttonbox
        self.layout = QVBoxLayout()
        self.button_box = QDialogButtonBox(QDialogButtonBox.Ok)
        
        # check if authors is already a list else convert it to one
        if not isinstance(menga_chart.author, list):
            menga_chart.author = [menga_chart.author]
        
        
        # initialize the Textbox
        self.text_edit = QTextEdit()
        self.res = f'<p align="center">wow script by penisspan</p>'
        self.text_edit.setText(
        f"""
<p align="center">Authors: {str(menga_chart.author)[1:-1]}</p>
<p align="center">
Of course it would be unfair not to include all of the support 
other menga-team members have given us duriong the development 
process. Here are a few friends, colleagues, etc that helped us 
the most and without whom this application would have been 
compleatly impossible. Hope it doesent get to repetitive.
</p>
<p align="center">🬜🬪🬜🬪🬜🬪🬜🬪🬜🬪🬜🬪</p>
        """
            )
        self.text_edit.setReadOnly(True)
        self.text_edit.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.text_edit.verticalScrollBar().valueChanged.connect(self.addAuthor)
        # add a few enrie so the user can already scroll down and trigger the system
        for _ in range(20):
            self.addAuthor()
        
        label = QLabel(
            f"""
<head>
    <meta charset="utf-8" />
    <meta name="generator" content="pandoc" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=yes" />
</head>

<body>
    <section id="menga-chart" class="level2">
        <h2>{menga_chart.name}</h2>
        <p><sub><em>{menga_chart.version}</em></sub></p>
        <p><strong>Application for displaying and editing school grade stats</strong></p>
        <p>Contact us: </p>
        <ul>
            <li><a href="https://github.com/menga-tema/menga0chart">website</a>: https://github.com/menga-tema/menga</li>
            <li><a href="{menga_chart.email}">email</a>: {menga_chart.email}</li>
            <li>shouting (very hard)</li>
        </ul>
        <p>Copyright © 2022 menga-team;</p>
        <p><em>Permission is hereby granted, free of charge, to any person obtaining a copy of this software and
                associated documentation files (the “Software”), to deal in the Software without restriction, including
                without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
                copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the
                following conditions:</em></p>
        <p>The above copyright notice and this permission notice shall be included in all copies or substantial portions
            of the Software.</p>
        <p><strong>THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT
                LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN
                NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
                WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
                SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.</strong></p>
        <p>important credits:</p>
    </section>
</body>

</html>

        """
        )
        label.setWordWrap(True)
        
        # assemble the ui
        self.layout.addWidget(label)
        self.layout.addWidget(self.text_edit)

        self.button_box.accepted.connect(self.accept)

        self.setWindowTitle("About")
        self.setLayout(self.layout)
    
    def addAuthor(self):
        """adds a entry to the textbox after checking if the vertical scrollbar has scrolled enough and pushing it up again by 10 pixel to avoid lag
        """
        if self.text_edit.verticalScrollBar().value() > self.text_edit.verticalScrollBar().maximum() - 1:
            # push the scrollbar up to avoid causing lag
            self.text_edit.verticalScrollBar().setValue(self.text_edit.verticalScrollBar().value() - 10)
            
            # here we combine the prefix and title in a thanks frase to then be added as an aentry in the textbox
            preFixes = ["chief", "supreme", "royal", "very skilled", "excellent", "(we miss u)", "bossy", "only", "handsome", "verified", "temporary", "very rich", "most successfull", "very helpfull", "very based", "inevitable", "surprise", "forgotten", "senior", "junior", "analitical", "2 year old", "magic", "imaginary", "explosive", "american", "british", "sussy", "italian", "chinese", "professional", "japanese", "gaming", "financial", "very needed", "helper"]
            titles = ["executeve", "boss", "barman", "homless", "branch developer", "main developer", "backend developer", "fronend developer", "fullstack developer", "project manager", "manager", "duce of scily", "emperor", "leader", "president", "representative", "prime minister", "price", "son", "secretary", "excel expert", "fortnite player", "emotional support", "doomer", "social media expert", "amogus", "fund manager", "artist", "designer", "painter", "king", "only hope left", "cat", "foor cleaner robot", "manufactor", "tech support", "vacationer", "human rights expert", "linux god", "security guard", "body guard", "general", "commander", "liutenant", "tester", "user", "criticist", "debugger", "dependecy manager", "wizard", "shamman", "priest", "dragon slayer"]
            
            # 50% percent of the time a prefix is added
            prefix = random.choice(preFixes) if random.randint(0, 1) else ""  
            title = random.choice(titles)
            author = random.choice(menga_chart.author)
            
            content = f"big thx to our <strong>{prefix} {title}</strong> a.k.a <strong>{author}</strong>"
            # occasionally convert it to "amogus"
            if random.randint(0, 75) == 75:
                content = "amogus"
            
            # append the entry
            self.text_edit.append(content)
        

    @staticmethod
    def displayDialog():
        """conviniency function that declares a aboutDialog() and starts it
        """
        d = aboutDialog()
        d.exec()