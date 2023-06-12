import sys
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
from franz.openrdf.connect import ag_connect
from ngodis import NGOScreen
from functools import partial


class Window(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('NGO Search')
        self.vert = QVBoxLayout()  # general outer layout
        self.inputs = QFormLayout()  # format for entering in the rest of data
        self.row1 = QHBoxLayout()  # format for location row row
        self.row2 = QHBoxLayout()  # format for sdgs row
        self.rowbottom = QHBoxLayout()  # layout for the bottom row buttons (search, reset, done)
        self.dropdown = QComboBox()  # layout to for a certification dropdown menu
        self.results = QGridLayout()  # layout to show results
        self.t = None  # instance to call sdg tree class
        self.sdgs = []  # list to track all sdgs selected, this is needed for reselection(hold an instance to delete)
        self.resultList = []  # list of ngo IRIs from query
        self.allResults = []  # list of every ngo's characteristics, needed for researching(hold an instance to delete)
        self.resultsbuttons = []  # list of buttons to link results to ngo pages
        self.ngoScreen = None
        self.resize(1000, 700)

        self.locationEdit = QPushButton("Edit Location")
        self.location = QLabel("India")

        self.row1.addWidget(self.location)
        self.row1.addWidget(self.locationEdit)

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

        self.dropdown.addItems(["None", "Gold", "Platinum", "Diamond"])

        self.minf = QLineEdit()
        self.minf.setPlaceholderText("₹0")  # no input this returns empty string not 0
        self.maxf = QLineEdit()
        self.maxf.setPlaceholderText("no limit")

        self.textS = QLineEdit()

        self.maxnumsearch = QLineEdit()
        self.maxnumsearch.setPlaceholderText("10")

        self.inputs.addRow(QLabel('Locations:'), self.row1)
        self.inputs.addRow(QLabel('SDGs:'), self.row2)
        self.inputs.addRow(QLabel('Certification:'), self.dropdown)
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
        self.vert.addWidget(QLabel('Results: (Showing 10 of 300,000)'))
        self.vert.addWidget(self.scroll2)
        self.vert.addLayout(self.rowbottom)

        self.setLayout(self.vert)
        self.show()

    def sdgtree(self):
        self.t = Tree()
        self.t.show()

    def setSDG(self, a):
        for i in self.sdgs:
            i.deleteLater()
        self.sdgs.clear()

        for i in range(len(a)):
            self.sdgs.append(QLabel(a[i]))
            self.vbox.addWidget(self.sdgs[i])

        self.t.close()

    def doQuery(self):
        # loc = self.location.text()
        # self.sdgs
        # cert = self.dropdown.currentText()
        # minBudget = self.minf.text()
        # maxBudget = self.maxf.text()
        # text = self.textS.text()
        # numSearch = self.maxnumsearch.text()

        self.conn = ag_connect('NGO', host='localhost', port='10035',
                               user='test', password='xyzzy')
        self.conn.setNamespace('ngo', 'http://www.semanticweb.org/mdebe/ontologies/NGO#')

        iris = [self.conn.createURI('http://www.w3.org/2000/01/rdf-schema#label'),
                self.conn.createURI('http://www.semanticweb.org/mdebe/ontologies/NGO#description'),
                self.conn.createURI('http://www.semanticweb.org/mdebe/ontologies/NGO#hasSDGGoal'),
                self.conn.createURI('http://www.semanticweb.org/mdebe/ontologies/NGO#providesServicesInLocation'),
                self.conn.createURI('http://www.semanticweb.org/mdebe/ontologies/NGO#maximumAnualBudget'),
                self.conn.createURI('http://www.semanticweb.org/mdebe/ontologies/NGO#hasDaanRating')]
        query = self.conn.prepareTupleQuery(query="""
            SELECT * WHERE {?ngoRecipient a ngo:NGORecipient} LIMIT 20 """)
        self.resultList = [] #all ngo recipients
        with query.evaluate() as result:
            for statement in result:
                # ngorecip = statement[0]
                self.resultList.append(statement[0])
                # for labelstments in conn.getStatements(ngorecip, rdfslbl, None):
                #     resultList.append(labelstments[2])
        # may seem redundant however, unknown how many ngos are in results, maxsearchnum constantly changing
        for param in self.allResults:
            param.deleteLater()
            self.results.removeWidget(param)
        self.allResults = []
        if self.maxnumsearch.text() == '':
            maxs = 10
        else:
            maxs = int(self.maxnumsearch.text())
        for ngorecip in range(0, min(maxs, len(self.resultList))):
            for iri in range(len(iris)):
                for labelstments in self.conn.getStatements(self.resultList[ngorecip], iris[iri], None):
                    label = QLabel(str(labelstments[2]))
                    label.setWordWrap(True)
                    self.allResults.append(label)
                    self.results.addWidget(label, ngorecip + 1, iri)
        self.resultsbuttons = []
        for i in range(0, min(maxs, len(self.resultList))):
            self.resultsbuttons.append(QPushButton('See NGO'))
            self.results.addWidget(self.resultsbuttons[i], i + 1, 6)
            self.resultsbuttons[i].clicked.connect(partial(self.getNGOScreen, self.resultList[i]))
        
    def getNGOScreen(self, ngo):
        self.ngoScreen = NGOScreen(ngo)
        

    def setResults(self):  # set the labels for formatting should only be called once

        name1 = QLabel('NGO Name')
        font = name1.font()
        font.setBold(True)
        name1.setFont(font)
        self.results.addWidget(name1, 0, 0)
        name2 = QLabel('NGO Description')
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
        name6 = QLabel('Daan Certification')
        name6.setFont(font)
        self.results.addWidget(name6, 0, 5)

        self.doQuery()

        # iris = [self.conn.createURI('http://www.w3.org/2000/01/rdf-schema#label')] #for each display characteristic
        # namebuttons = []
        # self.results.removeWidget(self.name1)
        # self.name1.deleteLater()
        # self.results.addWidget(QLabel("hi"),0,0)
        # for ngorecip in range(1,11):
        #     for lab in self.conn.getStatements(self.resultList[ngorecip-1], iris[0], None):
        #         self.results.removeWidget(self.results.takeAt(0,0).widget())
        #         self.results.addWidget(QLabel(str(lab[2])),ngorecip, 0)
        # for ngorecip in range(len(self.resultList)):
        #     for iriobj in range(len(iris)):
        #         for labelstments in self.conn.getStatements(self.resultList[ngorecip], iris[iriobj], None):
        #             results.addWidget(QLabel(labelstments[2]),iriobj,ngorecip)

    def reset(self):
        self.dropdown.setCurrentText('None')
        self.minf.clear()
        self.maxf.clear()
        self.textS.clear()
        self.maxnumsearch.clear()
        for i in self.sdgs:
            i.deleteLater()
        self.sdgs.clear()
        self.sdgs.append(QLabel('All'))
        self.vbox.addWidget(self.sdgs[0])
        self.doQuery()

    def exit(self):
        self.close()


class Tree(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle('Select SDG(s)')
        data = {"1. End poverty in all its forms everywhere": [
            "1.1 By 2030, eradicate extreme poverty for all people everywhere, currently measured as people living on less than $1.25 a day"],
                "2. End hunger, achieve food security and improved nutrition and promote sustainable agriculture": [
                    "1.2 By 2030, reduce at least by half the proportion of men, women and children of all ages living in poverty in all its dimensions according to national definitions"],
                "3. Ensure healthy lives and promote well-being for all at all ages": [
                    "3.1 By 2030, reduce the global maternal mortality ratio to less than 70 per 100,000 live births"],
                "4. Ensure inclusive and equitable quality education and promote lifelong learning opportunities for all": [
                    "4.1 By 2030, ensure that all girls and boys complete free, equitable and quality primary and secondary education leading to relevant and effective learning outcomes"],
                "5. Achieve gender equality and empower all women and girls":
                    ["5.1 End all forms of discrimination against all women and girls everywhere",
                     "5.2 Eliminate all forms of violence against all women and girls in the public and private spheres, including trafficking and sexual and other types of exploitation",
                     "5.3 Eliminate all harmful practices, such as child, early and forced marriage and female genital mutilation",
                     "5.4 Recognize and value unpaid care and domestic work through the provision of public services, infrastructure and social protection policies and the promotion of shared responsibility within the household and the family as nationally appropriate",
                     "5.5 Ensure women's full and effective participation and equal opportunities for leadership at all levels of decision-making in political, economic and public life",
                     "5.6 Ensure universal access to sexual and reproductive health and reproductive rights as agreed in accordance with the Programme of Action of the International Conference on Population and Development and the Beijing Platform for Action and the outcome documents of their review conferences",
                     "5.a Undertake reforms to give women equal rights to economic resources, as well as access to ownership and control over land and other forms of property, financial services, inheritance and natural resources, in accordance with national laws",
                     "5.b Enhance the use of enabling technology, in particular information and communications technology, to promote the empowerment of women",
                     "5.c Adopt and strengthen sound policies and enforceable legislation for the promotion of gender equality and the empowerment of all women and girls at all levels"],
                "6. Ensure availability and sustainable management of water and sanitation for all": [
                    "6.1 By 2030, achieve universal and equitable access to safe and affordable drinking water for all"],
                "7. Ensure access to affordable, reliable, sustainable and modern energy for all": [
                    "7.1 By 2030, ensure universal access to affordable, reliable and modern energy services"],
                "8. Promote sustained, inclusive and sustainable economic growth, full and productive employment and decent work for all": [
                    "8.1 Sustain per capita economic growth in accordance with national circumstances and, in particular, at least 7 percent gross domestic product growth per annum in the least developed countries"],
                "9. Build resilient infrastructure, promote inclusive and sustainable industrialization and foster innovation": [
                    "9.1 Develop quality, reliable, sustainable and resilient infrastructure, including regional and transborder infrastructure, to support economic development and human well-being, with a focus on affordable and equitable access for all"],
                "10. Reduce inequality within and among countries": [
                    "10.1 By 2030, progressively achieve and sustain income growth of the bottom 40 percent of the population at a rate higher than the national average"],
                "11. Make cities and human settlements inclusive, safe, resilient and sustainable": [
                    "11.1 By 2030, ensure access for all to adequate, safe and affordable housing and basic services and upgrade slums"],
                "12. Ensure sustainable consumption and production patterns": [
                    "12.1 Implement the 10-Year Framework of Programmes on Sustainable Consumption and Production Patterns, all countries taking action, with developed countries taking the lead, taking into account the development and capabilities of developing countries"],
                "13. Take urgent action to combat climate change and its impacts": [
                    "13.1 Strengthen resilience and adaptive capacity to climate-related hazards and natural disasters in all countries"],
                "14. Conserve and sustainably use the oceans, seas and marine resources for sustainable development": [
                    "14.1 By 2025, prevent and significantly reduce marine pollution of all kinds, in particular from land-based activities, including marine debris and nutrient pollution"],
                "15. Protect, restore and promote sustainable use of terrestrial ecosystems, sustainably manage forests, combat desertification, and halt and reverse land degradation and halt biodiversity loss": [
                    "15.1 By 2020, ensure the conservation, restoration and sustainable use of terrestrial and inland freshwater ecosystems and their services, in particular forests, wetlands, mountains and drylands, in line with obligations under international agreements"],
                "16. Promote peaceful and inclusive societies for sustainable development, provide access to justice for all and build effective, accountable and inclusive institutions at all levels": [
                    "16.1 Significantly reduce all forms of violence and related death rates everywhere"],
                "17. Strengthen the means of implementation and revitalize the Global Partnership for Sustainable Development": [
                    "17.1 Strengthen domestic resource mobilization, including through international support to developing countries, to improve domestic capacity for tax and other revenue collection"]
                }

        indicators = [[
                          "5.1.1 Whether or not legal frameworks are in place to promote, enforce and monitor equality and non-discrimination on the basis of sex"],
                      [
                          "5.2.1 Proportion of ever-partnered women and girls aged 15 years and older subjected to physical, sexual or psychological violence by a current or former intimate partner in the previous 12 months, by form of violence and by age",
                          "5.2.2 Proportion of women and girls aged 15 years and older subjected to sexual violence by persons other than an intimate partner in the previous 12 months, by age and place of occurrence"],
                      [
                          "5.3.1 Proportion of women aged 20-24 years who were married or in a union before age 15 and before age 18",
                          "5.3.2 Proportion of girls and women aged 15-49 years who have undergone female genital mutilation/cutting, by age"],
                      ["5.4.1 Proportion of time spent on unpaid domestic and care work, by sex, age and location"],
                      ["5.5.1 Proportion of seats held by women in (a) national parliaments and (b) local governments",
                       "5.5.2 Proportion of women in managerial positions"],
                      [
                          "5.6.1 Proportion of women aged 15-49 years who make their own informed decisions regarding sexual relations, contraceptive use and reproductive health care",
                          "5.6.2 Number of countries with laws and regulations that guarantee full and equal access to women and men aged 15 years and older to sexual and reproductive health care, information and education"],
                      [
                          "5.a.1 (a) Proportion of total agricultural population with ownership or secure rights over agricultural land, by sex; and (b) share of women among owners or rights-bearers of agricultural land, by type of tenure",
                          "5.a.2 Proportion of countries where the legal framework (including customary law) guarantees women's equal rights to land ownership and/or control"],
                      ["5.b.1 Proportion of individuals who own a mobile telephone, by sex"],
                      [
                          "5.c.1 Proportion of countries with systems to track and make public allocations for gender equality and women's empowerment"]]
        self.tree = QTreeWidget()
        self.tree.setColumnCount(1)
        self.tree.setHeaderLabels(["United Nations Sustainable Development Goals, Targets, Indicators"])
        self.selects = []
        items = []
        count = 1
        for key, values in data.items():
            item = QTreeWidgetItem([key])
            for tori in range(len(values)):
                child1 = QTreeWidgetItem([values[tori]])
                item.addChild(child1)
                if count == 5:
                    for i in indicators[tori]:
                        child2 = QTreeWidgetItem([i])
                        child1.addChild(child2)
            items.append(item)
            count += 1
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
        w.setSDG(self.selects)


app = QApplication(sys.argv)
# Create and show the form
w = Window()
# Run the main Qt 
sys.exit(app.exec())
