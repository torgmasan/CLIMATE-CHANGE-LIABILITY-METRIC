import sys
from typing import Dict

from PyQt5.QtWidgets import QApplication, QLabel, QComboBox, QLineEdit
from Application.Functionalities.cclm_application_window import CCLMApplicationWindow
from PyQt5 import QtCore
from Application.Layouts.home_user_input_layout import Ui_HomeMainWindow
from Application.Layouts.weightage_user_input_layout import Ui_WeightageMainWindow
from Datasets.dataset_utilities import possible_years, get_raw_datasets

app = QApplication(sys.argv)


class HomeWindow(CCLMApplicationWindow, Ui_HomeMainWindow):
    """Home Screen for CCLM, taking in correlation input from user"""

    def __init__(self) -> None:
        super().__init__()
        self.setupUi(self)
        self.dataset_to_combo_box = {}
        self.dataset_to_correlation = {}

        self.year_drop_down.addItems(possible_years())
        self.populate_grid()

        self.begin_analysis.clicked.connect(self.weight_win_open)

    def populate_grid(self) -> None:
        """Adds required Label and ComboBox items to
        obtain correlation for all csv files in Responsibility Datasets directory

        Preconditions:
            - At least one csv file in Raw Datasets
        """
        temp_combo_year = str(self.year_drop_down.currentText())
        correlation_keys = list(get_raw_datasets(temp_combo_year).keys())
        combo_box_items = ['direct', 'inverse']

        for i in range(len(correlation_keys)):
            label = QLabel(correlation_keys[i])
            label.setAlignment(QtCore.Qt.AlignCenter)
            self.correlation_grid.addWidget(label, i, 0)
            self.dataset_to_combo_box[correlation_keys[i]] = QComboBox()
            current_combo = self.dataset_to_combo_box[correlation_keys[i]]
            current_combo.addItems(combo_box_items)
            self.correlation_grid.addWidget(current_combo, i, 1)

    def weight_win_open(self) -> None:
        """Close the HomeWindow and open the WeightageWindow"""
        for dataset in self.dataset_to_combo_box:
            current_combo = self.dataset_to_combo_box[dataset]
            self.dataset_to_correlation[dataset] = str(current_combo.currentText())

        self.next_win = WeightageWindow(self.dataset_to_correlation)
        super(HomeWindow, self).next_window(self.next_win)


class WeightageWindow(CCLMApplicationWindow, Ui_WeightageMainWindow):
    """Second Screen for CCLM, taking in weightage for each dataset from user"""

    def __init__(self, dataset_to_correlation: Dict[str, str]) -> None:
        super().__init__()
        self.setupUi(self)

        self.dataset_to_correlation = dataset_to_correlation

        self.dataset_to_line_edit = {}
        self.dataset_to_weightage = {}

        self.populate_grid()

    def populate_grid(self) -> None:
        """Adds required Label and QLineEdit items to
        obtain weightage for all csv files in Responsibility Datasets directory

        Preconditions:
            - All user input is 0 <= input <= 100
            - All user input adds up to 100"""
        dataset_keys = list(self.dataset_to_correlation.keys())

        for data_key in dataset_keys:
            label = QLabel(data_key)
            label.setAlignment(QtCore.Qt.AlignCenter)
            self.dataset_to_line_edit[data_key] = QLineEdit()
            current_edit = self.dataset_to_line_edit[data_key]
            current_edit.setFixedWidth(100)
            self.factor_form.addRow(label, current_edit)

        self.factor_form.setSpacing(30)

    def country_list_win_open(self) -> None:
        """Close the WeightageWindow and open the CountryListWindow"""
        pass

    def map_win_open(self) -> None:
        """Close the WeightageWindow and open the MapWindow"""
        pass


gui_home = HomeWindow()
gui_home.show()
sys.exit(app.exec_())
