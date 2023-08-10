import sys
from PySide6.QtWidgets import *
from PySide6.QtCore import *

from franz.openrdf.sail.allegrographserver import AllegroGraphServer
from franz.openrdf.repository.repository import Repository
# What is RE?
import re

class Form(QDialog):

    def __init__(self, parent=None):
        super(Form, self).__init__(parent)
        # Create widgets
        self.edit = QLineEdit("")
        self.button = QPushButton("Search FTI")
        # Create layout and add widgets
        layout = QVBoxLayout()
        layout.addWidget(self.edit)
        layout.addWidget(self.button)
        # Set dialog layout
        self.setLayout(layout)
        # Add button signal to greetings slot
        self.triples = []
        self.d = None
        self.button.clicked.connect(self.invokefti)

    def invokefti(self):
        server = AllegroGraphServer('localhost', '10035', 'mdebellis', 'df1559')
        catalog = server.openCatalog('')
        mode = Repository.OPEN
        my_repository = catalog.getRepository('NGO', mode)
        conn = my_repository.getConnection()
        for triple in conn.evalFreeTextSearch(self.edit.text(), index='search'):
            self.triples.append(re.findall('#(.+[^>])', triple[0])[0])
        self.d = Display(self.triples)
        self.close()
        self.d.show()



class Display(QWidget):

    def __init__(self, triples):
        super().__init__()
        layout = QVBoxLayout()
        listWidget = QListWidget()
        for i in triples:
            listWidgetItem = QListWidgetItem(i)
            listWidget.addItem(listWidgetItem)
        layout.addWidget(listWidget)
        self.setFixedSize(640, 480)
        self.setLayout(layout)


# Create the Qt Application
app = QApplication(sys.argv)
# Create and show the form
form = Form()
form.show()
# Run the main Qt
sys.exit(app.exec())

