from typing import Dict
import csv
from dataclasses import dataclass


@dataclass
class Country:
    """Class for maintaining information about each country"""
    name: str
    co2_emissions: float
    gdp_per_capita: float
    renewable_energy_percentage: float
    cri_rank: float
    budget_allotted: float


def extract_wanted_column(file_name: str, first_column_name: str, second_column_name) -> Dict[str, str]:
    """Return two lists on which contain the essential columns from the input csv files for further processing.

    Precondition:
        - filepath refers to a csv file with 2 or more columns
        - first and second column strings are present in the csv header
    """
    mapping_of_relevant_columns = {}

    with open(file_name) as csvfile:
        reader = csv.reader(csvfile)
        header = next(reader)

        req_i = req_j = 0

        for i in range(len(header)):
            for j in range(len(header)):
                if header[i] == first_column_name and header[j] == second_column_name:
                    req_i = i
                    req_j = j

        for row in reader:
            if row[req_j] != '':
                mapping_of_relevant_columns[row[req_i]] = row[req_j]
            else:
                mapping_of_relevant_columns[row[req_i]] = -999

    return mapping_of_relevant_columns


COUNTRY_CODE_TABLE = extract_wanted_column('./Raw Datasets/countries_codes_and_coordinates.csv',
                                           'Alpha-3 code', 'Country', )


def iso_to_name(iso_target: str) -> str:
    """Converts the input iso to give to corresponding country name

    Precondition:
        iso entered is valid
    """
    if iso_target in COUNTRY_CODE_TABLE:
        return COUNTRY_CODE_TABLE[iso_target]
    else:
        return 'Not Found'


def create_dataset() -> Dict[str, Country]:
    """Provides a dictionary mapping the ISO codes to the corresponding country
    dataclass. The dataclass provided has no budget of 0 when initialized.

    Precondition:
        All csv files contain valid information
    """

    dataset_dict = {}

    co2_emissions_data = extract_wanted_column('./Raw Datasets/co2_emissions.csv',
                                               'Country Code', '2014', )
    gdp_per_capita_data = extract_wanted_column('./Raw Datasets/gdp.csv',
                                                'Country Code', '2014', )
    renewable_energy_percentage_data = extract_wanted_column('./Raw Datasets/Renewable Energy.csv',
                                                             'Country Code', '2014', )

    climate_risk_index_data = extract_wanted_column('./Raw Datasets/cri.csv', 'Country Name', 'Score')

    for iso in COUNTRY_CODE_TABLE:
        name = COUNTRY_CODE_TABLE[iso]

        try:
            co2_emissions = float(co2_emissions_data[iso])
            gdp_per_capita = float(gdp_per_capita_data[iso])
            renewable_energy_percentage = float(renewable_energy_percentage_data[iso])
            climate_risk_index = float(climate_risk_index_data[iso_to_name(iso)])

            dataset_dict[iso] = Country(name, co2_emissions, gdp_per_capita, renewable_energy_percentage,
                                        climate_risk_index, 0)

        except KeyError:
            print('LOG: unavailable data for ' + COUNTRY_CODE_TABLE[iso])

    return dataset_dict
