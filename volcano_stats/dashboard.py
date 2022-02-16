# Copied from the Dash tutorial documentation at https://dash.plotly.com/layout on 24/05/2021

# Run this app with `python dash_app.py` and visit http://127.0.0.1:8050/ in your web browser.
import dash
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import numpy as np
from dash import dcc
from dash import html
import plotly.graph_objs as go
from dash.dependencies import Input, Output

FONT_AWESOME = "https://use.fontawesome.com/releases/v5.10.2/css/all.css"
external_stylesheets=[dbc.themes.BOOTSTRAP, FONT_AWESOME]

app = dash.Dash(__name__, 
    external_stylesheets=external_stylesheets, suppress_callback_exceptions=True)
data_path = "volcano_stats/data/Geo_Eruption_Results.xlsx"
df = pd.read_excel(data_path)
country_list = sorted(df.Country.unique())
volcano_list = sorted(df.Vol_name.unique())
VEI_list = sorted(df.VEI.unique())
StaYr_list = sorted(df.Sta_yr.unique())

# Plot figures
def plot_vol_position(df):
    """
    Show the distribution of volcanos
    param: df Dataframe the prepared data
    return: positions of volcanos on the map
    rtype: Figure
    """
    fig = px.scatter_geo(df, 
                        lat=df.Latitude,
                        lon=df.Longitude,
                        hover_name="Vol_name",
                        projection="natural earth",
    )

    # Set layout
    fig.update_layout(
        title="Distribution of volcanos all over the world",
    )
    return fig

