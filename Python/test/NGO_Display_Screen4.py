import sys
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6 import QtCore
from PySide6.QtGui import *

class Window(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        outer = QVBoxLayout()
        split = QHBoxLayout()
        left = QFormLayout()
        middle = QFormLayout()
        right = QFormLayout()
        row1 = QFormLayout()
        self.resize(500,300)

        #title
        self.setWindowTitle('Tech For Women')
        title = QLabel('Tech For Women')
        title.setFont(QFont('Times', 12))
        title.setAlignment(QtCore.Qt.AlignCenter)

        #Description
        d = QLabel('Description:')
        font = d.font()
        font.setBold(True)
        d.setFont(font)
        descrip = QLabel('Tech for Women provides technology education, infrastructure, and tools to promote gender equality for girls and women of India')
        descrip.setWordWrap(True)
        # d.setStyleSheet("border: 1px solid black;")
        # descrip.setStyleSheet("border: 1px solid black;")
        row1.addRow(d, descrip)
        #row1.addWidget(descrip)
        row1.setContentsMargins(0,10,0,0)

        s = QLabel("SDG Focus:")
        s.setFont(font)
        scrip = QLabel("5. Gender Equality, Target 5.b, Indicator 5.b.1, Target 4.3, Target 4.4, Target 4.5")
        scrip.setWordWrap(True)
        left.addRow(s, scrip)
        pc = QLabel("Primary Contact:")
        pc.setFont(font)
        pcrip = QLabel("Nivedita Dhutta")
        left.addRow(pc, pcrip)
        phone = QLabel("Phone:")
        phone.setFont(font)
        phcrip = QLabel("+91 5555-123456")
        left.addRow(phone, phcrip)
        em = QLabel("Email:")
        em.setFont(font)
        emcrip = QLabel("ndhutta@techforwomen.org")
        left.addRow(em, emcrip)

        miss = QLabel("Mission:")
        miss.setFont(font)
        mcrip = QLabel("Empower women via technology")
        middle.addRow(miss, mcrip)
        v = QLabel("Vision:")
        v.setFont(font)
        vcrip = QLabel("Use technology to promote gender equality")
        middle.addRow(v, vcrip)
        loc = QLabel("Location:")
        loc.setFont(font)
        locrip = QLabel("Rajnandgaon")
        middle.addRow(loc, locrip)
        web = QLabel("Web Site:")
        web.setFont(font)
        webcrip = QLabel("www.techforwomen.org")
        middle.addRow(web, webcrip)
        reg = QLabel("Registration Number:")
        reg.setFont(font)
        regcrip = QLabel("123971")
        middle.addRow(reg, regcrip)

        p = QLabel("Provides Services in Locations:")
        p.setWordWrap(True)
        p.setFont(font)
        pcrip = QLabel("India")
        right.addRow(p, pcrip)
        b = QLabel("Budget:")
        b.setFont(font)
        bcrip = QLabel("₹800,000")
        right.addRow(b, bcrip)
        c = QLabel("Daan Rating:")
        c.setFont(font)
        ccrip = QLabel("Platimum")
        right.addRow(c, ccrip)
        cp = QLabel("Completed Projects:")
        cp.setFont(font)
        cpcrip = QLabel("WomenForWomen Web Site")
        right.addRow(cp, cpcrip)
        pp = QLabel("Projects in Process:")
        pp.setFont(font)
        ppcrip = QLabel("Cell Service for Women in Crisis")
        right.addRow(pp, ppcrip)
        
        split.addLayout(left)
        split.addLayout(middle)
        split.addLayout(right)

        outer.addWidget(title)
        outer.addLayout(row1)
        outer.addLayout(split)

        self.setLayout(outer)
        
        self.show()

app = QApplication(sys.argv)
# Create and show the form
w = Window()
# Run the main Qt 
sys.exit(app.exec())
