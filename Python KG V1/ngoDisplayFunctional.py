import sys
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6 import QtCore
from PySide6.QtGui import *
from franz.openrdf.connect import ag_connect
from franz.openrdf.vocabulary import RDF
import webbrowser

class NGOScreen(QWidget):

    def __init__(self, ngo, parent=None):
        super().__init__(parent)
        outer = QVBoxLayout()
        infoHolder = QFormLayout()
        self.resize(700,500)
        self.ngo = ngo
        
        
        self.conn = ag_connect('NGO', host='localhost', port='10035',
                               user='mdebellis', password='df1559')
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
                statements = self.conn.getStatements(self.ngo, iri, None)
                with statements:
                    for labelstments in statements:
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
                
            states = self.conn.getStatements(iri, self.conn.createURI('http://www.w3.org/2000/01/rdf-schema#label'), None)
            with states:
                for name in states:
                    n = str(name[2])
                    n = n[1:len(n)-1] + ':'
                    n1 = QLabel(n.capitalize())
                    font = n1.font()
                    font.setBold(True)
                    n1.setFont(font)
                    infoHolder.addRow(n1, label)
#self.conn.createURI('http://www.w3.org/2004/02/skos/core#prefLabel')
        
        title = None
        state = self.conn.getStatements(self.ngo, self.conn.createURI('http://www.w3.org/2000/01/rdf-schema#label'), None)
        with state:
            for n in state:
                t = str(n[2])
                label = QLabel(t[1:len(t)-1])
                label.setWordWrap(True)
                self.setWindowTitle(label.text())
                title = label
                title.setFont(QFont('Times', 12))
                title.setAlignment(QtCore.Qt.AlignCenter)
                break     
        
        botbuttons = QHBoxLayout()
        doneB = QPushButton("Done")
        doneB.clicked.connect(self.exit)
        contactB = QPushButton("Contact")
        contactB.clicked.connect(self.mail)
        rfpB = QPushButton('Send RFP')
        rfpB.clicked.connect(self.rfpmail)
        n = None
        stats = self.conn.getStatements(self.ngo, RDF.TYPE, self.conn.createURI('http://www.semanticweb.org/mdebe/ontologies/NGO#NGORecipient'))
        with stats:
            for i in stats:
                n = i[0]   
        if self.ngo != n:
            rfpB.setDisabled(True)
        else:
            rfpB.setDisabled(False)
        botbuttons.addWidget(doneB)
        botbuttons.addWidget(contactB)
        botbuttons.addWidget(rfpB)
        
        scroll = QScrollArea()
        widget = QWidget()
        widget.setLayout(infoHolder)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        scroll.setWidgetResizable(True)
        scroll.setWidget(widget)
        
        outer.addWidget(title)
        outer.addWidget(scroll)
        outer.addLayout(botbuttons)
        
        self.setLayout(outer)
        
        self.show()
        
    def exit(self):
        self.close()
        a = NGOScreen(self.ngo)
        
    def mail(self):
        m = 1
        stat = self.conn.getStatements(self.ngo, self.conn.createURI('http://www.semanticweb.org/mdebe/ontologies/NGO#orgEmail'), None)
        with stat:
            for emailtriple in stat:
                email = str(emailtriple[2])[1:len(str(emailtriple[2]))-1]
                webbrowser.open("mailto:?to="+email.lower(), new=1)
                m = 0
        if m:
            webbrowser.open("mailto:?to=No Email Found", new=1)
            
    def rfpmail(self):
        rfp_current_funder = "UN Women Organization"
        rfp_topic = "Strengthening ecosystem for gender equality: Prevention and Response to Gender based Violence in Goa, India"
        rfp_url = "https://ngobox.org/full_rfp_eoi_RFP---Strengthening-ecosystem-for-gender-equality--Prevention-and-Response-to-Gender-based-Violence-in-Goa,-India-UN-Women-_15842"
        primaryContact = 'NGO'
        sta = self.conn.getStatements(self.ngo, self.conn.createURI('http://www.w3.org/2000/01/rdf-schema#label'), None)
        with sta:
            for cont in sta:
                primaryContact = str(cont[2])[1:len(str(cont[2]))-1]
        st = self.conn.getStatements(self.ngo, self.conn.createURI('<http://www.semanticweb.org/mdebe/ontologies/NGO#primaryPoc>'), None)        
        with st:
            for cont in st:
                primaryContact = str(cont[2])[1:len(str(cont[2]))-1]
            
        m = 1
        l = "English"
        s1 = self.conn.getStatements(self.ngo, self.conn.createURI('<http://www.semanticweb.org/mdebe/ontologies/NGO#preferredLanguage>'), None)
        with s1:   
            for lang in s1:
                l = str(lang[2])[1:len(str(lang[2]))-1]
        body = "Dear " + primaryContact + ", %0D%0A%0D%0AI represent the " + rfp_current_funder + ". We have an RFP for "  + rfp_topic + " that I believe you may be qualified for. Please visit the following page to see the RFP and instructions for how to reply if you are interested: " + rfp_url + " If you have questions you can reply to this email or reach me at: +1 (415) 555-5555.%0D%0A%0D%0ASincerely,%0D%0AMichael DeBellis%0D%0A+1 (415) 555-5555%0D%0AUN Women%0D%0Ahttps://www.unwomen.org/ "
        if l == "Hindi":
            body = "प्रिय " + primaryContact + ", %0D%0A%0D%0Aमैं प्रतिनिधित्व करता हूं" + rfp_current_funder +  ". हमारे पास इसके लिए एक आरएफपी है "  + rfp_topic + " मुझे विश्वास है कि आप इसके लिए योग्य हो सकते हैं।. यदि आप रुचि रखते हैं तो कृपया आरएफपी और उत्तर देने के निर्देश देखने के लिए निम्नलिखित पृष्ठ पर जाएँ:  " + rfp_url + "  यदि आपके कोई प्रश्न हैं तो आप इस ईमेल का उत्तर दे सकते हैं या मुझसे यहां संपर्क कर सकते हैं: <Current User Phone>. %0D%0A%0D%0Aईमानदारी से,%0D%0A<Current User>%0D%0A<Current User Phone>%0D%0A<Current Funder Name and Address>"
        s2 = self.conn.getStatements(self.ngo, self.conn.createURI('http://www.semanticweb.org/mdebe/ontologies/NGO#orgEmail'), None)
        with s2:
            for emailtriple in s2:
                email = str(emailtriple[2])[1:len(str(emailtriple[2]))-1]
                webbrowser.open("mailto:?to="+email.lower()+"&subject=RFP&body="+body, new=1)
                m = 0
        if m:
            webbrowser.open("mailto:?to=No Email Found", new=1)
            
    def is_object_prop(self, prop_iri):
        statements = self.conn.getStatements(prop_iri, self.conn.createURI("http://www.w3.org/1999/02/22-rdf-syntax-ns#type"), None)
        with statements:
            for statement in statements:
                if statement[2] == self.conn.createURI("http://www.w3.org/2002/07/owl#ObjectProperty"):
                    return True
        return False


    def get_instance_values(self, subject_iri):
        i_statements = self.conn.getStatements(subject_iri, None, None)
        result_statements = []
        with i_statements:
            for statement in i_statements:
                # print(statement[1])
                prop_iri = statement[1]
                lab = None
                if prop_iri not in self.stop_properties:
                    if self.is_object_prop(prop_iri):
                        # print(1)
                        obj_iri = statement[2]
                        label = self.conn.getStatements(obj_iri, self.conn.createURI('http://www.w3.org/2000/01/rdf-schema#label'), None)
                        with label:
                            for i in label:
                                lab = i[2]
                                # print(lab)
                    result_statements.append((statement[1], lab))
        return result_statements
