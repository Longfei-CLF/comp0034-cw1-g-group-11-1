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
from dash.dependencies import Input, Output

#external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]
FONT_AWESOME = "https://use.fontawesome.com/releases/v5.10.2/css/all.css"
external_stylesheets=[dbc.themes.BOOTSTRAP, FONT_AWESOME]

app = dash.Dash(__name__, 
    external_stylesheets=external_stylesheets)
data_path = "Test/volcano_stats/data/Geo_Eruption_Results.xlsx"
df = pd.read_excel(data_path)
country_list = sorted(df.Country.unique())
volcano_list = sorted(df.Vol_name.unique())
VEI_list = sorted(df.VEI.unique())
StaYr_list = sorted(df.Sta_yr.unique())
print(df.info())
print(df[df['VEI']==int('1')])
# Plot figures
def plot_vol_position(df):
    """
    Show the distribution of volcanos https://plotly.com/python/scatter-plots-on-maps/#simple-us-airports-map
    param: df Dataframe the prepared data
    return: positions of volcanos on the map
    rtype: Figure
    """
    fig = px.scatter_geo(df, 
                        lat=df.Latitude,
                        lon=df.Longitude,
                        # color="continent", # which column to use to set the color of markers
                        hover_name="Vol_name", # column added to hover information
                        # size="pop", # size of markers
                        projection="natural earth",
                        title='Distribution of volcanos all over the world'
    )
    return fig

def plot_VEI_density(df):
    """
    Show density of VEI of eruptions disturbted over the world https://plotly.com/python/sliders/
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
                name=str(year)
            )
        ) 

    # Make 1st trace visible
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
    return fig_VEI_density

def plot_NumErup(df):
    """
    Show the trend of number of eruptions verus time  https://plotly.com/python/range-slider/
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
    return fig_NumErup

def plot_ErupDur(df):
    """
    Show the eruption duration of 
    param: df Dataframe the prepared data, xaxis used for plotting
    return: Eruption duration of eruptions
    rtype: Figure
    """
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
        
    fig_ErupDur = px.scatter(df, x=StaYr_list, y=ErupDur_without_Outliner,
                    size=ErupDur_without_Outliner, size_max=60)
    fig_ErupDur.update_layout(
        title_text="The average eruption duration over the years",
        xaxis_title = "Eruption Stating Year",
        yaxis_title = "Average eruption durations (d)"
    )
    return fig_ErupDur

fig_VEI_density = plot_VEI_density(df)
fig_NumErup = plot_NumErup(df)
fig_ErupDur = plot_ErupDur(df)

# App layout
app.layout = html.Div([
    # Introduction Part
    html.Div(children=[
        html.H1(children='Volcano Stats'),
        html.Div(children='''Interested in volcanos? Play around the figures!'''),
        # Filters https://dash.plotly.com/layout
        html.Div(children=[
            html.Label('Choose the country or region'),
            dcc.Dropdown(
                options=[{'label':x, 'value':x} for x in country_list] + [{'label': 'All', 'value': 'all_values'}],
                value='all_values',
                multi=True,
                id='crossfilter_country'
            ),

            html.Label('Choose the volcano eruption index (VEI)'),
            dcc.RadioItems(
                id="crossfilter_VEI",
                options=['1', '2', '3', '4', '5', '6'],
                value='1',
                labelStyle={"display": "inline-block"},
            ),                                
        ],style={'padding': 10, 'flex': 1}),

        dcc.Tabs(id="tabs-graph", value='tab-1-general-analysis', children=[
            dcc.Tab(label='General Analysis', value='tab-1-general-analysis'),
            dcc.Tab(label='Eruption Prediction', value='tab-2-eruption-prediction'),
            dcc.Tab(label='Number of Eruptions', value='tab-3-NumErup'),
            dcc.Tab(label='Eruption Durations', value='tab-4-ErupDur'),
        ]),
        html.Div(id='tabs-content-graph'),
        html.Div(html.P(['Produced by Louis Ng & Longfei C.', html.Br(), 'Last updated: 13/02/2018', html.Br(), 'Data Reference: Global Volcanism Program, 2013. Volcanoes of the World, v. 4.10.5 (27 Jan 2022). Venzke, E (ed.). Smithsonian Institution. Downloaded 13 Feb 2022. https://doi.org/10.5479/si.GVP.VOTW4-2013.']))
    ],),
])

