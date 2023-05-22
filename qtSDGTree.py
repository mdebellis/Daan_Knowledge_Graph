import sys
from PySide6.QtWidgets import QApplication, QTreeWidget, QTreeWidgetItem
data = {"1. End poverty in all its forms everywhere": ["1.1 By 2030, eradicate extreme poverty for all people everywhere, currently measured as people living on less than $1.25 a day"],
        "2. End hunger, achieve food security and improved nutrition and promote sustainable agriculture": ["1.2 By 2030, reduce at least by half the proportion of men, women and children of all ages living in poverty in all its dimensions according to national definitions"],
        "3. Ensure healthy lives and promote well-being for all at all ages": ["3.1 By 2030, reduce the global maternal mortality ratio to less than 70 per 100,000 live births"],
        "4. Ensure inclusive and equitable quality education and promote lifelong learning opportunities for all": ["4.1 By 2030, ensure that all girls and boys complete free, equitable and quality primary and secondary education leading to relevant and effective learning outcomes"],
        "5. Achieve gender equality and empower all women and girls":["5.1 End all forms of discrimination against all women and girls everywhere"],
        "6. Ensure availability and sustainable management of water and sanitation for all": ["6.1 By 2030, achieve universal and equitable access to safe and affordable drinking water for all"],
        "7. Ensure access to affordable, reliable, sustainable and modern energy for all":[],
        "8. Promote sustained, inclusive and sustainable economic growth, full and productive employment and decent work for all":[],
        "9. Build resilient infrastructure, promote inclusive and sustainable industrialization and foster innovation":[],
        "10. Reduce inequality within and among countries":[],
        "11. Make cities and human settlements inclusive, safe, resilient and sustainable":[],
        "12. Ensure sustainable consumption and production patterns":[],
        "13. Take urgent action to combat climate change and its impacts":[],
        "14. Conserve and sustainably use the oceans, seas and marine resources for sustainable development":[]}
app = QApplication()
tree = QTreeWidget()
tree.setColumnCount(1)
tree.setHeaderLabels(["United Nations Sustainable Development Goals, Targets, Indicators"])
items = []
for key, values in data.items():
    item = QTreeWidgetItem([key])
    for tori in values:
        child1 = QTreeWidgetItem([tori])
        item.addChild(child1)
    items.append(item)

tree.insertTopLevelItems(0, items)
tree.show()
sys.exit(app.exec())
