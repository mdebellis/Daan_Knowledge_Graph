import sys
from PySide6.QtWidgets import QApplication, QTreeWidget, QTreeWidgetItem
data = {"1. End poverty in all its forms everywhere": ["1.1 By 2030, eradicate extreme poverty for all people everywhere, currently measured as people living on less than $1.25 a day"],
        "2. End hunger, achieve food security and improved nutrition and promote sustainable agriculture": ["1.2 By 2030, reduce at least by half the proportion of men, women and children of all ages living in poverty in all its dimensions according to national definitions"],
        "3. Ensure healthy lives and promote well-being for all at all ages": []}
app = QApplication()
tree = QTreeWidget()
tree.setColumnCount(2)
tree.setHeaderLabels(["United Nations Goal", "United Nations Target and Indicator"])
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