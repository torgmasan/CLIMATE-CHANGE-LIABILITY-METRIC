import plotly.express as px
from typing import Dict
from Datasets.dataset_utilities import map_iso_to_country
from Datasets.computation import budget_percentage, set_up_computation
import pandas


def plot(total_budget: float, factor_proportionality: Dict[str, str], weights: Dict[str, float],
         year: str) -> Dict[str, float]:
    """information for the graph to be plotted."""
    percentage_values = {}
    set_up_computation(year)
    data = map_iso_to_country(year)
    for code in data:
        percentage_values[code] = budget_percentage(total_budget, data[code], factor_proportionality, weights)
    return percentage_values


df = px.data.gapminder().query("year==2018")
iso_alpha_list = df['iso_alpha'].to_list()
budget = [0 for _ in range(len(iso_alpha_list))]

df['budget'] = budget

map_data = map_iso_to_country('2014')
output = plot(1000000, {'Renewable Energy': 'inverse', 'GDP': 'direct', 'Climate Risk Index': 'direct',
                        'Carbon Dioxide Emissions': 'direct'}, {'Renewable Energy': 0.25, 'GDP': 0.25,
                                                                'Climate Risk Index': 0.25,
                                                                'Carbon Dioxide Emissions': 0.25},
              '2014')
d = {'Iso_code': [code for code in output if code != 'ERI'], 'Budget percentage': [output[code] for code in output if code != 'ERI'],
     'Country Name': [map_data[code].name for code in map_data if code != 'ERI']}

df = pandas.DataFrame(data=d)
fig = px.choropleth(df, locations="Iso_code",
                    color="Budget percentage",
                    hover_name="Country Name",
                    color_continuous_scale=px.colors.sequential.Plasma)
fig.show()
