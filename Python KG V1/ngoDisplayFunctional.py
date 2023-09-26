import sys
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6 import QtCore
from PySide6.QtGui import *
from franz.openrdf.connect import ag_connect

class NGOScreen(QWidget):

    def __init__(self, ngo, parent=None):
        super().__init__(parent)
        outer = QVBoxLayout()
        split = QHBoxLayout()
        left = QFormLayout()
        middle = QFormLayout()
        right = QFormLayout()
        row1 = QFormLayout()
        tempf = QFormLayout()
        self.resize(700,500)
        self.ngo = ngo
        
        info = []
        self.conn = ag_connect('NGO', host='localhost', port='10035',
                               user='mdebellis', password='df1559')
        self.conn.setNamespace('ngo', 'http://www.semanticweb.org/mdebe/ontologies/NGO#')
        iris = [
                self.conn.createURI('http://www.semanticweb.org/mdebe/ontologies/NGO#missionStatement'),
                self.conn.createURI('http://www.semanticweb.org/mdebe/ontologies/NGO#objectives'),
                self.conn.createURI('http://www.semanticweb.org/mdebe/ontologies/NGO#chairmanName'),
                self.conn.createURI('http://www.semanticweb.org/mdebe/ontologies/NGO#areasOfOperation'),
                self.conn.createURI('http://www.semanticweb.org/mdebe/ontologies/NGO#email'),
                self.conn.createURI('http://www.semanticweb.org/mdebe/ontologies/NGO#mailingAddress'),
                self.conn.createURI('http://www.semanticweb.org/mdebe/ontologies/NGO#primaryPOC'),
                self.conn.createURI('http://www.semanticweb.org/mdebe/ontologies/NGO#orgWebsite'),
                self.conn.createURI('http://www.semanticweb.org/mdebe/ontologies/NGO#orgType'),
                self.conn.createURI('http://www.semanticweb.org/mdebe/ontologies/NGO#officePhone')]
        for iri in range(len(iris)):
            l = '"Not Found"'
            for labelstments in self.conn.getStatements(self.ngo, iris[iri], None):
                l = str(labelstments[2])
            label = QLabel(l[1:len(l)-1])
            label.setWordWrap(True)
            if l != '"Not Found"':
                for name in self.conn.getStatements(iris[iri], self.conn.createURI('http://www.w3.org/2004/02/skos/core#prefLabel'), None):
                    n = str(name[2])
                    n1 = QLabel(n[1:len(n)-1] + ':')
                    font = n1.font()
                    font.setBold(True)
                    n1.setFont(font)
                    tempf.addRow(n1, label)
                # self.results.addWidget(label, ngorecip + 1, iri)

        #title
        title = None
        for n in self.conn.getStatements(self.ngo, self.conn.createURI('http://www.w3.org/2000/01/rdf-schema#label'), None):
            t = str(n[2])
            label = QLabel(t[1:len(t)-1])
            label.setWordWrap(True)
            self.setWindowTitle(label.text())
            title = label
            title.setFont(QFont('Times', 12))
            title.setAlignment(QtCore.Qt.AlignCenter)
            break

        # #Description
        # d = QLabel('Mission Statement:')
        # font = d.font()
        # font.setBold(True)
        # d.setFont(font)
        # descrip = info[1]
        # descrip.setWordWrap(True)
        # # d.setStyleSheet("border: 1px solid black;")
        # # descrip.setStyleSheet("border: 1px solid black;")
        # row1.addRow(d, descrip)
        # #row1.addWidget(descrip)
        # row1.setContentsMargins(0,10,0,0)

        # s = QLabel("Chairman:")
        # s.setFont(font)
        # scrip = info[2]
        # scrip.setWordWrap(True)
        # left.addRow(s, scrip)
        # pc = QLabel("Area of Operation:")
        # pc.setFont(font)
        # pcrip = info[3]
        # left.addRow(pc, pcrip)
        # phone = QLabel("Office Phone:")
        # phone.setFont(font)
        # phcrip = info[6]
        # left.addRow(phone, phcrip)
        # em = QLabel("Email:")
        # em.setFont(font)
        # emcrip = info[4]
        # left.addRow(em, emcrip)

        # miss = QLabel("Mailing Address")
        # miss.setFont(font)
        # mcrip =info[5]
        
        
        
        
        # split.addLayout(left)
        # split.addLayout(middle)
        # split.addLayout(right)

        # outer.addWidget(title)
        # outer.addLayout(row1)
        # outer.addLayout(split)
        outer.addWidget(title)
        outer.addLayout(tempf)
        self.setLayout(outer)
        
        self.show()

# app = QApplication(sys.argv)
# # Create and show the form
# w = Window()
# # Run the main Qt 
# sys.exit(app.exec())