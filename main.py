import sys
from PyQt5.QtWidgets import QApplication

from ui.main_window import SitSmartWindow

app = QApplication(sys.argv)

window = SitSmartWindow()
window.show()

sys.exit(app.exec_())