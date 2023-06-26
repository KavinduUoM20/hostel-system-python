import sys
from PyQt6.QtWidgets import QApplication
from HostelSystem import HostelSystem

app = QApplication(sys.argv)
hostel_system = HostelSystem()
sys.exit(app.exec())