# Copied from the Dash tutorial documentation at https://dash.plotly.com/layout on 24/05/2021
# Import section modified 10/10/2021 to comply with changes in the Dash library.

# Run this app with `python dash_app.py` and visit http://127.0.0.1:8050/ in your web browser.

import dash
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import numpy as np
from dash import dcc
from dash import html
import plotly.graph_objs as go

external_stylesheets = ["https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0/css/materialize.min.css"]

app = dash.Dash(__name__, 
    external_stylesheets=external_stylesheets)

data = "volcano_stats/data/Geo_Eruption_Results.xlsx"
df = pd.read_excel(data)
country_list = sorted(df.Country.unique())
volcano_list = sorted(df.Country.unique())
VEI_list = sorted(df.VEI.unique())
StaYr_list = sorted(df.Sta_yr.unique())

# Create figure for distributtion of volcanos https://plotly.com/python/scatter-plots-on-maps/#simple-us-airports-map
# fig_position_scatter = go.figure(data=go.Choropleth(
#     locations = df['Code'],
#     z = df['VEI'],
#     text = df['Country'],
#     colorscale = 'Blues',
#     autocolorscale=False,
#     reversescale=True,
#     marker_line_color='darkgray',
#     marker_line_width=0.5,
#     #colorbar_tickprefix = '$',
#     colorbar_title = 'VEI',
# ))

fig_vol_position = px.scatter_geo(df, 
                    lat=df.Latitude,
                    lon=df.Longitude,
                    # color="continent", # which column to use to set the color of markers
                    hover_name="Vol_name", # column added to hover information
                    # size="pop", # size of markers
                    projection="natural earth",
                    title='Distribution of volcanos all over the world')

# Create figure for VEI density https://plotly.com/python/sliders/
fig_VEI_density = go.Figure()
data_slider = []
for year in df['Sta_yr'].unique():
    df_segmented =  df[(df['Sta_yr']== year)]
    fig_VEI_density.add_trace(
        go.Densitymapbox(
            visible=False,
            lat=df_segmented.Latitude,
            lon=df_segmented.Longitude, 
            z=df_segmented.VEI,
            name=str(year)
        )
    )
    
# Make 10th trace visible
fig_VEI_density.data[1].visible = True

# Create and add slider
steps = []
for i in range(len(fig_VEI_density.data)):
    step = dict(
        method="update",
        args=[{"visible": [False] * len(fig_VEI_density.data)},
              {"title": "Slider switched to step: " + str(i+min(df.Sta_yr))}],
        label='{}'.format(i + min(df.Sta_yr))  # layout attribute
    )
    step["args"][0]["visible"][i] = True  # Toggle i'th trace to "visible"
    steps.append(step)

sliders = [dict(
    active=1,
    currentvalue={"prefix": "Starting Year: "},
    pad={"t": 1},
    steps=steps
)]

fig_VEI_density.update_layout(sliders=sliders, title='The volcano eruption index (VEI) of each eruptions over the years')
fig_VEI_density.update_layout(mapbox_style="stamen-terrain", mapbox_center_lon=180)
# fig_VEI_density.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

# Create figure for eruptions over time https://plotly.com/python/range-slider/
"""
Show the trend of number of eruptions verus time
param: df Dataframe the prepared data, xaxis used for plotting
return: Line plot of number of eruptions over time
"""
NumErup = []
for i in StaYr_list:
    count = 0
    for x in df.Sta_yr:
        if i == x:
            count = count + 1
    NumErup.append(count)

# Create figure
fig_NumErup = go.Figure()
fig_NumErup.add_trace(
    go.Scatter(x=StaYr_list, y=NumErup))

# Set title
fig_NumErup.update_layout(
    title_text="Number of eruptions over the years"
)

# Add range slider
fig_NumErup.update_layout(
    xaxis=dict(
        rangeselector=dict(
            buttons=list([
                dict(count=1,
                     label="YTD",
                     step="year",
                     stepmode="todate"),
                dict(count=1,
                     label="1y",
                     step="year",
                     stepmode="backward"),
                dict(step="all")
            ])
        ),
        rangeslider=dict(
            visible=True
        ),
        type="date"
    )
)

ErupDur_without_Outliner = []
for i in StaYr_list:
    dur_without_Outliner = []
    row = 0
    for x in df.Sta_yr:
        if i == x:
            day = df.loc[row, 'Erup_dur']
            if day < 10000:
                dur_without_Outliner.append(day)
        row = row + 1
    if sum(dur_without_Outliner) == 0:
        ErupDur_without_Outliner.append(0)
    else:
        ErupDur_without_Outliner.append(np.mean(dur_without_Outliner))
    
fig_ErupDur = px.scatter(df, x=StaYr_list, y=NumErup,
                size=ErupDur_without_Outliner, size_max=60)
fig_ErupDur.update_layout(
    title_text="The average eruption duration over the years",
    xaxis_title = "Eruption Stating Year",
    yaxis_title = "Average eruption durations (d)"
)

app.layout = html.Div([
    # Introduction Part
    html.Div(children=[
        html.H1(children='Volcano Stats'),
        html.Div(children='''Looking for some volcanos? Produced by Louis W. & Longfei C.'''),
    ],),

    # General Analysis
    html.Div([
        # Text
        html.Div(children=[
            html.H2(children='General information about volcanos')
        ],),

        # Filters https://dash.plotly.com/layout
        html.Div(children=[
            html.Label('Choose the country or region'),
            dcc.Dropdown(country_list, ['Japan'], multi=True),

            # html.Br(),
            # html.Label('Slider'),
            # dcc.Slider(
            # min=min(df['Sta_yr']),
            # max=max(df['Sta_yr']),
            # #marks={i: f'Label {i}' if i == 1 else str(i) for i in range(1, 6)},
            # value=1,
            # ),
        ],style={'padding': 10, 'flex': 1}),

        # figure
        html.Div(children=[
            dcc.Graph(
            id='General_position',
            figure=fig_vol_position)
        ],),
    ],),

    # Detailed Analysis
    html.Div([
        # Text
        html.Div(children=[
            html.H2(children='Details Analysis')
        ],),

        # Filters
        html.Div(children=[
            html.Label('Choose the country or region'),
            dcc.Dropdown(country_list, ['Japan'], multi=True),
        
            html.Br(),
            html.Label('Choose the VEI'),
            dcc.Checklist(['1', '2'], ['1']),
            # html.Br(),
            # html.Label('Slider'),
            # dcc.Slider(
            # min=min(df['Sta_yr']),
            # max=max(df['Sta_yr']),
            # #marks={i: f'Label {i}' if i == 1 else str(i) for i in range(1, 6)},
            # value=1,
            # ),
        ],style={'padding': 10, 'flex': 1}),

        # figure
        html.Div(children=[
            dcc.Graph(
            id='VEI_density',
            figure=fig_VEI_density)
        ],),

        # figure
        html.Div(children=[
            dcc.Graph(
            id='NumErup',
            figure=fig_NumErup)
        ],),
        
        # figure
        html.Div(children=[
            dcc.Graph(
            id='ErupDur',
            figure=fig_ErupDur)
        ],),
    ],)
])


if __name__ == '__main__':
    app.run_server(debug=True)