from Datasets.dataset_utilities import Country, get_clean_datasets
from typing import Dict


def _calculate_total(factor: str, year: str) -> float:
    """Calculates the total of the factor passed"""
    total = 0.0
    data = get_clean_datasets(year)

    for countries in data[factor]:
        total += data[countries]

    return total


def _positive_calculation(factor: str, year: str, country: Country) -> float:
    """Calculates the weighted responsibility if the relation is positive."""
    total_data = _calculate_total(factor, year)
    country_data = country.factors[factor]
    calc = country_data / total_data * 100

    return calc


def _negative_calculation(factor: str, year: str, country: Country) -> float:
    """Calculates the weighted responsibility if the relation is negative."""
    total_data = _calculate_total(factor, year)
    country_data = country.factors[factor]
    sum_so_far = sum([total_data - float(get_clean_datasets(year)[factor][i]) for i in
                      get_clean_datasets(year)[factor]])
    calc = (total_data - country_data) / sum_so_far * 100

    return calc


def _unavailable_value(country: Country, weights: Dict[str, float]) -> float:
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
    split = _unavailable_value(country, weights)
    total = 0
    for factor in country.factors:
        if country.factors[factor] != -999:
            if factor_proportionality[factor] == 'direct':
                result = _positive_calculation(factor, year, country)
                score[factor] = result
            else:
                result = _negative_calculation(factor, year, country)
                score[factor] = result
    for value in weights:
        total += weights[value]
    for factor in country.factors:
        weighted_result += score[factor] * (weights[factor] + split)

    return weighted_result / total


def budget_percentage(total_budget: float, country: Country,
                      year: str, weights: Dict[str, float]) -> float:
    """Calculates the budget and the budget percentage based on the responsibility of the country"""
    budget = responsibility(weights, country, year) * total_budget
    percentage = budget / country.gdp * 100
    return percentage
