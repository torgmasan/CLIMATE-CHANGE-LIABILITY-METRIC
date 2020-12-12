import plotly.express as px
from typing import Dict
from Computation.dataset_utilities import map_iso_to_country
from Computation.computation import budget_percentage, set_up_computation
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
        year: str) -> pandas.DataFrame:
    """Plots the graph with the passed parameters"""

    map_data = map_iso_to_country('2014')
    set_up_computation(year)
    output = _plot(total_budget, factor_proportionality, weights, year)
    d = {'Iso Code': [code for code in output],
         'Budget': [output[code] for code in output],
         'Country Name': [map_data[code].name for code in map_data],
         'Renewable Energy': [map_data[code].factors['Renewable Energy'] for code in map_data],
         'CO2 Emissions': [map_data[code].factors['Carbon Dioxide Emissions'] for code in map_data],
         'Climate Risk Index': [map_data[code].factors['Climate Risk Index'] for code in map_data],
         'GDP': [map_data[code].factors['GDP'] for code in map_data]}
    df = pandas.DataFrame(data=d)
    fig = px.choropleth(df, locations="Iso Code",
                        color="Budget",
                        hover_name="Country Name",
                        hover_data=['Renewable Energy', 'CO2 Emissions', 'Climate Risk Index', 'GDP'],
                        color_continuous_scale=px.colors.sequential.Plasma)
    fig.show()
    return df
