import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from Application.Layouts.home_layout import Ui_MainWindow
from Datasets.dataset_utilities import possible_years

app = QApplication(sys.argv)


class HomeWindow(QMainWindow, Ui_MainWindow):

    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.year_drop_down.addItems(possible_years())


gui_home = HomeWindow()
gui_home.show()
sys.exit(app.exec_())
