from Computation.dataset_utilities import Country, get_clean_datasets
from typing import Dict
from fractions import Fraction
CLEAN_DATASET = {}


def set_up_computation(year: str) -> None:
    """Decrease computation time by calling the clean
    dataset once and providing th value to global constant

    Precondition:
        - Must be called before any computation is done.
    """
    global CLEAN_DATASET
    CLEAN_DATASET = get_clean_datasets(year)


def _calculate_total(factor: str) -> float:
    """Calculates the total of the factor passed"""
    total = 0.0

    for countries in CLEAN_DATASET[factor]:
        if CLEAN_DATASET[factor][countries] != -999:
            total += CLEAN_DATASET[factor][countries]

    return total


def _positive_calculation(factor: str, country: Country) -> Fraction:
    """Calculates the weighted responsibility if the relation is positive."""
    total_data = _calculate_total(factor)
    country_data = country.factors[factor]
    calc = Fraction(country_data / total_data * 100)

    return calc


def _negative_calculation(factor: str, country: Country) -> Fraction:
    """Calculates the weighted responsibility if the relation is negative."""
    total_data = _calculate_total(factor)
    country_data = country.factors[factor]
    sum_so_far = sum([total_data - float(CLEAN_DATASET[factor][i]) for i in
                      CLEAN_DATASET[factor]])
    calc = Fraction((total_data - country_data) / sum_so_far * 100)

    return calc


def _unavailable_value(country: Country, weights: Dict[str, float]) -> float:
    """Calculates the split of the weights for responsibility based on the number of
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
                   country: Country, factor_proportionality: Dict[str, str]) -> Fraction:
    """Calculates the responsibility of the given country.

    Preconditions:
        - sum([weights[factor] for factor in country.factors]) == 100.0
        - factor_proportionality.keys() == country.factors.keys()
    """
    weighted_result = Fraction(0.0)
    score = {}
    split = _unavailable_value(country, weights)

    for factor in country.factors:
        if country.factors[factor] != -999:
            if factor_proportionality[factor] == 'direct':
                result = Fraction(_positive_calculation(factor, country))
            else:
                result = Fraction(_negative_calculation(factor, country))

            score[factor] = result

    for factor in score:
        weighted_result += Fraction(score[factor] * (weights[factor] + split))

    return weighted_result


def budget_percentage(total_budget: float, country: Country,
                      factor_proportionality: Dict[str, str], weights: Dict[str, float]) -> float:
    """Calculates the budget and the budget percentage based on the responsibility of the country

    factor_proportionality = inverse or direct
    factor_proportionality.keys() == weights.keys()
    total_budget >= 1,000,000
    """

    budget = responsibility(weights, country, factor_proportionality) * total_budget
    percentage = budget / country.gdp * 100
    return percentage