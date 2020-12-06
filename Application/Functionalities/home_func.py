import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QComboBox
from PyQt5 import QtCore
from Application.Layouts.home_layout import Ui_MainWindow
from Datasets.dataset_utilities import possible_years, get_datasets

app = QApplication(sys.argv)


class HomeWindow(QMainWindow, Ui_MainWindow):

    def __init__(self) -> None:
        super().__init__()
        self.setupUi(self)
        self.dataset_to_combo_box = {}
        self.dataset_to_correlation = {}

        self.year_drop_down.addItems(possible_years())
        self.populate_grid()

        self.begin_analysis.clicked.connect(self.open_constant_window)

    def populate_grid(self) -> None:
        """Adds required Label and ComboBox items to
        obtain correlation for all csv files in Responsibility Datasets directory

        Preconditions:
            - At least one csv file in Raw Datasets
        """
        temp_combo_year = str(self.year_drop_down.currentText())
        correlation_keys = list(get_datasets(temp_combo_year).keys())
        combo_box_items = ['direct', 'inverse']

        for i in range(len(correlation_keys)):
            label = QLabel(correlation_keys[i])
            label.setAlignment(QtCore.Qt.AlignCenter)
            self.correlation_grid.addWidget(label, i, 0)
            self.dataset_to_combo_box[correlation_keys[i]] = QComboBox()
            current_combo = self.dataset_to_combo_box[correlation_keys[i]]
            current_combo.addItems(combo_box_items)
            self.correlation_grid.addWidget(current_combo, i, 1)

    def open_constant_window(self):
        """Close the HomeWindow and open the ConstantWindow"""
        for dataset in self.dataset_to_combo_box:
            current_combo = self.dataset_to_combo_box[dataset]
            self.dataset_to_correlation[dataset] = str(current_combo.currentText())

        self.close()


gui_home = HomeWindow()
gui_home.show()
sys.exit(app.exec_())
