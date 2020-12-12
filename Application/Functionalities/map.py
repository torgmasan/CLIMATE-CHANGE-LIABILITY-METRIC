"""
Displays a choropleth map using the computation result of budget details
and displays them based on each country's data on each factor.
Color coded based on budget but it also displays the budget percentage.
"""
from typing import Dict, Tuple
import plotly.express as px
import pandas
from Computation.dataset_utilities import map_iso_to_country
from Computation.computation import budget_details, set_up_computation


def _plot(total_budget: float, factor_proportionality: Dict[str, str], weights: Dict[str, float],
          year: str) -> Dict[str, Tuple[float, float]]:
    """information for the graph to be plotted."""
    percentage_values = {}
    data = map_iso_to_country(year)
    for code in data:
        percentage_values[code] = budget_details(total_budget, data[code],
                                                 factor_proportionality, weights)
    return percentage_values


def run(total_budget: float, factor_proportionality: Dict[str, str], weights: Dict[str, float],
        year: str) -> None:
    """Plots the graph with the passed parameters"""

    map_data = map_iso_to_country('2014')
    set_up_computation(year)
    output = _plot(total_budget, factor_proportionality, weights, year)
    d = {'Iso Code': output.keys(),
         'Budget': [output[code][0] for code in output],
         'Budget Percentage': [output[code][1] for code in output],
         'Country Name': [map_data[code].name for code in map_data],
         'Renewable Energy': [map_data[code].factors['Renewable Energy'] for code in map_data],
         'CO2 Emissions': [map_data[code].factors['Carbon Dioxide Emissions'] for code in map_data],
         'Climate Risk Index': [map_data[code].factors['Climate Risk Index'] for code in map_data],
         'GDP': [map_data[code].factors['GDP'] for code in map_data]}
    df = pandas.DataFrame(data=d)
    fig = px.choropleth(df, locations="Iso Code",
                        color="Budget",
                        hover_name="Country Name",
                        hover_data=['Renewable Energy', 'CO2 Emissions', 'Climate Risk Index',
                                    'GDP', 'Budget Percentage'],
                        color_continuous_scale=px.colors.sequential.Plasma)
    fig.show()


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)

    import python_ta

    python_ta.check_all(config={
        'extra-imports': ['math'],
        'max-line-length': 100,
        'disable': ['E0401', 'E9999', 'E0611']
    })
