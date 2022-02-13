# Copied from the Dash tutorial documentation at https://dash.plotly.com/layout on 24/05/2021
# Import section modified 10/10/2021 to comply with changes in the Dash library.

# Run this app with `python dash_app.py` and visit http://127.0.0.1:8050/ in your web browser.

import dash
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
from dash import dcc
from dash import html
import plotly.graph_objs as go

external_stylesheets = ["https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0/css/materialize.min.css"]

app = dash.Dash(__name__, 
    external_stylesheets=external_stylesheets)

data = "Test/volcano_stats/data/Geo_Eruption_Results.xlsx"
df = pd.read_excel(data)

print(df.info())

fig = go.Figure(data=go.Choropleth(
    locations = df['Code'],
    z = df['VEI'],
    text = df['Country'],
    colorscale = 'Blues',
    autocolorscale=False,
    reversescale=True,
    marker_line_color='darkgray',
    marker_line_width=0.5,
    #colorbar_tickprefix = '$',
    colorbar_title = 'VEI',
))


# assume you have a "long-form" data frame see https://plotly.com/python/px-arguments/ for more options
"""df = pd.DataFrame({
    "Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
    "Amount": [4, 1, 2, 2, 4, 5],
    "City": ["SF", "SF", "SF", "Montreal", "Montreal", "Montreal"]
})

fig = px.bar(df, 
    x="Fruit", 
    y="Amount",
    color="City", 
    barmode="group"
)"""

app.layout = html.Div(children=[
    html.H1(children='Hello Dash'),
    
    html.Div(children='''
        Dash: A web application framework for Python.
    '''),

    dcc.Graph(
        id='example-graph',
        figure=fig
    )
])


if __name__ == '__main__':
    app.run_server(debug=True)