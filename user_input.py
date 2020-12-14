"""
This script contains all windows that are displayed
when the program is run. It is responsible for User interaction
of all sorts, through GUI.
"""

import sys
from typing import Dict

from PyQt5.QtWidgets import QApplication, QLabel, QComboBox, QLineEdit, QDialog
from PyQt5 import QtCore
from cclm_application_window import CCLMApplicationWindow
from home_user_input_layout import Ui_HomeMainWindow
from precondition_failed_dialog import Ui_Dialog
from weightage_user_input_layout import Ui_WeightageMainWindow
from map import run
from dataset_utilities import possible_years, get_raw_datasets

app = QApplication(sys.argv)


class WarnDialog(QDialog, Ui_Dialog):
    """Dialog Screen that alerts user if input that
    violates Preconditions is entered."""
    def __init__(self) -> None:
        super().__init__()
        self.setupUi(self)


class HomeWindow(CCLMApplicationWindow, Ui_HomeMainWindow):
    """Home Screen for CCLM, taking in correlation input from user

        Instance Attributes:
            - dataset_to_combo_box: dictionary mapping factors to the
            combo_box that determines it's correlation.
            - dataset_to_correlation: dictionary mapping factor to correlation

        Representation Invariants:
            - self.dataset_to_combo_box != {}
            - self.dataset_to_correlation != {}
    """
    dataset_to_combo_box: Dict
    dataset_to_correlation: Dict

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
        obtain correlation for all csv files in Responsibility Computation directory

        Preconditions:
            - At least one csv file in Raw Computation
        """
        temp_combo_year = str(self.year_drop_down.currentText())
        correlation_keys = list(get_raw_datasets(temp_combo_year).keys())
        combo_box_items = ['direct', 'inverse']
        length = len(correlation_keys)
        for i in range(length):
            label = QLabel(correlation_keys[i])
            label.setAlignment(QtCore.Qt.AlignCenter)
            self.correlation_grid.addWidget(label, i, 0)
            self.dataset_to_combo_box[correlation_keys[i]] = QComboBox()
            current_combo = self.dataset_to_combo_box[correlation_keys[i]]
            if correlation_keys[i] == 'Renewable Energy':
                # Since it is known that the default dataset Renewable Energy
                # is inversely correlated, the combo items have been switched.
                # Nevertheless, user still has authority to switch to direct
                current_combo.addItems(['inverse', 'direct'])
            else:
                current_combo.addItems(combo_box_items)
            self.correlation_grid.addWidget(current_combo, i, 1)

    def weight_win_open(self) -> None:
        """Close the HomeWindow and open the WeightageWindow"""
        combo_year = str(self.year_drop_down.currentText())

        for dataset in self.dataset_to_combo_box:
            current_combo = self.dataset_to_combo_box[dataset]
            self.dataset_to_correlation[dataset] = str(current_combo.currentText())

        self.next_win = WeightageWindow(combo_year, self.dataset_to_correlation)
        super(HomeWindow, self).next_window()


class WeightageWindow(CCLMApplicationWindow, Ui_WeightageMainWindow):
    """Second Screen for CCLM, taking in weightage for each dataset from user

        Instance Attributes:
            - dataset_to_line_edit: dictionary mapping factors to the
            line_edit that determines it's weightage.
            - dataset_to_correlation: dictionary mapping factor to correlation
            - dataset_to_weightage: dictionary mapping factor to weightage

        Representation Invariants:
            - self.dataset_to_combo_box != {}
            - self.dataset_to_correlation != {}
            - self.dataset_to_weightage != {}
    """
    dataset_to_correlation: Dict[str, str]
    year: str
    dataset_to_line_edit: Dict
    dataset_to_weightage: Dict

    def __init__(self, year: str, dataset_to_correlation: Dict[str, str]) -> None:
        super().__init__()
        self.setupUi(self)

        self.dataset_to_correlation = dataset_to_correlation
        self.year = year

        self.dataset_to_line_edit = {}
        self.dataset_to_weightage = {}

        self.populate_grid()

        self.display_analysis.clicked.connect(self.map_win_open)

    def populate_grid(self) -> None:
        """Adds required Label and QLineEdit items to
        obtain weightage for all csv files in Responsibility Computation directory

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

    def precondition_evaluation(self) -> bool:
        """Evaluate all user input and check if it satisfies all
        preconditions of following functions involved in computation.
        """
        try:
            total_budget = float(self.budget.text())
            is_budget_valid = total_budget >= 1000000

            for line_edit in self.dataset_to_line_edit:
                self.dataset_to_weightage[line_edit] = self.dataset_to_line_edit[line_edit].text()

            is_sum_valid = sum(float(self.dataset_to_weightage[dataset])
                               for dataset in self.dataset_to_weightage) == 100

            is_factor_valid = all(float(self.dataset_to_weightage[dataset]) >= 0
                                  for dataset in self.dataset_to_weightage)

            if is_factor_valid and is_sum_valid and is_budget_valid:
                return True

            error_dialog = WarnDialog()
            error_dialog.exec_()
            return False

        except ValueError:
            error_dialog = WarnDialog()
            error_dialog.exec_()
            return False

    def map_win_open(self) -> None:
        """Close the WeightageWindow and open the MapWindow"""

        if self.precondition_evaluation():
            total_budget = float(self.budget.text())
            factor_proportionality = {data_name: self.dataset_to_correlation[data_name]
                                      for data_name in self.dataset_to_correlation}
            weights = {data_name: float(self.dataset_to_weightage[data_name]) / 100
                       for data_name in self.dataset_to_correlation}

            run(total_budget, factor_proportionality,
                weights, self.year)
            self.next_window()


def run_app() -> None:
    """Runs the home application"""
    gui_home = HomeWindow()
    gui_home.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)

    import python_ta

    python_ta.check_all(config={
        'extra-imports': ['math'],
        'max-line-length': 100,
        'disable': ['E9997', 'E9999', 'E0611', 'E0401']
    })
