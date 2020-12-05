from typing import Dict
import csv
from dataclasses import dataclass
import warnings
import os


@dataclass
class Country:
    """Class for maintaining information about each country"""
    name: str
    gdp: float
    factors: dict


def extract_wanted_column(file_name: str, dependant_column: str, indepenent_column='Country Code',
                          back_up_independent_column='Country Name') -> Dict[str, str]:
    """Return two lists on which contain the essential columns from the input csv files for further processing.

    Precondition:
        - filepath refers to a csv file with 2 or more columns
        - first and second column strings are present in the csv header
    """
    mapping_of_relevant_columns = {}

    with open(file_name) as csvfile:
        reader = csv.reader(csvfile)
        header = next(reader)

        req_i = req_j = back_up_req_i = -999

        for i in range(len(header)):
            if header[i] == indepenent_column:
                req_i = i
            elif header[i] == dependant_column:
                req_j = i
            elif header[i] == back_up_independent_column:
                back_up_req_i = i

        for row in reader:
            if req_i != -999:
                if row[req_j] != '':
                    mapping_of_relevant_columns[row[req_i]] = row[req_j]
                else:
                    mapping_of_relevant_columns[row[req_i]] = -999

            else:
                row[back_up_req_i] = name_to_iso(row[back_up_req_i])
                if row[req_j] != '':
                    mapping_of_relevant_columns[row[back_up_req_i]] = row[req_j]
                else:
                    mapping_of_relevant_columns[row[back_up_req_i]] = -999

    if 'Not Found' in mapping_of_relevant_columns:
        mapping_of_relevant_columns.pop('Not Found')

    return mapping_of_relevant_columns


COUNTRY_CODE_TABLE = extract_wanted_column('../Raw Datasets/Constant Datasets/countries_codes_and_coordinates.csv',
                                           'Alpha-3 code', indepenent_column='Country', back_up_independent_column='')


def name_to_iso(name_target: str) -> str:
    """Converts the input country name to give to corresponding iso

    Precondition:
        name entered is valid
    """
    if name_target in COUNTRY_CODE_TABLE:
        return COUNTRY_CODE_TABLE[name_target]
    else:
        return 'Not Found'


def get_datasets(year: str) -> Dict[str, Dict[str, str]]:
    """Creates a map from the datasets that determine the responsibility
    of each country

    Precondition:
        - At least one csv file in the Constant Datasets directory
        - All files are csv files with .csv extension
        - All csv files have a column of either 'Country Name' or 'Country Code'
        as well as a column of the input year
    """
    current_path = os.getcwd()
    target_path = os.path.join(current_path, '../Raw Datasets/Responsibility Datasets/')
    files = os.listdir(target_path)
    data_dict = {}

    for name in files:
        data_dict[name[:-4]] = extract_wanted_column(os.path.join(target_path, name), year, 'Country Code',
                                                     'Country Name')

    return data_dict


def map_iso_to_country(year: str) -> Dict[str, Country]:
    """Provides a dictionary mapping the ISO codes to the corresponding country
    dataclass. The dataclass provided has no budget of 0 when initialized.

    Precondition:
        - All csv files have a column of either 'Country Name' or 'Country Code'
        as well as a column of the input year
    """

    code_to_country = {}
    responsibility_datasets = get_datasets(year)

    country_gdp_table = extract_wanted_column('../Raw Datasets/Constant Datasets/gdp_total.csv', year)

    for country in COUNTRY_CODE_TABLE:
        country_data_map = {}
        country_iso = COUNTRY_CODE_TABLE[country]

        try:
            for dataset in responsibility_datasets:
                corresponding_data = responsibility_datasets[dataset]
                country_data_map[dataset] = float(corresponding_data[country_iso])

            code_to_country[country_iso] = Country(country, float(country_gdp_table[country_iso]), country_data_map)

        except KeyError:
            warnings.warn('Unavailable data for ' + country, RuntimeWarning)

    return code_to_country
