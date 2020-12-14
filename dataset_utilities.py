"""
Creates a data class Country. It also creates the clean dataset devoid of the unnecessary columns
and maps the values to the corresponding countries for every factor.
"""
from typing import Dict, Optional, List
import csv
from dataclasses import dataclass
from datetime import datetime
import warnings
import os


@dataclass
class Country:
    """Class for maintaining information about each country

    Instance Attributes:
        - name: The name of the country.
        - gdp: The country's gdp.
        - factors: The different factors affecting climate
                    based on Responsibility Datasets directory

    Representation Invariants:
        - self.name != ''
        - self.gdp > 0.0
    """
    name: str
    gdp: float
    factors: dict


def _extract_wanted_column(file_name: str, dependent_column: str, independent_column='Country Code',
                           back_up_independent_column='Country Name') -> Dict[str, str]:
    """Return two lists which contain the essential columns from the input csv files
    for further processing.

    Precondition:
        - filepath refers to a csv file with 2 or more columns
        - first and second column strings are present in the csv header

    >>> _extract_wanted_column(os.path.join(
    ...                                     'Responsibility '
    ...                                     'Datasets/'
    ...                                     'GDP.csv'), '2014')['CAN']
    '1803533209844.65'
    """
    mapping_of_relevant_columns = {}

    with open(file_name) as csvfile:
        reader = csv.reader(csvfile)
        header = next(reader)

        req_i = req_j = back_up_req_i = -999
        length = len(header)
        for i in range(length):
            if header[i] == independent_column:
                req_i = i
            elif header[i] == dependent_column:
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
                row[back_up_req_i] = _name_to_iso(row[back_up_req_i])
                if row[req_j] != '':
                    mapping_of_relevant_columns[row[back_up_req_i]] = row[req_j]
                else:
                    mapping_of_relevant_columns[row[back_up_req_i]] = -999

    if 'Not Found' in mapping_of_relevant_columns:
        mapping_of_relevant_columns.pop('Not Found')

    return mapping_of_relevant_columns


COUNTRY_CODE_TABLE = _extract_wanted_column(os.path.join('Constant '
                                                         'Datasets/'
                                                         'countries_codes_and_coordinates.csv'),
                                            'Alpha-3 code', independent_column='Country',
                                            back_up_independent_column='')


def _name_to_iso(name_target: str) -> str:
    """Converts the input country name to give to corresponding iso

    Precondition:
        - Name entered is valid

    >>> _name_to_iso('Canada')
    'CAN'
    """
    if name_target in COUNTRY_CODE_TABLE:
        return COUNTRY_CODE_TABLE[name_target]

    return 'Not Found'


def get_raw_datasets(year: str) -> Optional[Dict[str, Dict[str, str]]]:
    """Provide a raw version of the datasets used for computation

    Precondition:
        - At least one csv file in the Constant Computation directory
        - All files are csv files with .csv extension
        - All csv files have a column of either 'Country Name' or 'Country Code'
        as well as a column of the input year

    >>> get_raw_datasets('2014')['Renewable Energy']['CAN']
    '22.024651539556'
    """
    target_path = os.path.join('Responsibility Datasets/')
    files = os.listdir(target_path)
    data_dict = {}

    for name in files:
        data_dict[name[:-4]] = _extract_wanted_column(os.path.join(target_path, name),
                                                      year, 'Country Code',
                                                      'Country Name')

    return data_dict


def map_iso_to_country(year: str) -> Dict[str, Country]:
    """Provides a dictionary mapping the ISO codes to the corresponding country
    dataclass. The dataclass provided has no budget of 0 when initialized.

    Precondition:
        - All csv files have a column of either 'Country Name' or 'Country Code'
        as well as a column of the input year

    >>> Canada = map_iso_to_country('2014')['CAN']
    >>> Canada.name
    'Canada'
    >>> Canada.gdp
    1803533209844.65
    >>> Canada.factors['Carbon Dioxide Emissions']
    540614.809
    """

    code_to_country = {}
    responsibility_datasets = get_raw_datasets(year)

    country_gdp_table = _extract_wanted_column('Constant Datasets/GDP.csv', year)

    for country in COUNTRY_CODE_TABLE:
        country_data_map = {}
        country_iso = COUNTRY_CODE_TABLE[country]

        try:
            for dataset in responsibility_datasets:
                corresponding_data = responsibility_datasets[dataset]
                country_data_map[dataset] = float(corresponding_data[country_iso])

            no_information = any(country_data_map[data_set] == -999
                                 for data_set in country_data_map)

            if not no_information:
                code_to_country[country_iso] = Country(country,
                                                       float(country_gdp_table[country_iso]),
                                                       country_data_map)
            else:
                warnings.warn('Unavailable data for ' + country + ' in ' + year, RuntimeWarning)

        except KeyError:
            warnings.warn('Unavailable data for ' + country + ' in ' + year, RuntimeWarning)

    return code_to_country


def get_clean_datasets(year: str) -> Dict[str, Dict[str, str]]:
    """Provide a final revised dataset for performing computations

    >>> get_clean_datasets('2014')['Climate Risk Index']['CAN']
    102.17
    """
    raw_data_map = get_raw_datasets(year)
    clean_data_map = {}
    mapped_iso_to_country = map_iso_to_country(year)

    for data_key in raw_data_map:
        each_data_map = {}
        for country in raw_data_map[data_key]:
            if country in mapped_iso_to_country:
                each_data_map[country] = mapped_iso_to_country[country].factors[data_key]

        clean_data_map[data_key] = each_data_map

    return clean_data_map


def possible_years() -> List[str]:
    """Provides a list of years for which data can be analyzed

    Precondition:
        - All data worth considering is from 1950 and onwards
        - At least one year is common to analyze in all datasets

    >>> possible_years()
    ['2014']
    """
    today = datetime.today()
    current_year = today.year
    possible_year_list = []

    for year in range(1950, current_year + 1):

        year_str = str(year)
        try:
            raw_datasets = get_clean_datasets(year_str)
        except IndexError:
            continue

        is_invalid = False
        if raw_datasets is not None:
            for factor in raw_datasets:
                is_invalid = all(raw_datasets[factor][code] == -999
                                 for code in raw_datasets[factor])

            if not is_invalid:
                possible_year_list.append(year_str)

    return possible_year_list


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)

    import python_ta

    python_ta.check_all(config={
        'extra-imports': ['math'],
        'max-line-length': 100,
        'disable': ['E9999', 'E9970', 'E9998']
    })
