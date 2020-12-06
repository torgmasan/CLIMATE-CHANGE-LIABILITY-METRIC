from Datasets.dataset_utilities import Country, get_datasets
from typing import Dict
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
    data = get_datasets(year)

    for countries in data[factor]:
        total += data[countries]

    return total


def positive_calculation(factor: str, year: str, country: Country) -> float:
    """Calculates the weighted responsibility if the relation is positive."""
    total_data = calculate_total(factor, year)
    country_data = country.factors[factor]
    calc = country_data / total_data * 100

    return calc


def negative_calculation(factor: str, year: str, country: Country) -> float:
    """Calculates the weighted responsibility if the relation is negative."""
    total_data = calculate_total(factor, year)
    country_data = country.factors[factor]
    sum_so_far = sum([total_data - float(get_datasets(year)[factor][i]) for i in
                      get_datasets(year)[factor]])
    calc = (total_data - country_data) / sum_so_far * 100

    return calc


def unavailable_value(country: Country, weights: Dict[str, float]) -> float:
    """Calculates the split of the weights for responsibility based on the number of\
    unavailable values"""
    count_so_far = 0
    split = 0.0

    for factor in country.factors:
        if country.factors[factor] == -999:
            count_so_far += 1

    for factor in country.factors:
        if country.factors[factor] == -999:
            split += weights[factor] / (len(weights) - count_so_far)
            weights[factor] = 0

    return split


def responsibility(weights: Dict[str, float],
                   country: Country, year: str) -> float:
    """Calculates the responsibility of the given country.

    Preconditions:
        - sum([weights[factor] for factor in country.factors]) == 100.0
        - factor_proportionality.keys() == country.factors.keys()
    """
    weighted_result = 0.0
    score = {}
    split = unavailable_value(country, weights)

    for factor in country.factors:
        if country.factors[factor] != -999:
            if factor_proportionality[factor] == 'direct':
                result = positive_calculation(factor, year, country)
                score[factor] = result
            else:
                result = negative_calculation(factor, year, country)
                score[factor] = result

    for factor in country.factors:
        weighted_result += score[factor] * (weights[factor] + split)

    return weighted_result


def budget_percentage(total_budget: float, country: Country,
                      year: str, weights: Dict[str, float]) -> float:
    """Calculates the budget and the budget percentage based on the responsibility of the country"""
    budget = responsibility(weights, country, year) * total_budget
    percentage = budget / country.gdp * 100
    return percentage
