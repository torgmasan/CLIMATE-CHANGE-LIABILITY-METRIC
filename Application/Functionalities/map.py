import plotly.express as px
from typing import Dict
from Datasets.dataset_utilities import map_iso_to_country
from Datasets.computation import budget_percentage, set_up_computation
import pandas


def _plot(total_budget: float, factor_proportionality: Dict[str, str], weights: Dict[str, float],
          year: str) -> Dict[str, float]:
    """information for the graph to be plotted."""
    percentage_values = {}
    data = map_iso_to_country(year)
    for code in data:
        percentage_values[code] = budget_percentage(total_budget, data[code], factor_proportionality, weights)
    return percentage_values


def run(total_budget: float, factor_proportionality: Dict[str, str], weights: Dict[str, float],
        year: str) -> None:
    """Plots the graph with the passed parameters"""

    map_data = map_iso_to_country('2014')
    set_up_computation(year)
    output = _plot(total_budget, factor_proportionality, weights, year)
    d = {'Iso_code': [code for code in output],
         'Budget percentage': [output[code] for code in output],
         'Country Name': [map_data[code].name for code in map_data]}

    df = pandas.DataFrame(data=d)
    fig = px.choropleth(df, locations="Iso_code",
                        color="Budget percentage",
                        hover_name="Country Name",
                        color_continuous_scale=px.colors.sequential.Plasma)
    fig.show()
