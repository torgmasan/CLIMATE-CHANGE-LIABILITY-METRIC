import plotly.express as px
from typing import Dict
from Datasets.dataset_utilities import map_iso_to_country
from Datasets.computation import budget_percentage
df = px.data.gapminder().query("year==2018")
iso_alpha_list = df['iso_alpha'].to_list()
budget = [0 for _ in range(len(iso_alpha_list))]

df['budget'] = budget
fig = px.choropleth(df, locations="iso_alpha",
                    color="budget",
                    hover_name="country",
                    color_continuous_scale=px.colors.sequential.Plasma)

# fig.show()


def plot(total_budget: float, factor_proportionality: Dict[str, str], weights: Dict[str, float],
         year: str) -> Dict[str, float]:
    """information for the graph to be plotted."""
    percentage_values = {}
    data = map_iso_to_country(year)
    for code in data:
        percentage_values[code] = budget_percentage(total_budget, data[code], factor_proportionality, weights, year)
    return percentage_values