def plot_NumErup(df):
    """
    Show the trend of number of eruptions verus time
    param: df Dataframe the prepared data, xaxis used for plotting
    return: Line plot of number of eruptions over time
    rtype: Figure
    """
    # Prepare data
    NumErup = []
    for i in StaYr_list:
        count = 0
        for x in df.Sta_yr:
            if i == x:
                count = count + 1
        NumErup.append(count)

    # Create figure
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(x=StaYr_list, y=NumErup))

    # Set layout
    fig.update_layout(
        title="Number of eruptions over the years",
        xaxis_title="Starting Year",
        yaxis_title="Number of Eruptions",
    )

    # Add range slider
    fig.update_layout(
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
    return fig

def plot_VEI_density(df):
    """
    Show density of VEI of eruptions disturbted over the world
    param: df Dataframe the prepared data
    return: density of VEI of eruptions
    rtype: Figure
    """
    # Create figure for each year
    fig_VEI_density = go.Figure()
    for year in df['Sta_yr'].unique():
        df_segmented =  df[(df['Sta_yr']== year)]
        fig_VEI_density.add_trace(
            go.Densitymapbox(
                visible=False,
                lat=df_segmented.Latitude,
                lon=df_segmented.Longitude, 
                z=df_segmented.VEI,
                name='',
            )
        )

    # Make 1st trace visible
    if len(df) != 0:
        fig_VEI_density.data[1].visible = True

    # Create and add slider
    steps = []
    for i in range(len(fig_VEI_density.data)):
        step = dict(
            method="update",
            args=[{"visible": [False] * len(fig_VEI_density.data)}],
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

    fig_VEI_density.update_layout(sliders=sliders)
    fig_VEI_density.update_layout(mapbox_style="stamen-terrain", mapbox_center_lon=180)
    fig_VEI_density.update_layout(
        title='The volcano eruption index (VEI) of each eruptions over the years',
        xaxis_title="Starting Year"
    )    
    return fig_VEI_density

def plot_NumErup_Dur(df):
    """
    Show the trend of number of eruptions and durations verus time
    param: df Dataframe the prepared data, xaxis used for plotting
    return: Line plot of number of eruptions and durations over time
    rtype: Figure
    """
    # Prepare data
    NumErup = []
    for i in StaYr_list:
        count = 0
        for x in df.Sta_yr:
            if i == x:
                count = count + 1
        NumErup.append(count)

    ErupDur = []
    for i in StaYr_list:
        dur = np.mean(df[df['Sta_yr'] == i]['Erup_dur'])
        ErupDur.append(dur)

    # Create figure
    fig = go.Figure()
    fig = px.scatter(df, x=StaYr_list, y=ErupDur,
                    size=NumErup, size_max=60)

    # Set layout
    fig.update_layout(
        title="Number of eruptions & durations over the years",
        xaxis_title="Starting Year",
        yaxis_title="Average Eruption Durations (days)",
    )

    # Add range slider
    fig.update_layout(
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
    return fig

# Callback for tabs
@app.callback(Output('tabs-content-graph', 'children'),
              Input('tabs-graph', 'value'))
def render_content(tab):
    if tab == 'tab-1-overview':
        return html.Div([
            # Text
            html.Div(children=[
                html.H2(children='General information about volcanos')
            ],),

            html.Div([
                dbc.Card(
                    children=[dbc.CardBody([
                        html.H4("Total number of eruptions", className="card-title"),
                    ], id="Tot_Erup")
                    ], style={'width': '33%', 'display': 'inline-block'}),
                dbc.Card(
                    children=[dbc.CardBody([
                        html.H4("Average Eruption Duration (Days)", className="card-title"),
                    ], id="Avg_ErupDur")
                    ], style={'width': '33%', 'display': 'inline-block'}),
                dbc.Card(
                    children=[dbc.CardBody([
                        html.H4("Max VEI", className="card-title"),
                    ], id="Max_VEI")

                    ], style={'width': '33%', 'display': 'inline-block'}),
            ]),

            html.Div([
                dbc.Card(
                    children=[dbc.CardBody([
                        html.H4("Total number of eruptions", className="card-title"),
                    ], id="Tot_Erup")
                    ], style={'width': '33%', 'display': 'inline-block'}),
                dbc.Card(
                    children=[dbc.CardBody([
                        html.H4("Total number of eruptions", className="card-title"),
                    ], id="Avg_ErupDur")
                    ], style={'width': '33%', 'display': 'inline-block'}),
                dbc.Card(
                    children=[dbc.CardBody([
                        html.H4("Total number of eruptions", className="card-title"),
                    ],  id="Max_VEI")
                    ], style={'width': '33%', 'display': 'inline-block'}),
            ]),

            # figure
            html.Div([
                html.Div(children=[
                    dcc.Graph(
                    id='General_position',
                    hoverData={'points': [{'customdata': 'Kikai'}]}
                    ),
                ],style={'width': '50%', 'padding': '0 20','display': 'inline-block'}),

                html.Div([
                        dcc.Graph(id='NumErup')
                ],style={'width': '50%', 'display': 'inline-block', 'padding': '0 20'}),
            ],),
        ],),

    elif tab == 'tab-2-eruption-prediction':
        # Eruption Predictions
        return html.Div([
            html.Div(children=[
                html.H2(children='Volcano Eruption Index')
            ],),
            html.Div([
                dcc.Graph(id='VEI_density')
            ],style={'width': '99%', 'padding': '0 20'}),

            html.Div(children=[
                html.H2(children='Eruptions')
            ],),
            html.Div([
                dcc.Graph(id='NumErup_Dur')
            ],style={'width': '99%', 'padding': '0 20'}),
        ],)

# Callback for changes in country in positions
@app.callback(
    Output('General_position', 'figure'),
    [Input('crossfilter_country', 'value'),
    Input('crossfilter_VEI', 'value'),
    Input('crossfilter_volcano', 'value')
    ],
)
def update_fig_vol_position(country_value, VEI_value, volcano_value):
    if type(volcano_value) != list:
        volcano_value = [volcano_value]
        if volcano_value == ['all_values']:
            df_vol = df
        else: df_vol = df[df['Vol_name'].isin(volcano_value)]
    else: df_vol = df[df['Vol_name'].isin(volcano_value)]

    df_VEI = df_vol[df_vol['VEI'].isin(VEI_value)]

    if type(country_value) != list:
        country_value = [country_value]
        if country_value == ['all_values']:
            dff = df_VEI
        else: dff = df_VEI[df_VEI['Country'].isin(country_value)]
    else: dff = df_VEI[df_VEI['Country'].isin(country_value)]
    fig = plot_vol_position(dff)
    fig.update_traces(customdata=dff['Vol_name'])
    fig.update_layout(margin={'l': 40, 'b': 20, 't': 40, 'r': 0}, hovermode='closest')
    return fig

# Callback for changes in country in VEI density and eurption durations
@app.callback(
    [Output('VEI_density', 'figure'),
    Output('NumErup_Dur', 'figure')
    ],
    [Input('crossfilter_country', 'value'),
    Input('crossfilter_VEI', 'value'),
    Input('crossfilter_volcano', 'value')
    ],
)
def update_fig_VEI_density_eruptions(country_value, VEI_value, volcano_value):
    if type(volcano_value) != list:
        volcano_value = [volcano_value]
        if volcano_value == ['all_values']:
            df_vol = df
        else: df_vol = df[df['Vol_name'].isin(volcano_value)]
    else: df_vol = df[df['Vol_name'].isin(volcano_value)]

    df_VEI = df_vol[df_vol['VEI'].isin(VEI_value)]

    if type(country_value) != list:
        country_value = [country_value]
        if country_value == ['all_values']:
            dff = df_VEI
        else: dff = df_VEI[df_VEI['Country'].isin(country_value)]
    else: dff = df_VEI[df_VEI['Country'].isin(country_value)]
    fig_VEI_density = plot_VEI_density(dff)
    fig_VEI_density.update_layout(margin={'l': 40, 'b': 20, 't': 40, 'r': 0})
    fig_NumErup_Dur = plot_NumErup_Dur(dff)
    fig_NumErup_Dur.update_layout(margin={'l': 40, 'b': 20, 't': 40, 'r': 0})
    return fig_VEI_density, fig_NumErup_Dur

# Callback for number of eruptions with the change in the volcano
@app.callback(
    Output('NumErup', 'figure'),
    Input('General_position', 'hoverData'))
def update_fig_NumErup(hoverData):
    Vol_name_value = hoverData['points'][0]['customdata']
    dff = df[df['Vol_name'] == Vol_name_value]
    return plot_NumErup(dff)

# Callback for cards 
@app.callback(
    [Output(component_id='Tot_Erup', component_property='children'),
    Output('Avg_ErupDur', 'children'),
    Output('Max_VEI', 'children'),
    ],
    Input('General_position', 'hoverData'))
def update_card_body(hoverData):
    Vol_name_value = hoverData['points'][0]['customdata']
    dff = df[df['Vol_name'] == Vol_name_value]
    return str(len(dff)), round(sum(dff['Erup_dur']/len(dff))), max(dff['VEI'])

# App layout
app.layout = html.Div([
    # Introduction Part
    html.Div(children=[

        html.Div(children=[
            html.Img(
                src="assets/1.png",
                style={"width": "75%", "height": "75%"}),
        ], style={'padding': 10, 'flex': 1, "display": "inline-block"}),
        html.Div(children=[
            html.H1(children='Volcano Stats'),
            html.Div(children='''Professional Vocanol Analysis: Play around with the figures'''),
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
                    value=[1,2,3,4,5,6],
                    labelStyle={"display": "inline-block", },
                ),
            ], style={'padding': 10, 'flex': 1, "display": "inline-block"}),
        ], style={'textAlign': 'center'}),

        html.Br(),
        dcc.Tabs(id="tabs-graph", value='tab-1-overview', children=[
            dcc.Tab(label='Overview', value='tab-1-overview'),
            dcc.Tab(label='Eruption Prediction', value='tab-2-eruption-prediction')
        ]),
        html.Div(id='tabs-content-graph'),

        html.Div(html.P(['Produced by Louis Ng & Longfei C.', html.Br(), 'Last updated: 13/02/2018', html.Br(),
                        'Data Reference: Global Volcanism Program, 2013. Volcanoes of the World, v. 4.10.5 (27 Jan 2022). Venzke, E (ed.). Smithsonian Institution. Downloaded 13 Feb 2022. https://doi.org/10.5479/si.GVP.VOTW4-2013.']))
        ], ),
])

if __name__ == '__main__':
    app.run_server(debug=True)