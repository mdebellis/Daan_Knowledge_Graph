import sys
from PySide6.QtGui import QColor
from PySide6.QtWidgets import (QApplication, QTableWidget,
                               QTableWidgetItem)
ngos = [("JAMAL E WARSI AKHLAKE AALUMN EDUCATIONAL AND WELLFARE SOCIETY", "Rajnandgaon", "Gender Equality"),
          ("Women for India", "Rajnandgaon", "Gender Equality"),
          ("Dignity Foundation for India", "Rajnandgaon", "Gender Equality"),
          ("Damini Social Enterprises", "Rajnandgaon", "Gender Equality")]

app = QApplication()
table = QTableWidget()
table.setRowCount(len(ngos))
table.setColumnCount(len(ngos[0]))
table.setHorizontalHeaderLabels(["NGO Name", "NGO Location", "SDG Focus"])
for i, (name, location,sdg) in enumerate(ngos):
    item_name = QTableWidgetItem(name)
    item_location = QTableWidgetItem(location)
    item_sdg = QTableWidgetItem(sdg)
    table.setItem(i, 0, item_name)
    table.setItem(i, 1, item_location)
    table.setItem(i, 2, item_sdg)
table.show()
sys.exit(app.exec())