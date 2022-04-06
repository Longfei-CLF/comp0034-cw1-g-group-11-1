
from dash import html
from dash import dcc


import pandas as pd
from pathlib import Path

data_path = Path(__file__).parent.joinpath('data', 'Geo_Eruption_Results.xlsx')


df = pd.read_excel(data_path)
country_list = sorted(df.Country.unique())
volcano_list = sorted(df.Vol_name.unique())
VEI_list = sorted(df.VEI.unique())
StaYr_list = sorted(df.Sta_yr.unique())

# App layout
layout = html.Div([
    # Introduction Part
    html.Div(children=[
        html.Div(children=[
            html.H1(children='Volcano Stats'),
            html.Div(
                children='''Professional Vocanol Analysis: Play around with the figures'''),
        ], style={'padding': 10, 'flex': 1, "display": "inline-block"}),

        # Filters
        html.Div(children=[
            html.Div(children=[
                html.Label('Choose the country or region'),
                dcc.Dropdown(
                    options=[{'label': x, 'value': x} for x in country_list] + [
                        {'label': 'All', 'value': 'all_values'}],
                    value='all_values',
                    multi=True,
                    id='crossfilter_country'
                ),
                html.Label('Choose the volcano'),
                dcc.Dropdown(
                    options=[{'label': x, 'value': x} for x in volcano_list] + [
                        {'label': 'All', 'value': 'all_values'}],
                    value='all_values',
                    multi=True,
                    id='crossfilter_volcano'
                ),
            ], style={'padding': 10, 'flex': 1, "width": "30rem", "display": "inline-block"}),

            html.Div(children=[
                html.Br(),
                html.Label('Choose the VEI'),
                dcc.Checklist(
                    id="crossfilter_VEI",
                    options=[{'label': x, 'value': x} for x in VEI_list],
                    value=[1, 2, 3, 4, 5, 6],
                    labelStyle={"display": "inline-block", "width": "15%"},
                ),
            ], style={'padding': 10, 'flex': 1, "display": "inline-block"}),
        ], style={'textAlign': 'center'}),

        html.Br(),
        dcc.Tabs(id="tabs-graph", value='tab-1-overview', children=[
            dcc.Tab(label='Overview', value='tab-1-overview'),
            dcc.Tab(label='Eruption Prediction',
                    value='tab-2-eruption-prediction')
        ]),
        html.Div(id='tabs-content-graph'),

        html.Div(html.P(['Produced by Louis Ng & Longfei C.', html.Br(), 'Last updated: 13/02/2018', html.Br(),
                        'Data Reference: Global Volcanism Program, 2013. Volcanoes of the World, v. 4.10.5 (27 Jan 2022). Venzke, E (ed.). Smithsonian Institution. Downloaded 13 Feb 2022. https://doi.org/10.5479/si.GVP.VOTW4-2013.']))
    ], ),
])
