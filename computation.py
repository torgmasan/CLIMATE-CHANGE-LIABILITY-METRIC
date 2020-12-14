"""
This is the Computation portion of the application. Its primary purpose
is to calculate the responsibility and budget details(both the actual
budget and the budget percentage).
"""
from typing import Dict, Tuple
from dataset_utilities import Country, get_clean_datasets

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
    """Calculates the total of the factor passed
    >>> set_up_computation('2014')
    >>> _calculate_total('GDP')
    76774314690507.08
    """
    total = 0.0

    for countries in CLEAN_DATASET[factor]:
        if CLEAN_DATASET[factor][countries] != -999:
            total += CLEAN_DATASET[factor][countries]

    return total


def _positive_calculation(factor: str, country: Country) -> float:
    """Calculates the weighted responsibility if the relation is positive.


    >>> from Computation.dataset_utilities import map_iso_to_country
    >>> Canada = map_iso_to_country('2014')['CAN']
    >>> set_up_computation('2014')
    >>> _positive_calculation('Carbon Dioxide Emissions', Canada)
    0.016379052517579262

    """
    total_data = _calculate_total(factor)
    country_data = country.factors[factor]
    calc = country_data / total_data

    return calc


def _negative_calculation(factor: str, country: Country) -> float:
    """Calculates the weighted responsibility if the relation is negative.

    >>> from Computation.dataset_utilities import map_iso_to_country
    >>> Canada = map_iso_to_country('2014')['CAN']
    >>> set_up_computation('2014')
    >>> _negative_calculation('Renewable Energy', Canada)
    0.00607266929574747
    """
    total_data = _calculate_total(factor)
    country_data = country.factors[factor]
    sum_so_far = sum([total_data - float(CLEAN_DATASET[factor][i]) for i in
                      CLEAN_DATASET[factor]])
    calc = (total_data - country_data) / sum_so_far

    return calc


def _responsibility(weights: Dict[str, float],
                    country: Country, factor_proportionality: Dict[str, str]) -> float:
    """Calculates the responsibility of the given country.

    Preconditions:
        - sum([weights[factor] for factor in country.factors]) == 100.0
        - factor_proportionality.keys() == country.factors.keys()

    >>> from Computation.dataset_utilities import map_iso_to_country
    >>> Canada = map_iso_to_country('2014')['CAN']
    >>> set_up_computation('2014')
    >>> w = {'GDP': 25, 'Renewable Energy': 25, 'Carbon Dioxide Emissions': 25, 'Climate Risk Index': 25}
    >>> f = {'GDP': 'direct', 'Renewable Energy': 'inverse',
    ...      'Carbon Dioxide Emissions': 'direct', 'Climate Risk Index': 'direct'}
    >>> _responsibility(w, Canada, f)
    1.3187578635060144
    """
    weighted_result = 0.0
    score = {}

    for factor in country.factors:

        if factor_proportionality[factor] == 'direct':
            result = _positive_calculation(factor, country)
        else:
            result = _negative_calculation(factor, country)

        score[factor] = result

    for factor in score:
        weighted_result += score[factor] * weights[factor]

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

    >>> from Computation.dataset_utilities import map_iso_to_country
    >>> Canada = map_iso_to_country('2014')['CAN']
    >>> set_up_computation('2014')
    >>> w = {'GDP': 25, 'Renewable Energy': 25, 'Carbon Dioxide Emissions': 25, 'Climate Risk Index': 25}
    >>> f = {'GDP': 'direct', 'Renewable Energy': 'inverse',
    ...      'Carbon Dioxide Emissions': 'direct', 'Climate Risk Index': 'direct'}
    >>> budget_details(1000000, Canada, f, w)
    (1318757.8635060145, 7.312079734975369e-05)
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