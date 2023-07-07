import sys
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
from franz.openrdf.connect import ag_connect
from ngoDisplayFunctional import NGOScreen
from functools import partial
from franz.openrdf.vocabulary import RDF
from franz.openrdf.query.query import QueryLanguage
import re


class Window(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.conn = ag_connect('minitest', host='localhost', port='10035',
                               user='test', password='xyzzy')
        self.conn.setNamespace('ngo', 'http://www.semanticweb.org/mdebe/ontologies/NGO#')
        self.setWindowTitle('NGO Search')
        self.vert = QVBoxLayout()  # general outer layout
        self.inputs = QFormLayout()  # format for entering in the rest of data
        self.row1 = QHBoxLayout()  # format for location row row
        self.row2 = QHBoxLayout()  # format for sdgs row
        self.rowbottom = QHBoxLayout()  # layout for the bottom row buttons (search, reset, done)
        self.orgTypes = []
        self.results = QGridLayout()  # layout to show results
        self.t = None  # instance to call sdg tree class
        self.sdgs = []  # list to track all sdgs selected, this is needed for reselection(hold an instance to delete)
        self.resultList = []  # list of ngo IRIs from query
        self.allResults = []  # list of every ngo's characteristics, needed for re searching(hold an instance to delete)
        self.resultsbuttons = []  # list of buttons to link results to ngo pages
        self.ngoScreen = None
        self.sdgIRI = {}
        self.resize(900, 800)

        self.n = 10
        self.nums = QLabel('Results: (Showing ' + str(self.n) + ' of 300,000)')
        
        self.statedrop = QComboBox()
        self.statedrop.addItems(["Select", "Andhra Pradesh","Arunachal Pradesh","Assam","Bihar","Chhattisgarh","Goa","Gujarat","Haryana",
                                 "Himachal Pradesh","Jharkhand","Karnataka","Kerala","Maharashtra","Madhya Pradesh","Manipur",
                                 "Meghalaya","Mizoram","Nagaland","Odisha","Punjab","Rajasthan","Sikkim","Tamil Nadu","Tripura",
                                 "Telangana","Uttar Pradesh","Uttarakhand","West Bengal","Andaman & Nicobar","Chandigarh",
                                 "Dadra & Nagar Haveli and Daman & Diu","Delhi","Jammu & Kashmir","Ladakh","Lakshadweep","Puducherry (UT)"])

        self.row1.addWidget(self.statedrop)
        # self.row1.addWidget(self.locationEdit)

        self.scroll = QScrollArea()  # Scroll Area which contains the widgets, set as the centralWidget
        self.widget = QWidget()  # Widget that contains the collection of Vertical Box
        self.vbox = QVBoxLayout()
        self.sdgItem = QLabel("All")
        self.sdgs.append(self.sdgItem)
        self.vbox.addWidget(self.sdgItem)
        self.widget.setLayout(self.vbox)
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(self.widget)
        self.row2.addWidget(self.scroll)
        self.sdgEdit = QPushButton("Edit SDGs")
        self.sdgEdit.clicked.connect(self.sdgtree)
        self.row2.addWidget(self.sdgEdit)

        self.check1 = QCheckBox('Cooperative Society')
        self.check2 = QCheckBox('Academic Institutions (Private)')
        self.check3 = QCheckBox('Other Registered Entities (Non-Government)')
        self.check4 = QCheckBox('Private Sector Companies (Sec 8/25)')
        self.check5 = QCheckBox('Trust (Non-Government)')
        self.check6 = QCheckBox('Registered Societies (Non-Government)')
        self.check1.setChecked(True)
        self.check2.setChecked(True)
        self.check3.setChecked(True)
        self.check4.setChecked(True)
        self.check5.setChecked(True)
        self.check6.setChecked(True)
        self.horz = QHBoxLayout()
        self.horz.addWidget(self.check1)
        self.horz.addWidget(self.check2)
        self.horz.addWidget(self.check3)
        self.horz.addWidget(self.check4)
        self.horz.addWidget(self.check5)
        self.horz.addWidget(self.check6)

        self.minf = QLineEdit()
        self.minf.setPlaceholderText("₹0")  # no input this returns empty string not 0
        self.maxf = QLineEdit()
        self.maxf.setPlaceholderText("no limit")

        self.textS = QLineEdit()

        self.maxnumsearch = QLineEdit()
        self.maxnumsearch.setPlaceholderText("10")

        self.inputs.addRow(QLabel('Locations:'), self.row1)
        self.inputs.addRow(QLabel('SDGs:'), self.row2)
        self.inputs.addRow(QLabel('Organization Type:'), self.horz)
        self.inputs.addRow(QLabel('Minimum Annual Budget:'), self.minf)
        self.inputs.addRow(QLabel('Maximum Annual Budget:'), self.maxf)
        self.inputs.addRow(QLabel('Text Search:'), self.textS)
        self.inputs.addRow(QLabel('Maximum Number of NGOs:'), self.maxnumsearch)

        searchB = QPushButton("Search")
        searchB.clicked.connect(self.doQuery)
        resetB = QPushButton("Reset Search")
        resetB.clicked.connect(self.reset)
        doneB = QPushButton("Done")
        doneB.clicked.connect(self.exit)

        self.rowbottom.addWidget(searchB)
        self.rowbottom.addWidget(resetB)
        self.rowbottom.addWidget(doneB)

        # results grid
        self.setResults()

        self.scroll2 = QScrollArea()  # Scroll Area which contains the widgets, set as the centralWidget
        self.widget2 = QWidget()  # Widget that contains the collection of Vertical Box
        self.widget2.setLayout(self.results)
        self.scroll2.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll2.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll2.setWidgetResizable(True)
        self.scroll2.setWidget(self.widget2)

        self.vert.addLayout(self.inputs)
        
        self.vert.addWidget(self.nums)
        self.vert.addWidget(self.scroll2)
        self.vert.addLayout(self.rowbottom)

        self.setLayout(self.vert)
        self.show()

    def sdgtree(self): # function to display tree
        self.t = Tree()
        self.t.show()

    def setSDG(self, a, irimapper): # display sdgs selected in sdgtree
        for i in self.sdgs:
            i.deleteLater()
        self.sdgs.clear()

        for i in range(len(a)):
            self.sdgs.append(QLabel(a[i]))
            self.vbox.addWidget(self.sdgs[i])
        self.sdgIRI = irimapper
        self.t.close()
    
    def get_name_from_iri(self, iri):
        iri_str = str(iri)
        iri_str = iri_str.replace('<', '')
        iri_str = iri_str.replace('>', '')
        if iri_str.startswith('http://www.semanticweb.org/mdebe/ontologies/NGO#'):
            iri_str = iri_str.replace('http://www.semanticweb.org/mdebe/ontologies/NGO#','ngo:')
        elif iri_str.startswith('http://www.semanticweb.org/mdebe/ontologies/2022/10/UNSDG#'):
            iri_str = iri_str.replace('http://www.semanticweb.org/mdebe/ontologies/2022/10/UNSDG#', 'sdg:')
        return iri_str

    def generateQuery(self, sdgs=[], maxBudget = None, minBudget = None, location ="",orgTypeList = [], qlimit ="20"):
        qstring = "SELECT * WHERE {?ngoRecipient a ngo:NGORecipient. "
        org_type_test_string = "?ngoRecipient ngo:orgType ?orgType."
        org_type_query_string = ""
        i = 0
        if maxBudget != None:
            mbstring = " ?ngoRecipient ngo:avgMonthlyExpenditure ?avm. Filter(?avm < " + str(maxBudget) + ")"
            qstring = qstring + mbstring
        if minBudget != None:
            mbstring = " ?ngoRecipient ngo:avgMonthlyExpenditure ?avm. Filter(?avm > " + str(minBudget) + ")"
            qstring = qstring + mbstring
        if location != "":
            locstring = " ?ngoRecipient ngo:state ?state. filter(?state = \"" + location + "\")"
            qstring = qstring + locstring
        if location != "":
            locstring = " ?ngoRecipient ngo:state ?state. filter(?state = \"" + location + "\")"
            qstring = qstring + locstring
        for orgType in orgTypeList:
            org_type_query_string = org_type_query_string + "|| ?orgType =  \"" + orgType + "\" "
        if orgTypeList !=[]:
            org_type_query_string = org_type_test_string + " Filter(" + org_type_query_string[3:] + ")"
            qstring = qstring + org_type_query_string
        for sdg in sdgs:
            sdgname = self.get_name_from_iri(sdg)
            sdg_test_string = " ?ngoRecipient ngo:hasSDGGoal " + sdgname + ". "
            qstring = qstring + sdg_test_string
        qstring = qstring + "} LIMIT " + qlimit
        return qstring




    def query(self,sdgs=[], maxBudget = None, minBudget = None, location ="", orgTypeList = [], qlimit ="20"):
        query_string = self.generateQuery(sdgs, maxBudget, minBudget, location, orgTypeList, qlimit)
        tuple_query = self.conn.prepareTupleQuery(QueryLanguage.SPARQL, query_string)
        result = tuple_query.evaluate()
        ngor_list = []
        with result:
            for binding_set in result:
                ngor = binding_set.getValue("ngoRecipient")
                ngor_list.append(ngor)
        return ngor_list
    
    def doQuery(self): #produces a set of results
        self.orgTypes = []
        if self.check1.isChecked():
            self.orgTypes.append(self.check1.text())
        if self.check2.isChecked():
            self.orgTypes.append(self.check2.text())
        if self.check3.isChecked():
            self.orgTypes.append(self.check3.text())
        if self.check4.isChecked():
            self.orgTypes.append(self.check4.text())
        if self.check5.isChecked():
            self.orgTypes.append(self.check5.text())
        if self.check6.isChecked():
            self.orgTypes.append(self.check6.text())
        if self.statedrop.currentText() == 'Select':
            loc = ''
        else:
            loc = self.statedrop.currentText()
        if self.maxf.text() == '':
            maxbudget = None
        else:
            maxbudget = int(self.maxf.text())
        if self.minf.text() == '':
            minbudget = None
        else:
            minbudget = int(self.minf.text())
        if self.maxnumsearch.text() == '':
            src = '10'
        else:
            src = self.maxnumsearch.text()
        #textsearch = self.textS.text() look at this later
        sdglist = []
        for s in self.sdgs:
            if s.text() == 'All':
                break
            sdglist.append(self.sdgIRI[s.text()])

        self.resultList = self.query(sdgs=sdglist, maxBudget = maxbudget, minBudget = minbudget, 
                                     location =loc, orgTypeList = self.orgTypes, qlimit = src)
        
        iris = [self.conn.createURI('http://www.w3.org/2000/01/rdf-schema#label'),
                self.conn.createURI('http://www.semanticweb.org/mdebe/ontologies/NGO#objectives'),
                self.conn.createURI('http://www.semanticweb.org/mdebe/ontologies/NGO#hasSDGGoal'),
                self.conn.createURI('http://www.semanticweb.org/mdebe/ontologies/NGO#state'),
                self.conn.createURI('http://www.semanticweb.org/mdebe/ontologies/NGO#totalIncome'),
                self.conn.createURI('http://www.semanticweb.org/mdebe/ontologies/NGO#orgType')]
        
        for param in self.allResults:
            param.deleteLater()
            self.results.removeWidget(param)
        self.allResults = [] # tracks every parameter entered into results to be deleted on new search
        if self.maxnumsearch.text() == '':
            maxs = 10
        else:
            maxs = int(self.maxnumsearch.text())
        
        for ngorecip in range(0, min(maxs, len(self.resultList))): #adds all parameters of specified number of ngos into display
            for iri in range(len(iris)):
                for labelstments in self.conn.getStatements(self.resultList[ngorecip], iris[iri], None):
                    l = str(labelstments[2])
                    label = QLabel(l[1:len(l)-1])
                    label.setWordWrap(True)
                    self.allResults.append(label)
                    self.results.addWidget(label, ngorecip + 1, iri)
        self.resultsbuttons = []
        
        for i in range(0, min(maxs, len(self.resultList))): #adds all buttons into results display
            self.resultsbuttons.append(QPushButton('See NGO'))
            self.results.addWidget(self.resultsbuttons[i], i + 1, 6)
            self.resultsbuttons[i].clicked.connect(partial(self.getNGOScreen, self.resultList[i]))
        
        self.nums.setText('Results: (Showing ' + str(maxs) + ' of 300,000)')
        
        
    def getNGOScreen(self, ngo): # function to call last specific ngo screen
        self.ngoScreen = NGOScreen(ngo)
        

    def setResults(self):  # set the labels for formatting the results, should only be called once

        name1 = QLabel('NGO Name')
        font = name1.font()
        font.setBold(True)
        name1.setFont(font)
        self.results.addWidget(name1, 0, 0)
        name2 = QLabel('NGO Objective')
        name2.setFont(font)
        self.results.addWidget(name2, 0, 1)
        name3 = QLabel('SDG Focus')
        name3.setFont(font)
        self.results.addWidget(name3, 0, 2)
        name4 = QLabel('Provides Services in Locations')
        name4.setFont(font)
        self.results.addWidget(name4, 0, 3)
        name5 = QLabel('Annual Budget')
        name5.setFont(font)
        self.results.addWidget(name5, 0, 4)
        name6 = QLabel('Organization Type')
        name6.setFont(font)
        self.results.addWidget(name6, 0, 5)

        self.doQuery()

    def reset(self): # resets all inputs
        self.statedrop.setCurrentText('Select')
        self.minf.clear()
        self.maxf.clear()
        self.textS.clear()
        self.maxnumsearch.clear()
        for i in self.sdgs:
            i.deleteLater()
        self.sdgs.clear()
        self.sdgs.append(QLabel('All'))
        self.vbox.addWidget(self.sdgs[0])
        self.doQuery() # when all parameters are reset, a base set of results will be displayed
        self.nums = QLabel('Results: (Showing ' + str(self.n) + ' of 300,000)')
    
    def exit(self):
        self.close()


class Tree(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle('Select SDG(s)')
        self.tree = QTreeWidget()
        self.tree.setColumnCount(1)
        self.tree.setHeaderLabels(["United Nations Sustainable Development Goals, Targets, Indicators"])
        self.selects = []
        items = []
        self.irimapper = {}
        conn = ag_connect('minitest', host='localhost', port='10035',
                               user='test', password='xyzzy')
        conn.setNamespace('ngo', 'http://www.semanticweb.org/mdebe/ontologies/NGO#')
        sdg_class = conn.createURI('http://www.semanticweb.org/mdebe/ontologies/2022/10/UNSDG#SDGGoal')
        targetIRI = conn.createURI('http://www.semanticweb.org/mdebe/ontologies/2022/10/UNSDG#hasTarget')
        indicatorIRI = conn.createURI('http://www.semanticweb.org/mdebe/ontologies/2022/10/UNSDG#hasIndicator')
        descriptionIRI = conn.createURI('http://www.semanticweb.org/mdebe/ontologies/2022/10/UNSDG#goalDescription')
        indicatorDesc = conn.createURI('http://www.semanticweb.org/mdebe/ontologies/2022/10/UNSDG#indicatorDescription')
        l1 = []
        for sdg in conn.getStatements(None, RDF.TYPE, sdg_class):
            for descrip in conn.getStatements(sdg[0], descriptionIRI, None): #should only iterate once
                sdgLabel = str(descrip[2])[1:len(str(descrip[2]))-1]
                self.irimapper[sdgLabel] = sdg[0]
                l1.append(sdgLabel)
        l1.sort(key=lambda x: int(re.findall("\s(\d+)\.",x)[0]))
        for sd in l1:
            item = QTreeWidgetItem([sd])
            l2 = []
            for target in conn.getStatements(self.irimapper[sd], targetIRI, None):
                for tcrip in conn.getStatements(target[2], descriptionIRI, None): #should only iterate once
                    targetLabel = str(tcrip[2])[1:len(str(tcrip[2]))-1]
                    self.irimapper[targetLabel] = target[2]
                    l2.append(targetLabel)
            l2.sort(key=lambda x: int((re.findall("\.(.+?)\s",x)[0])) if re.findall("\.(.+?)\s",x)[0].isnumeric() else ord((re.findall("\.(.+?)\s",x)[0])))
            for t in l2:
                child1 = QTreeWidgetItem([t])
                item.addChild(child1)
                l3 = []
                for indicator in conn.getStatements(self.irimapper[t], indicatorIRI, None):
                    for icrip in conn.getStatements(indicator[2], indicatorDesc, None): #should only iterate once
                        indicatorLabel = str(icrip[2])[1:len(str(icrip[2]))-1]
                        self.irimapper[indicatorLabel] = indicator[2]
                        l3.append(indicatorLabel)
                l3.sort()
                for i in l3:
                    child2 = QTreeWidgetItem([i])
                    child1.addChild(child2)
            items.append(item)
        
        self.tree.insertTopLevelItems(0, items)
        self.tree.setSelectionMode(QAbstractItemView.MultiSelection)
        self.button = QPushButton('Done')
        self.button.setFixedSize(QSize(30, 20))
        self.button.setFont(QFont('Arial', 7))
        self.button.clicked.connect(self.clicks)
        l = QVBoxLayout()
        l.addWidget(self.tree)
        l.addWidget(self.button, alignment=Qt.AlignRight)
        self.resize(700, 400)

        self.setLayout(l)
        self.show()

    def clicks(self):
        result = self.tree.selectedItems()
        for item in result:
            self.selects.append(item.text(0))
        w.setSDG(self.selects, self.irimapper)


app = QApplication(sys.argv)
# Create and show the form
w = Window()
# Run the main Qt 
sys.exit(app.exec())
