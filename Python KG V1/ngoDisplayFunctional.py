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
        
        
        self.conn = ag_connect('NGO2', host='localhost', port='10035',
                               user='test', password='xyzzy')
        self.conn.setNamespace('ngo', 'http://www.semanticweb.org/mdebe/ontologies/NGO#')
        self.conn.setNamespace('rdfs', 'http://www.w3.org/2000/01/rdf-schema#')
        self.stop_properties = [self.conn.createURI("http://www.w3.org/1999/02/22-rdf-syntax-ns#type"), 
                           self.conn.createURI('http://www.w3.org/2000/01/rdf-schema#label'),
                           self.conn.createURI('http://www.semanticweb.org/mdebe/ontologies/NGO#ngoName'),
                           self.conn.createURI('http://www.semanticweb.org/mdebe/ontologies/NGO#scrapeSource'),
                           self.conn.createURI('http://www.semanticweb.org/mdebe/ontologies/NGO#websiteIsValid')]
        
        finance_properties = [
            self.conn.createURI("http://www.semanticweb.org/mdebe/ontologies/NGO#netWorthFY2015-16"),
            self.conn.createURI("http://www.semanticweb.org/mdebe/ontologies/NGO#netWorthFY2016-17"),
            self.conn.createURI("http://www.semanticweb.org/mdebe/ontologies/NGO#netWorthFY2014-15"),
            self.conn.createURI("http://www.semanticweb.org/mdebe/ontologies/NGO#turnOverFY2014-15"),
            self.conn.createURI("http://www.semanticweb.org/mdebe/ontologies/NGO#netProfitFY2016-17"),
            self.conn.createURI("http://www.semanticweb.org/mdebe/ontologies/NGO#turnOverFY2015-16"),
            self.conn.createURI("http://www.semanticweb.org/mdebe/ontologies/NGO#netProfitFY2014-15"),
            self.conn.createURI("http://www.semanticweb.org/mdebe/ontologies/NGO#paidUpCapital"),
            self.conn.createURI("http://www.semanticweb.org/mdebe/ontologies/NGO#turnOverFY2016-17"),
            self.conn.createURI("http://www.semanticweb.org/mdebe/ontologies/NGO#authorizedCapital"),
            self.conn.createURI("http://www.semanticweb.org/mdebe/ontologies/NGO#netProfitFY2015-16")]
        iris = self.get_instance_values(self.ngo)
        for iri, obj in iris:
            label = None
            if obj == None:
                for labelstments in self.conn.getStatements(self.ngo, iri, None):
                    l = str(labelstments[2])[1:1001]
                    l = l[:len(l)-1]
                    if iri in finance_properties:
                        l = "₹" + l + " (in INR Cr.)"
                label = QLabel(l)
                label.setWordWrap(True)
                
                    
                if iri == self.conn.createURI('http://www.semanticweb.org/mdebe/ontologies/NGO#orgWebsite'):
                    label.setText('<a href="' + l + '>' + l[:len(l)-1] + '</a>')
                    label.setOpenExternalLinks(True)
            else:
                label = QLabel(str(obj)[1:len(str(obj))-1])
                label.setWordWrap(True)
                
            for name in self.conn.getStatements(iri, self.conn.createURI('http://www.w3.org/2000/01/rdf-schema#label'), None):
                n = str(name[2])
                n = n[1:len(n)-1] + ':'
                n1 = QLabel(n.capitalize())
                font = n1.font()
                font.setBold(True)
                n1.setFont(font)
                tempf.addRow(n1, label)
#self.conn.createURI('http://www.w3.org/2004/02/skos/core#prefLabel')
        
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
        
    
    def is_object_prop(self, prop_iri):
        statements = self.conn.getStatements(prop_iri, self.conn.createURI("http://www.w3.org/1999/02/22-rdf-syntax-ns#type"), None)
        for statement in statements:
            if statement[2] == self.conn.createURI("http://www.w3.org/2002/07/owl#ObjectProperty"):
                return True
        return False


    def get_instance_values(self, subject_iri):
        i_statements = self.conn.getStatements(subject_iri, None, None)
        result_statements = []
        for statement in i_statements:
            print(statement[1])
            prop_iri = statement[1]
            lab = None
            if prop_iri not in self.stop_properties:
                if self.is_object_prop(prop_iri):
                    print(1)
                    obj_iri = statement[2]
                    label = self.conn.getStatements(obj_iri, self.conn.createURI('http://www.w3.org/2000/01/rdf-schema#label'), None)
                    for i in label:
                        lab = i[2]
                        print(lab)
                result_statements.append((statement[1], lab))
        return result_statements
