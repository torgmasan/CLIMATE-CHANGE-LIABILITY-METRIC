import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from Application.Layouts.home_layout import Ui_MainWindow

app = QApplication(sys.argv)


class HomeWindow(QMainWindow, Ui_MainWindow):

    def __init__(self):
        super().__init__()
        self.setupUi(self)


gui_home = HomeWindow()
gui_home.show()
sys.exit(app.exec_())
