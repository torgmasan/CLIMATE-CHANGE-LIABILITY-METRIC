import plotly.express as px
from typing import Dict, Tuple
from Computation.dataset_utilities import map_iso_to_country
from Computation.computation import budget_details, set_up_computation
import pandas


def _plot(total_budget: float, factor_proportionality: Dict[str, str], weights: Dict[str, float],
          year: str) -> Dict[str, Tuple[float, float]]:
    """information for the graph to be plotted."""
    percentage_values = {}
    data = map_iso_to_country(year)
    for code in data:
        percentage_values[code] = budget_details(total_budget, data[code], factor_proportionality, weights)
    return percentage_values


def run(total_budget: float, factor_proportionality: Dict[str, str], weights: Dict[str, float],
        year: str) -> None:
    """Plots the graph with the passed parameters"""

    map_data = map_iso_to_country(year)
    set_up_computation(year)
    output = _plot(total_budget, factor_proportionality, weights, year)
    d = {'Iso Code': [code for code in output],
         'Budget': [output[code][0] for code in output],
         'Budget Percentage': [output[code][1] for code in output],
         'Country Name': [map_data[code].name for code in map_data]}

    keys = list(factor_proportionality.keys())

    for factor in keys:
        d[factor] = [map_data[code].factors[factor] for code in map_data]

    keys.append('Budget Percentage')

    df = pandas.DataFrame(data=d)
    fig = px.choropleth(df, locations="Iso Code",
                        color="Budget",
                        hover_name="Country Name",
                        hover_data=keys,
                        color_continuous_scale=px.colors.sequential.Plasma)

    fig.show()