# Card layout 
card = dbc.Card(
    [
        dbc.CardBody(
            [
                html.H4('Test',id='Tot_Erup', className="card-title"),
                html.P(
                    "Total Number of Erputions",
                    className="card-text",
                ),
            ]
        ),
    ],
    style={"width": "18rem"},
)
row = html.Div([
        dbc.CardGroup([
                card,
            ]),
    ], style={'padding': '25px'}
)

# Create Tabs https://dash.plotly.com/dash-core-components/tabs
@app.callback(Output('tabs-content-graph', 'children'),
              Input('tabs-graph', 'value'))
def render_content(tab):
    if tab == 'tab-1-general-analysis':
        return html.Div([
            # Text
            html.Div(children=[
                html.H2(children='General information about volcanos')
            ],),
                     
            html.Div([
                row
            ],),

            # figure
            html.Div([
                html.Div(children=[
                    dcc.Graph(
                    id='General_position',
                    hoverData={'points': [{'customdata': 'Kikai'}]}
                    )
                ],style={'width': '49%', 'padding': '0 20'}),

                html.Div([
                    html.Div([
                        dcc.Graph(id='NumErup')
                    ],style={'width': '49%', 'display': 'inline-block', 'padding': '0 20'}),

                    html.Div([
                        dbc.Card(
                            children = [dbc.CardBody([
                                html.H4("Total number of eruptions", className="card-title"),
                                ], id="Tot_Erup")
                            ]),
                        dbc.Card(
                            children = [dbc.CardBody([
                                html.H4("Total number of eruptions", className="card-title"),
                                ], id="Avg_ErupDur")
                            ]),
                        dbc.Card(
                            children = [dbc.CardBody([
                                html.H4("Total number of eruptions", className="card-title"),
                                ], id="Max_VEI")
                            ]),
                    ],style={'width': '24%', 'display': 'inline-block', 'padding': '0 20'}),
                ],),
            ],),
        ],),

    elif tab == 'tab-2-eruption-prediction':
        # Detailed Analysis
        return html.Div([
            # Text
            html.Div(children=[
                html.H2(children='Volcano Eruption Index')
            ],),
            # figure
            html.Div(children=[
                dcc.Graph(
                id='VEI_density',
                figure=fig_VEI_density)
            ],),
        ],)
    
    elif tab == 'tab-3-NumErup':
        # Detailed Analysis
        return html.Div([
            # Text
            html.Div(children=[
                html.H2(children='Number of Eruptions')
            ],),

            # figure
            html.Div(children=[
                dcc.Graph(
                id='NumErup',
                figure=fig_NumErup)
            ],),
        ],)

    elif tab == 'tab-4-ErupDur':
        # Detailed Analysis
        return html.Div([
            # Text
            html.Div(children=[
                html.H2(children='Eruption Durations')
            ],),

            # Filters
            html.Div(children=[
                html.Label('Choose the country or region'),
                dcc.Dropdown(country_list, ['Japan'], multi=True),
            
                html.Br(),
                html.Label('Choose the VEI'),
                dcc.Checklist(VEI_list, VEI_list, inline=True),
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
                id='ErupDur',
                figure=fig_ErupDur)
            ],),
        ],)

# Callback for changes in country
@app.callback(
    Output('General_position', 'figure'),
    Input('crossfilter_country', 'value'),
    Input('crossfilter_VEI', 'value'),
)
def update_graph(country_value, VEI_value):
    df_VEI = df[df['VEI']==int(VEI_value)]    
    if type(country_value) != list:
        country_value = [country_value]
        if country_value != ['all_values']:
            dff = df_VEI
        else: dff = df_VEI[df_VEI['Country'].isin(country_value)]
    else: dff = df_VEI[df_VEI['Country'].isin(country_value)]
    fig = plot_vol_position(dff)
    fig.update_traces(customdata=dff['Vol_name'])
    fig.update_layout(margin={'l': 40, 'b': 20, 't': 40, 'r': 0}, hovermode='closest')
    return fig

# Callback for number of eruptions with the change in the volcano
@app.callback(
    Output('NumErup', 'figure'),
    Input('General_position', 'hoverData'))
def update_NumErup(hoverData):
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
    return str(len(dff)), sum(dff['Erup_dur']/len(dff)), max(dff['VEI'])



if __name__ == '__main__':
    app.run_server(debug=True)