import sys
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
from franz.openrdf.connect import ag_connect
from ngoDisplayFunctional import NGOScreen
from functools import partial
from franz.openrdf.vocabulary import RDF
from franz.openrdf.query.query import QueryLanguage
from dropdownMS import *
import webbrowser
# from qt_material import apply_stylesheet #library for themes
import re


class Window(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Allegrograph presets
        self.conn = ag_connect('NGO', host='localhost', port='10035',
                               user='test', password='xyzzy')
        self.conn.setNamespace('ngo', 'http://www.semanticweb.org/mdebe/ontologies/NGO#')
        self.conn.setNamespace('sdg', 'http://www.semanticweb.org/mdebe/ontologies/2022/10/UNSDG#')
        self.conn.setNamespace('prov', 'https://www.w3.org/TR/prov-o/#')
        self.conn.setNamespace('rdfs', 'http://www.w3.org/2000/01/rdf-schema#')
        
        self.setWindowTitle('Search')
        self.resize(1514, 844)
    
        self.orgTypes = [] # list to hold org types for the query
        self.t = None  # instance to call sdg tree class
        self.sdgs = []  # list to track all sdgs selected, this is needed for reselection(hold an instance to delete)
        self.resultList = []  # list of ngo IRIs from query
        self.allResults = []  # list of every ngo's characteristics, needed for re searching(hold an instance to delete)
        self.resultsbuttons = []  # list of buttons to link results to ngo pages
        self.setR = [] # list that holds result labels, these are changed between CSR and NGOs
        self.ngoScreen = None # variable that calls ngoDisplay to see more info on NGO
        self.sdgIRI = {} # mapper for sdgs and their iris
        self.nums = QLabel('')
        
        #fti creation
        mission_prop = self.conn.createURI('http://www.semanticweb.org/mdebe/ontologies/NGO#missionStatement')
        vision_prop = self.conn.createURI('http://www.semanticweb.org/mdebe/ontologies/NGO#vision')
        objective_prop = self.conn.createURI('http://www.semanticweb.org/mdebe/ontologies/NGO#objectives')
        description_prop = self.conn.createURI('http://www.semanticweb.org/mdebe/ontologies/NGO#description')
        self.conn.createFreeTextIndex("NGO-INDEX", predicates=[description_prop,mission_prop,vision_prop,objective_prop], wordFilters=["stem.english"])
        
        # organization type construction
        self.type = QComboBox()
        self.type.addItems(['All', 'NGO', 'CSR'])
        self.type.currentTextChanged.connect(self.corp)
        
        # location construction
        self.statedrop = MultiComboBox()
        self.statedrop.addItems(["Andhra Pradesh","Arunachal Pradesh","Assam","Bihar","Chhattisgarh","Goa","Gujarat","Haryana",
                                 "Himachal Pradesh","Jharkhand","Karnataka","Kerala","Maharashtra","Madhya Pradesh","Manipur",
                                 "Meghalaya","Mizoram","Nagaland","Odisha","Punjab","Rajasthan","Sikkim","Tamil Nadu","Tripura",
                                 "Telangana","Uttar Pradesh","Uttarakhand","West Bengal","Andaman & Nicobar","Chandigarh",
                                 "Dadra & Nagar Haveli and Daman & Diu","Delhi","Jammu & Kashmir","Ladakh","Lakshadweep","Puducherry (UT)"])
        
        #sdg scrolling construction
        self.sdgRow = QHBoxLayout()
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
        self.sdgRow.addWidget(self.scroll)
        self.sdgEdit = QPushButton("Edit SDGs")
        self.sdgEdit.clicked.connect(self.sdgtree)
        self.sdgRow.addWidget(self.sdgEdit)
        
        # Checkable construction of org types, only shows under CSR
        self.checkRow = QHBoxLayout()
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
        self.checkRow.addWidget(self.check1)
        self.checkRow.addWidget(self.check2)
        self.checkRow.addWidget(self.check3)
        self.checkRow.addWidget(self.check4)
        self.checkRow.addWidget(self.check5)
        self.checkRow.addWidget(self.check6)
        self.orgTypeRow = QHBoxLayout()
        self.orgTypeRow.addWidget(QLabel('Organization Type:'))
        self.orgTypeRow.addLayout(self.checkRow)
        self.orgframe = QFrame()
        self.orgframe.setLayout(self.orgTypeRow)
        self.orgframe.hide()
        
        # org class construction, only shows under ngo
        self.orgClassRow = QHBoxLayout()
        self.orgClassRow.addWidget(QLabel('Organization Class:'))
        self.clas = QComboBox()
        self.clas.addItems(['All', 'Private', 'Public'])
        self.orgClassRow.addWidget(self.clas)
        self.clasframe = QFrame()
        self.clasframe.setLayout(self.orgClassRow)
        self.clasframe.hide()

        # finance construction
        self.minf = QLineEdit()
        self.minf.setPlaceholderText("₹0")  # no input this returns empty string not 0
        self.maxf = QLineEdit()
        self.maxf.setPlaceholderText("no limit")

        # text search
        self.textS = QLineEdit()

        # number search
        self.maxnumsearch = QLineEdit()
        self.maxnumsearch.setPlaceholderText("10")        
        
        # add all inputs into an organizer
        self.inputs = QFormLayout()
        self.inputs.addRow(self.type)
        self.inputs.addRow(QLabel('Locations:'), self.statedrop)
        self.inputs.addRow(QLabel('SDGs:'), self.sdgRow)
        self.inputs.addRow(self.orgframe)
        self.inputs.addRow(self.clasframe)
        self.inputs.addRow(QLabel('Minimum Monthly Budget:'), self.minf)
        self.inputs.addRow(QLabel('Maximum Monthly Budget:'), self.maxf)
        self.inputs.addRow(QLabel('Text Search:'), self.textS)
        self.inputs.addRow(QLabel('Maximum Results:'), self.maxnumsearch)

        # results grid construction
        self.results = QGridLayout()
        self.doQuery()
        
        # scroll area for results
        self.scroll2 = QScrollArea()
        self.widget2 = QWidget()
        self.widget2.setLayout(self.results)
        self.scroll2.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll2.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll2.setWidgetResizable(True)
        self.scroll2.setWidget(self.widget2)
        
        # bottom row of buttons
        self.rowbottom = QHBoxLayout()
        searchB = QPushButton("Search")
        searchB.clicked.connect(self.doQuery)
        resetB = QPushButton("Reset Search")
        resetB.clicked.connect(self.reset)
        self.graph = QPushButton('See Graph')
        self.graph.clicked.connect(self.browser)
        doneB = QPushButton("Done")
        doneB.clicked.connect(self.exit)
        self.rowbottom.addWidget(searchB)
        self.rowbottom.addWidget(resetB)
        self.rowbottom.addWidget(self.graph)
        self.rowbottom.addWidget(doneB)

        # adding all sub layouts and widgets to main vertical layout
        self.vert = QVBoxLayout() 
        self.vert.addLayout(self.inputs) # all user inputs for the query
        self.vert.addWidget(self.nums) # line for 'showing n of m results' constructed in doquery()
        self.vert.addWidget(self.scroll2) # scroll area displaying results
        self.vert.addLayout(self.rowbottom) # bottom row buttons

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
    
    def corp(self):
        if self.type.currentText() == 'All':
            self.orgframe.hide()
            self.clasframe.hide()
        if self.type.currentText() == 'NGO':
            self.orgframe.show()
            self.clasframe.hide()
        if self.type.currentText() == 'CSR':
            self.orgframe.hide()
            self.clasframe.show()
        self.show()
        
    def get_name_from_iri(self, iri):
        iri_str = str(iri)
        iri_str = iri_str.replace('<', '')
        iri_str = iri_str.replace('>', '')
        if iri_str.startswith('http://www.semanticweb.org/mdebe/ontologies/NGO#'):
            iri_str = iri_str.replace('http://www.semanticweb.org/mdebe/ontologies/NGO#','ngo:')
        elif iri_str.startswith('http://www.semanticweb.org/mdebe/ontologies/2022/10/UNSDG#'):
            iri_str = iri_str.replace('http://www.semanticweb.org/mdebe/ontologies/2022/10/UNSDG#', 'sdg:')
        return iri_str

    def generateQuery(self, sdgs=[], maxBudget = None, minBudget = None, loc_list =[],orgTypeList = [], classtype = 'All', qlimit ="20",fti_string=""):
        ctype = ''
        if self.type.currentText() == 'All':
            ctype = 'prov:Organization'
        elif self.type.currentText() == 'NGO':
            ctype = 'ngo:NGORecipient'
        else:
            ctype = 'ngo:CSRProgram'
            
        qstring = "SELECT * WHERE {?ngoRecipient a " + ctype  + "; rdfs:label ?label."
        if ctype == 'ngo:NGORecipient':
            qstring = qstring + " FILTER(EXISTS {?ngoRecipient ngo:missionStatement ?mission} || (EXISTS {?ngoRecipient ngo:objectives ?obj})) "
        org_type_test_string = "?ngoRecipient ngo:orgType ?orgType."
        org_type_query_string = ""
        loc_string = "?ngoRecipient ngo:state ?state."
        loc_filter = ""
        i = 0
        if maxBudget != None:
            mbstring = " ?ngoRecipient ngo:avgMonthlyExpenditure ?avm. Filter(?avm <= " + str(maxBudget) + ")"
            qstring = qstring + mbstring
        if minBudget != None:
            mbstring = " ?ngoRecipient ngo:avgMonthlyExpenditure ?avm. Filter(?avm >= " + str(minBudget) + ")"
            qstring = qstring + mbstring
        for loc in loc_list:
            loc_filter = loc_filter +  "|| ?state =  \"" + loc + "\" "
        if loc_list !=[]:
            qstring = qstring + loc_string + " Filter(" + loc_filter[3:] + ")"
        if ctype == 'ngo:NGORecipient':
            for orgType in orgTypeList:
                org_type_query_string = org_type_query_string + "|| ?orgType =  \"" + orgType + "\" "
            if orgTypeList !=[]:
                org_type_query_string = org_type_test_string + " Filter(" + org_type_query_string[3:] + ")"
                qstring = qstring + org_type_query_string
        if ctype == 'ngo:CSRProgram' and classtype != 'All':
             cs = '?ngoRecipient ngo:class \"' + classtype + "\"."
             qstring = qstring + cs
        for sdg in sdgs:
            sdgname = self.get_name_from_iri(sdg)
            sdg_test_string = " ?ngoRecipient ngo:hasSDGGoal " + sdgname + ". "
            qstring = qstring + sdg_test_string
        if fti_string != "":
            ftiqs = "?ngoRecipient fti:match " + "\"" + fti_string + "\"" ". "
            qstring = qstring + ftiqs
        qstring = qstring + "} ORDER BY ?label "
        return qstring

    def query(self, sdgs=[], maxBudget = None, minBudget = None, loc_list =[], orgTypeList = [], classtype = 'All', qlimit ="20",fti_string=""):
        query_string = self.generateQuery(sdgs, maxBudget, minBudget, loc_list, orgTypeList, classtype, qlimit,fti_string)
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
        
        sdglist = []
        for s in self.sdgs:
            if s.text() == 'All':
                break
            sdglist.append(self.sdgIRI[s.text()])
            
        self.resultList = self.query(sdgs=sdglist, maxBudget = maxbudget, minBudget = minbudget, 
                                     loc_list = self.statedrop.currentData(), orgTypeList = self.orgTypes, 
                                     classtype = self.clas.currentText(),qlimit = src, fti_string = self.textS.text())
        m = len(self.resultList)
        self.resultList = self.resultList[:int(src)]
        
        iris = [self.conn.createURI('http://www.w3.org/2000/01/rdf-schema#label'),
                self.conn.createURI('http://www.semanticweb.org/mdebe/ontologies/NGO#objectives'),
                self.conn.createURI('http://www.semanticweb.org/mdebe/ontologies/NGO#hasSDGGoal'),
                self.conn.createURI('http://www.semanticweb.org/mdebe/ontologies/NGO#state'),
                self.conn.createURI('http://www.semanticweb.org/mdebe/ontologies/NGO#avgMonthlyExpenditure')]
        if self.type.currentText() == 'CSR':
            iris = [
                self.conn.createURI('http://www.w3.org/2000/01/rdf-schema#label'),
                self.conn.createURI('http://www.semanticweb.org/mdebe/ontologies/NGO#class'),
                self.conn.createURI('http://www.semanticweb.org/mdebe/ontologies/NGO#subCategory'),
                self.conn.createURI('http://www.semanticweb.org/mdebe/ontologies/NGO#state'),
                self.conn.createURI('http://www.semanticweb.org/mdebe/ontologies/NGO#avgMonthlyExpenditure'),
            ]
        self.setResults()
        for param in self.allResults:
            param.deleteLater()
            self.results.removeWidget(param)
        self.allResults = [] # tracks every parameter entered into results to be deleted on new search
        
        for ngorecip in range(len(self.resultList)): #adds all parameters of specified number of ngos into display
            for iri in range(len(iris)):
                sdglabel = ''
                for labelstments in self.conn.getStatements(self.resultList[ngorecip], iris[iri], None):
                    if iris[iri] == self.conn.createURI('http://www.semanticweb.org/mdebe/ontologies/NGO#hasSDGGoal'):
                        for script in self.conn.getStatements(labelstments[2], 
                                                              self.conn.createURI('http://www.semanticweb.org/mdebe/ontologies/2022/10/UNSDG#goalDescription'), None):
                            sdglabel = sdglabel + str(script[2]) + '\n' 
                    else:  
                        l = str(labelstments[2])
                        if len(l) > 1000:
                            l = l[:1001] # character cap so descriptions don't run too long
                        label = QLabel(l[1:len(l)-1])
                        if iri == 4: # very important it avg monthly cost with cost, for formatting
                            label = QLabel(l[1:len(l)-45])
                        label.setWordWrap(True)
                        self.allResults.append(label)
                        self.results.addWidget(label, ngorecip + 1, iri)
                        break
                if iris[iri] == self.conn.createURI('http://www.semanticweb.org/mdebe/ontologies/NGO#hasSDGGoal'):
                    label = QLabel(sdglabel[1:len(sdglabel)-1])
                    label.setWordWrap(True)
                    self.allResults.append(label)
                    self.results.addWidget(label, ngorecip + 1, iri)
                    
        self.resultsbuttons = []
        for i in range(len(self.resultList)): #adds all buttons into results display
            self.resultsbuttons.append(QPushButton('See Details'))
            self.allResults.append(self.resultsbuttons[i])
            self.results.addWidget(self.resultsbuttons[i], i + 1, 6)
            self.resultsbuttons[i].clicked.connect(partial(self.getNGOScreen, self.resultList[i]))
            
        if int(src) > m:
            src = str(m)
        self.nums.setText('Results: (Showing ' + src + ' of ' + str(m) + ')')
        
    def getNGOScreen(self, ngo): # function to call last specific ngo screen
        self.ngoScreen = NGOScreen(ngo)
        
    def browser(self):
        webbrowser.open_new('http://localhost:10035')
        
    def setResults(self):  # set the labels for formatting the results, should only be called once
        if self.setR != []:
            for i in self.setR:
                i.deleteLater()
                self.results.removeWidget(i)
        if self.type.currentText() == 'CSR':
            self.setR = [QLabel('Name'), QLabel('Class'), QLabel('Organization Type'), QLabel('State'), QLabel('Monthly Budget')]
            font = self.setR[0].font()
            font.setBold(True)
            self.setR[0].setFont(font)
            self.results.addWidget(self.setR[0], 0, 0)
            self.setR[1].setFont(font)
            self.results.addWidget(self.setR[1], 0, 1)
            self.setR[2].setFont(font)
            self.results.addWidget(self.setR[2], 0, 2)
            self.setR[3].setFont(font)
            self.results.addWidget(self.setR[3], 0, 3)
            self.setR[4].setFont(font)
            self.results.addWidget(self.setR[4], 0, 4)
        else:
            self.setR = [QLabel('Name'), QLabel('Objective'), QLabel('SDG Focus'), QLabel('State'), QLabel('Monthly Budget')]
            font = self.setR[0].font()
            font.setBold(True)
            self.setR[0].setFont(font)
            self.results.addWidget(self.setR[0], 0, 0)
            self.setR[1].setFont(font)
            self.results.addWidget(self.setR[1], 0, 1)
            self.setR[2].setFont(font)
            self.results.addWidget(self.setR[2], 0, 2)
            self.setR[3].setFont(font)
            self.results.addWidget(self.setR[3], 0, 3)
            self.setR[4].setFont(font)
            self.results.addWidget(self.setR[4], 0, 4)

    def reset(self): # resets all inputs
        self.check1.setChecked(True)
        self.check2.setChecked(True)
        self.check3.setChecked(True)
        self.check4.setChecked(True)
        self.check5.setChecked(True)
        self.check6.setChecked(True)
        self.statedrop.setCurrentText('Select')
        self.minf.clear()
        self.maxf.clear()
        self.textS.clear()
        self.maxnumsearch.clear()
        self.type.setCurrentText('All')
        for i in self.sdgs:
            i.deleteLater()
        self.sdgs.clear()
        self.sdgs.append(QLabel('All'))
        self.vbox.addWidget(self.sdgs[0])
        self.doQuery() # when all parameters are reset, a base set of results will be displayed
    
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
        conn = ag_connect('NGO', host='localhost', port='10035',
                               user='mdebellis', password='df1559')
        conn.setNamespace('ngo', 'http://www.semanticweb.org/mdebe/ontologies/NGO#')
        conn.setNamespace('rdfs', 'hhttp://www.w3.org/2000/01/rdf-schema#')
        conn.setNamespace('rdfs', 'http://www.w3.org/2000/01/rdf-schema#')
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
# app.setStyle(QStyleFactory.create('Windows'))
# apply_stylesheet(app, theme='mt.xml', invert_secondary=True) for the changing themes

w = Window() # Run the main Qt 
sys.exit(app.exec())
