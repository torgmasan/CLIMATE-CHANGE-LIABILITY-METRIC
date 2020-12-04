import raw_to_clean
from typing import Dict, List, Set
import statistics
import math
""" Computation code:
                TODO LIST:
                    1. Create a dataclass with some instance variables that will be changed.
                    4. Return a dictionary containing the gdp% as well as other factors
                    5. -999 to be distributed to others
                    6. a, b, c, d weights to be included as parameters
                    7. Make the factor dictionary positive or negative.
                    8. Take year as an input.
"""
factor_proportionality = {'Renewable Energy': 'inverse', 'co2_emissions': 'direct', 'cri': 'direct',
                          'gdp_per_capita': 'direct'}


def check_factor(factor: str, proportionality: str) -> None:
    """Checks whether a factor is already in the factor_proportionality dict and adds if not"""
    if factor not in factor_proportionality:
        factor_proportionality[factor] = proportionality


def calculate_total(factor: str, year: str) -> float:
    """Calculates the total of the factor passed"""
    total = 0.0
    data = raw_to_clean.get_datasets(year)
    for countries in data:
        total += data[countries]
    return total


def positive_calculation(factor: str, year: str, country: str) -> float:
    """Calculates the weighted responsibility if the relation is positive."""
    total_data = calculate_total(factor, year)
    country_data = float(raw_to_clean.get_datasets(year)[factor][country])
    calc = country_data / total_data * 100
    return calc


def negative_calculation(factor: str, year: str, country: str) -> float:
    """Calculates the weighted responsibility if the relation is negative."""
    total_data = calculate_total(factor, year)
    country_data = float(raw_to_clean.get_datasets(year)[factor][country])
    sum_so_far = sum([total_data - float(raw_to_clean.get_datasets(year)[factor][i]) for i in
                      raw_to_clean.get_datasets(year)[factor]])
    calc = (total_data - country_data) / sum_so_far * 100
    return calc


def responsibility(a: float, b: float, c: float, d: float,
                   country: raw_to_clean.Country) -> float:
    """Calculates the responsibility of the given country.

    Preconditions:
        - a + b + c + d = 1
        - proportion == 'inverse' or relation == 'direct'
    """
    weighted_result = 0.0

    return weighted_result
