import sys
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
import re
class Window(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle('NGO Search')
        vert = QVBoxLayout() # general layout
        inputs = QFormLayout()
        row1 = QHBoxLayout()
        self.row2 = QHBoxLayout()
        rowbottom = QHBoxLayout()
        dropdown = QComboBox()
        results = QGridLayout()
        self.t = None
        self.items = []
        self.resize(1000,700)

        self.locationEdit = QPushButton("Edit Location")
        row1.addWidget(QLabel("Chandigarh"))
        row1.addWidget(self.locationEdit)

        self.scroll = QScrollArea()             # Scroll Area which contains the widgets, set as the centralWidget
        self.widget = QWidget()                 # Widget that contains the collection of Vertical Box
        self.vbox = QVBoxLayout()    
        self.sdgItem = QLabel("All")
        self.items.append(self.sdgItem)
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
        
        dropdown.addItems(["None", "Gold", "Platinum", "Diamond"])
        # cert = dropdown.currentText()
        # print(cert)
        minf = QLineEdit()
        minf.setPlaceholderText("₹0") #no input this returns empty string not 0
        maxf = QLineEdit()
        maxf.setPlaceholderText("no limit")

        textS = QLineEdit()

        searchB = QPushButton("Search")
        resetB = QPushButton("Reset Search")
        doneB = QPushButton("Done")

        maxsearch = QLineEdit()
        maxsearch.setPlaceholderText("10")

        inputs.addRow(QLabel('Locations:'), row1)
        inputs.addRow(QLabel('SDGs:'), self.row2)
        inputs.addRow(QLabel('Certification:'), dropdown)
        inputs.addRow(QLabel('Minimum Annual Budget:'), minf)
        inputs.addRow(QLabel('Maximum Annual Budget:'), maxf)
        inputs.addRow(QLabel('Text Search:'), textS)
        inputs.addRow(QLabel('Maximum Number of NGOs:'), maxsearch)
        
        rowbottom.addWidget(searchB)
        rowbottom.addWidget(resetB)
        rowbottom.addWidget(doneB)

        #results grid
        name1 = QLabel('NGO Name')
        font = name1.font()
        font.setBold(True)
        name1.setFont(font)
        results.addWidget(name1,0,0)
        results.addWidget(QLabel('Tech For Women'),1,0) 
        results.addWidget(QLabel('Action of Human Movement (AHM)'),2,0)
        results.addWidget(QLabel('Tech For Humanity'),3,0)

        name2 = QLabel('NGO Description')
        name2.setFont(font)
        results.addWidget(name2,0,1)
        h1q = QLabel('Tech for Women provides technology education, infrastructure, and tools to promote gender equality for girls and women of India')
        h2q = QLabel('Action of Human Movement (AHM) is working for the deprived sections of rural youths, Women, Children and BPL (Below Poverty Line) community in India.')
        h3q = QLabel("Our goal is to promote the development of technology infrastructure and education for those who most need it to lead a better life.")
        
        h1q.setWordWrap(True)
        h2q.setWordWrap(True)
        h3q.setWordWrap(True)
        
        results.addWidget(h1q,1,1) 
        results.addWidget(h2q,2,1)
        results.addWidget(h3q,3,1)

        name3 = QLabel('SDG Focus')
        name3.setFont(font)
        results.addWidget(name3,0,2)
        h3qq = QLabel('5. Gender Equality, Target 5.b, Indicator 5.b.1, Target 4.3, Target 4.4, Target 4.5')
        h3qq.setWordWrap(True)
        results.addWidget(h3qq,1,2)
        h4qq = QLabel('5. Gender Equality. Target 5.1, Target 5.2, Target 5.3, Target 5.4, Target 5.a, Target 5.b')
        h4qq.setWordWrap(True)
        h5qq = QLabel('9. Industry Innovation And Infrastructure, Target 5.b, Indicator 5.b.1')
        h5qq.setWordWrap(True)
        results.addWidget(h4qq,2,2)
        results.addWidget(h5qq,3,2)

        name4 = QLabel('Provides Services in Locations')
        name4.setFont(font)
        name4.setWordWrap(True)
        results.addWidget(name4,0,3)
        results.addWidget(QLabel('Chandigarh'),1,3) 
        results.addWidget(QLabel('Chandigarh, Punjab'),2,3)
        results.addWidget(QLabel('Haryana, Chandigarh'),3,3)
        
        name5 = QLabel('Annual Budget')
        name5.setFont(font)
        results.addWidget(name5,0,4)
        results.addWidget(QLabel('₹800,000'),1,4) 
        results.addWidget(QLabel('₹850,000'),2,4)
        results.addWidget(QLabel('₹650,000'),3,4)

        name6 = QLabel('Daan Certification')
        name6.setFont(font)
        results.addWidget(name6,0,5)
        results.addWidget(QLabel('Platimum'),1,5) 
        results.addWidget(QLabel('Diamond'),2,5)
        results.addWidget(QLabel('Gold'),3,5)

        self.scroll2 = QScrollArea()             # Scroll Area which contains the widgets, set as the centralWidget
        self.widget2 = QWidget()                 # Widget that contains the collection of Vertical Box    
        self.widget2.setLayout(results)    
        self.scroll2.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll2.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll2.setWidgetResizable(True)
        self.scroll2.setWidget(self.widget2)

        vert.addLayout(inputs)
        vert.addWidget(QLabel('Results: (Showing 3 of 3)'))
        vert.addWidget(self.scroll2)
        vert.addLayout(rowbottom)

        self.setLayout(vert)
        self.show()

    def sdgtree(self):
        self.t = Tree()
        self.t.show()
    
    def setSDG(self, a):
        for i in self.items:
            i.deleteLater()
        self.items.clear()
        
        for i in range(len(a)):
            self.items.append(QLabel(a[i]))
            self.vbox.addWidget(self.items[i])

        self.t.close()

class Tree(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle('SDG Tree')
        data = {"1. End poverty in all its forms everywhere": ["1.1 By 2030, eradicate extreme poverty for all people everywhere, currently measured as people living on less than $1.25 a day"],
        "2. End hunger, achieve food security and improved nutrition and promote sustainable agriculture": ["1.2 By 2030, reduce at least by half the proportion of men, women and children of all ages living in poverty in all its dimensions according to national definitions"],
        "3. Ensure healthy lives and promote well-being for all at all ages": ["3.1 By 2030, reduce the global maternal mortality ratio to less than 70 per 100,000 live births"],
        "4. Ensure inclusive and equitable quality education and promote lifelong learning opportunities for all": ["4.1 By 2030, ensure that all girls and boys complete free, equitable and quality primary and secondary education leading to relevant and effective learning outcomes"],
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
        "6. Ensure availability and sustainable management of water and sanitation for all": ["6.1 By 2030, achieve universal and equitable access to safe and affordable drinking water for all"],
        "7. Ensure access to affordable, reliable, sustainable and modern energy for all":["7.1 By 2030, ensure universal access to affordable, reliable and modern energy services"],
        "8. Promote sustained, inclusive and sustainable economic growth, full and productive employment and decent work for all":["8.1 Sustain per capita economic growth in accordance with national circumstances and, in particular, at least 7 percent gross domestic product growth per annum in the least developed countries"],
        "9. Build resilient infrastructure, promote inclusive and sustainable industrialization and foster innovation":["9.1 Develop quality, reliable, sustainable and resilient infrastructure, including regional and transborder infrastructure, to support economic development and human well-being, with a focus on affordable and equitable access for all"],
        "10. Reduce inequality within and among countries":["10.1 By 2030, progressively achieve and sustain income growth of the bottom 40 percent of the population at a rate higher than the national average"],
        "11. Make cities and human settlements inclusive, safe, resilient and sustainable":["11.1 By 2030, ensure access for all to adequate, safe and affordable housing and basic services and upgrade slums"],
        "12. Ensure sustainable consumption and production patterns":["12.1 Implement the 10-Year Framework of Programmes on Sustainable Consumption and Production Patterns, all countries taking action, with developed countries taking the lead, taking into account the development and capabilities of developing countries"],
        "13. Take urgent action to combat climate change and its impacts":["13.1 Strengthen resilience and adaptive capacity to climate-related hazards and natural disasters in all countries"],
        "14. Conserve and sustainably use the oceans, seas and marine resources for sustainable development":["14.1 By 2025, prevent and significantly reduce marine pollution of all kinds, in particular from land-based activities, including marine debris and nutrient pollution"],
        "15. Protect, restore and promote sustainable use of terrestrial ecosystems, sustainably manage forests, combat desertification, and halt and reverse land degradation and halt biodiversity loss":["15.1 By 2020, ensure the conservation, restoration and sustainable use of terrestrial and inland freshwater ecosystems and their services, in particular forests, wetlands, mountains and drylands, in line with obligations under international agreements"],
        "16. Promote peaceful and inclusive societies for sustainable development, provide access to justice for all and build effective, accountable and inclusive institutions at all levels":["16.1 Significantly reduce all forms of violence and related death rates everywhere"],
        "17. Strengthen the means of implementation and revitalize the Global Partnership for Sustainable Development":["17.1 Strengthen domestic resource mobilization, including through international support to developing countries, to improve domestic capacity for tax and other revenue collection"]
        }

        indicators = [["5.1.1 Whether or not legal frameworks are in place to promote, enforce and monitor equality and non-discrimination on the basis of sex"], 
              ["5.2.1 Proportion of ever-partnered women and girls aged 15 years and older subjected to physical, sexual or psychological violence by a current or former intimate partner in the previous 12 months, by form of violence and by age","5.2.2 Proportion of women and girls aged 15 years and older subjected to sexual violence by persons other than an intimate partner in the previous 12 months, by age and place of occurrence"],
              ["5.3.1 Proportion of women aged 20-24 years who were married or in a union before age 15 and before age 18", "5.3.2 Proportion of girls and women aged 15-49 years who have undergone female genital mutilation/cutting, by age"],
              ["5.4.1 Proportion of time spent on unpaid domestic and care work, by sex, age and location"],
              ["5.5.1 Proportion of seats held by women in (a) national parliaments and (b) local governments", "5.5.2 Proportion of women in managerial positions"],
              ["5.6.1 Proportion of women aged 15-49 years who make their own informed decisions regarding sexual relations, contraceptive use and reproductive health care", "5.6.2 Number of countries with laws and regulations that guarantee full and equal access to women and men aged 15 years and older to sexual and reproductive health care, information and education"],
              ["5.a.1 (a) Proportion of total agricultural population with ownership or secure rights over agricultural land, by sex; and (b) share of women among owners or rights-bearers of agricultural land, by type of tenure", "5.a.2 Proportion of countries where the legal framework (including customary law) guarantees women's equal rights to land ownership and/or control"],
              ["5.b.1 Proportion of individuals who own a mobile telephone, by sex"],
              ["5.c.1 Proportion of countries with systems to track and make public allocations for gender equality and women's empowerment"]]
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
        self.resize(700,400)
        
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
