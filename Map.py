import plotly.express as px

df = px.data.gapminder().query("year==2018")
iso_alpha_list = df['iso_alpha'].to_list()
budget = [0 for _ in range(len(iso_alpha_list))]

df['budget'] = budget
fig = px.choropleth(df, locations="iso_alpha",
                    color="budget",
                    hover_name="country",
                    color_continuous_scale=px.colors.sequential.Plasma)

fig.show()
