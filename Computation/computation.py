"""
This is the Computation portion of the application. Its primary purpose
is to calculate the responsibility and budget details(both the actual
budget and the budget percentage).
"""
from typing import Dict, Tuple
from Computation.dataset_utilities import Country, get_clean_datasets

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


def _positive_calculation(factor: str, country: Country) -> float:
    """Calculates the weighted responsibility if the relation is positive."""
    total_data = _calculate_total(factor)
    country_data = country.factors[factor]
    calc = country_data / total_data

    return calc


def _negative_calculation(factor: str, country: Country) -> float:
    """Calculates the weighted responsibility if the relation is negative."""
    total_data = _calculate_total(factor)
    country_data = country.factors[factor]
    sum_so_far = sum([total_data - float(CLEAN_DATASET[factor][i]) for i in
                      CLEAN_DATASET[factor]])
    calc = (total_data - country_data) / sum_so_far

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
            country.factors[factor] = 0
    return split


def _responsibility(weights: Dict[str, float],
                   country: Country, factor_proportionality: Dict[str, str]) -> float:
    """Calculates the responsibility of the given country.

    Preconditions:
        - sum([weights[factor] for factor in country.factors]) == 100.0
        - factor_proportionality.keys() == country.factors.keys()
    """
    weighted_result = 0.0
    score = {}
    split = _unavailable_value(country, weights)

    for factor in country.factors:
        if country.factors[factor] != -999:
            if factor_proportionality[factor] == 'direct':
                result = _positive_calculation(factor, country)
            else:
                result = _negative_calculation(factor, country)

            score[factor] = result

    for factor in score:
        weighted_result += score[factor] * (weights[factor] + split)

    return weighted_result


def budget_details(total_budget: float, country: Country,
                   factor_proportionality: Dict[str, str],
                   weights: Dict[str, float]) -> Tuple[float, float]:
    """Calculates the budget and the budget percentage based on the responsibility of the country

    Preconditions:
        - all(factor_proportionality[factor] == 'direct' or
        factor_proportionality[factor] == 'inverse' factor in factor_proportionality)
        - factor_proportionality.keys() == weights.keys()
        - total_budget >= 1,000,000
    """
    budget = _responsibility(weights, country, factor_proportionality) * total_budget
    percentage = budget / country.gdp * 100
    return budget, percentage


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)

    import python_ta

    python_ta.check_all(config={
        'extra-imports': ['math'],
        'max-line-length': 100,
        'disable': ['E0611', 'E9999', 'E0401', 'W0603', 'E9997']
    })
