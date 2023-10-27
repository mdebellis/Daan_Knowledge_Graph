import sys
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6 import QtCore
from PySide6.QtGui import *
from franz.openrdf.connect import ag_connect
from franz.openrdf.vocabulary import RDF

class NGOScreen(QWidget):

    def __init__(self, ngo, parent=None):
        super().__init__(parent)
        outer = QVBoxLayout()
        tempf = QFormLayout()
        self.resize(700,500)
        self.ngo = ngo
        
        
        self.conn = ag_connect('NGO', host='localhost', port='10035',
                               user='test', password='xyzzy')
        self.conn.setNamespace('ngo', 'http://www.semanticweb.org/mdebe/ontologies/NGO#')
        self.conn.setNamespace('rdfs', 'http://www.w3.org/2000/01/rdf-schema#')
        iris = [
                self.conn.createURI('http://www.semanticweb.org/mdebe/ontologies/NGO#orgWebsite'),
                self.conn.createURI('http://www.semanticweb.org/mdebe/ontologies/NGO#email'),
                self.conn.createURI('http://www.semanticweb.org/mdebe/ontologies/NGO#missionStatement'),
                self.conn.createURI('http://www.semanticweb.org/mdebe/ontologies/NGO#objectives'),
                self.conn.createURI('http://www.semanticweb.org/mdebe/ontologies/NGO#chairmanName'),
                self.conn.createURI('http://www.semanticweb.org/mdebe/ontologies/NGO#areasOfOperation'),
                self.conn.createURI('http://www.semanticweb.org/mdebe/ontologies/NGO#mailingAddress'),
                self.conn.createURI('http://www.semanticweb.org/mdebe/ontologies/NGO#state'),
                self.conn.createURI('http://www.semanticweb.org/mdebe/ontologies/NGO#primaryPOC'),
                self.conn.createURI('http://www.semanticweb.org/mdebe/ontologies/NGO#orgType'),
                self.conn.createURI('http://www.semanticweb.org/mdebe/ontologies/NGO#officePhone')]
        n = None
        for i in self.conn.getStatements(self.ngo, RDF.TYPE, self.conn.createURI('http://www.semanticweb.org/mdebe/ontologies/NGO#NGORecipient')):
            n = i[0]    
        if self.ngo != n:
            iris = [
                self.conn.createURI('http://www.semanticweb.org/mdebe/ontologies/NGO#orgWebsite'),
                self.conn.createURI('http://www.semanticweb.org/mdebe/ontologies/NGO#orgEmail'),
                self.conn.createURI('http://www.semanticweb.org/mdebe/ontologies/NGO#dateOfIncorporation'),
                self.conn.createURI('http://www.semanticweb.org/mdebe/ontologies/NGO#class'),
                self.conn.createURI('http://www.semanticweb.org/mdebe/ontologies/NGO#mailingAddress'),
                self.conn.createURI('http://www.semanticweb.org/mdebe/ontologies/NGO#subCategory'),
                self.conn.createURI('http://www.semanticweb.org/mdebe/ontologies/NGO#state'),
            ]
        for iri in range(len(iris)):
            l = '"Not Found"'
            for labelstments in self.conn.getStatements(self.ngo, iris[iri], None):
                l = str(labelstments[2])[1:1001]
            label = QLabel(l[:len(l)-1])
            label.setWordWrap(True)
            if iri ==0:
                label.setText('<a href="' + l + '>' + l[:len(l)-1] + '</a>')
                label.setOpenExternalLinks(True)
                
            if l != '"Not Found"':
                for name in self.conn.getStatements(iris[iri], self.conn.createURI('http://www.w3.org/2004/02/skos/core#prefLabel'), None):
                    n = str(name[2])
                    n1 = QLabel(n[1:len(n)-1] + ':')
                    font = n1.font()
                    font.setBold(True)
                    n1.setFont(font)
                    tempf.addRow(n1, label)


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

        
        outer.addWidget(title)
        outer.addLayout(tempf)
        self.setLayout(outer)
        
        self.show()
