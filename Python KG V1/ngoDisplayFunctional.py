import sys
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6 import QtCore
from PySide6.QtGui import *
from franz.openrdf.connect import ag_connect
# Must pip install PySide6 before running
# establish connection to repo on line 24

class NGOScreen(QWidget):

    def __init__(self, ngo, parent=None):
        super().__init__(parent)
        outer = QVBoxLayout()
        split = QHBoxLayout()
        left = QFormLayout()
        middle = QFormLayout()
        right = QFormLayout()
        row1 = QFormLayout()
        self.resize(500,300)
        self.ngo = ngo
        
        info = []
        self.conn = ag_connect('enter repo', host='localhost', port='10035',
                               user='xxx', password='xxx')
        self.conn.setNamespace('ngo', 'http://www.semanticweb.org/mdebe/ontologies/NGO#')
        iris = [self.conn.createURI('http://www.w3.org/2000/01/rdf-schema#label'),
                self.conn.createURI('http://www.semanticweb.org/mdebe/ontologies/NGO#missionStatement'),
                self.conn.createURI('http://www.semanticweb.org/mdebe/ontologies/NGO#chairmanName'),
                self.conn.createURI('http://www.semanticweb.org/mdebe/ontologies/NGO#areasOfOperation'),
                self.conn.createURI('http://www.semanticweb.org/mdebe/ontologies/NGO#email'),
                self.conn.createURI('http://www.semanticweb.org/mdebe/ontologies/NGO#mailingAddress'),
                self.conn.createURI('http://www.semanticweb.org/mdebe/ontologies/NGO#officePhone')]
        for iri in range(len(iris)):
                l = '"Not Found"'
                for labelstments in self.conn.getStatements(self.ngo, iris[iri], None):
                    l = str(labelstments[2])
                label = QLabel(l[1:len(l)-1])
                label.setWordWrap(True)
                info.append(label)
                    # self.results.addWidget(label, ngorecip + 1, iri)

        #title
        self.setWindowTitle(info[0].text())
        title = info[0]
        title.setFont(QFont('Times', 12))
        title.setAlignment(QtCore.Qt.AlignCenter)

        #Description
        d = QLabel('Mission Statement:')
        font = d.font()
        font.setBold(True)
        d.setFont(font)
        descrip = info[1]
        descrip.setWordWrap(True)
        # d.setStyleSheet("border: 1px solid black;")
        # descrip.setStyleSheet("border: 1px solid black;")
        row1.addRow(d, descrip)
        #row1.addWidget(descrip)
        row1.setContentsMargins(0,10,0,0)

        s = QLabel("Chairman:")
        s.setFont(font)
        scrip = info[2]
        scrip.setWordWrap(True)
        left.addRow(s, scrip)
        pc = QLabel("Area of Operation:")
        pc.setFont(font)
        pcrip = info[3]
        left.addRow(pc, pcrip)
        phone = QLabel("Office Phone:")
        phone.setFont(font)
        phcrip = info[6]
        left.addRow(phone, phcrip)
        em = QLabel("Email:")
        em.setFont(font)
        emcrip = info[4]
        left.addRow(em, emcrip)

        miss = QLabel("Mailing Address")
        miss.setFont(font)
        mcrip =info[5]
        # middle.addRow(miss, mcrip)
        # v = QLabel("Vision:")
        # v.setFont(font)
        # vcrip = QLabel("Use technology to promote gender equality")
        # middle.addRow(v, vcrip)
        # loc = QLabel("Location:")
        # loc.setFont(font)
        # locrip = QLabel("Rajnandgaon")
        # middle.addRow(loc, locrip)
        # web = QLabel("Web Site:")
        # web.setFont(font)
        # webcrip = QLabel("www.techforwomen.org")
        # middle.addRow(web, webcrip)
        # reg = QLabel("Registration Number:")
        # reg.setFont(font)
        # regcrip = QLabel("123971")
        # middle.addRow(reg, regcrip)

        # p = QLabel("Provides Services in Locations:")
        # p.setWordWrap(True)
        # p.setFont(font)
        # pcrip = QLabel("India")
        # right.addRow(p, pcrip)
        # b = QLabel("Budget:")
        # b.setFont(font)
        # bcrip = QLabel("₹800,000")
        # right.addRow(b, bcrip)
        # c = QLabel("Daan Rating:")
        # c.setFont(font)
        # ccrip = QLabel("Platimum")
        # right.addRow(c, ccrip)
        # cp = QLabel("Completed Projects:")
        # cp.setFont(font)
        # cpcrip = QLabel("WomenForWomen Web Site")
        # right.addRow(cp, cpcrip)
        # pp = QLabel("Projects in Process:")
        # pp.setFont(font)
        # ppcrip = QLabel("Cell Service for Women in Crisis")
        # right.addRow(pp, ppcrip)
        
        split.addLayout(left)
        split.addLayout(middle)
        split.addLayout(right)

        outer.addWidget(title)
        outer.addLayout(row1)
        outer.addLayout(split)

        self.setLayout(outer)
        
        self.show()

# app = QApplication(sys.argv)
# # Create and show the form
# w = Window()
# # Run the main Qt 
# sys.exit(app.exec())