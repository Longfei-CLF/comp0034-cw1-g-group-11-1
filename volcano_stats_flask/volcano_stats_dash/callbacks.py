
import pandas as pd
from dash import Output, Input
from dash import html
from dash import dcc
import dash_bootstrap_components as dbc
from pathlib import Path
import volcano_stats_dash.create_charts as cc

data_path = Path(__file__).parent.joinpath('data', 'Geo_Eruption_Results.xlsx')

df = pd.read_excel(data_path)

# Callback for tabs

def register_callbacks(app):
    @app.callback(
        Output('tabs-content-graph', 'children'),
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
                            html.H4("Total number of eruptions",
                                    className="card-title"),
                        ], id="Tot_Erup")
                        ], style={'width': '33%', 'display': 'inline-block'}),
                    dbc.Card(
                        children=[dbc.CardBody([
                            html.H4("Average Eruption Duration (Days)",
                                    className="card-title"),
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
                            html.H4("Total number of eruptions",
                                    className="card-title"),
                        ], id="Tot_Erup")
                        ], style={'width': '33%', 'display': 'inline-block'}),
                    dbc.Card(
                        children=[dbc.CardBody([
                            html.H4("Total number of eruptions",
                                    className="card-title"),
                        ], id="Avg_ErupDur")
                        ], style={'width': '33%', 'display': 'inline-block'}),
                    dbc.Card(
                        children=[dbc.CardBody([
                            html.H4("Total number of eruptions",
                                    className="card-title"),
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
                    ], style={'width': '50%', 'padding': '0 20', 'display': 'inline-block'}),

                    html.Div([
                        dcc.Graph(id='NumErup')
                    ], style={'width': '50%', 'display': 'inline-block', 'padding': '0 20'}),
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
                ], style={'width': '99%', 'padding': '0 20'}),

                html.Div(children=[
                    html.H2(children='Eruptions')
                ],),
                html.Div([
                    dcc.Graph(id='NumErup_Dur')
                ], style={'width': '99%', 'padding': '0 20'}),
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
            else:
                df_vol = df[df['Vol_name'].isin(volcano_value)]
        else:
            df_vol = df[df['Vol_name'].isin(volcano_value)]

        df_VEI = df_vol[df_vol['VEI'].isin(VEI_value)]

        if type(country_value) != list:
            country_value = [country_value]
            if country_value == ['all_values']:
                dff = df_VEI
            else:
                dff = df_VEI[df_VEI['Country'].isin(country_value)]
        else:
            dff = df_VEI[df_VEI['Country'].isin(country_value)]
        fig = cc.plot_vol_position(dff)
        fig.update_traces(customdata=dff['Vol_name'])
        fig.update_layout(
            margin={'l': 40, 'b': 20, 't': 40, 'r': 0}, hovermode='closest')
        return fig

    # Callback for number of eruptions with the change in the volcano


    @app.callback(
        Output('NumErup', 'figure'),
        Input('General_position', 'hoverData'))
    def update_fig_NumErup(hoverData):
        Vol_name_value = hoverData['points'][0]['customdata']
        dff = df[df['Vol_name'] == Vol_name_value]
        return cc.plot_NumErup(dff)

    # Callback for values on the cards


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
            else:
                df_vol = df[df['Vol_name'].isin(volcano_value)]
        else:
            df_vol = df[df['Vol_name'].isin(volcano_value)]

        df_VEI = df_vol[df_vol['VEI'].isin(VEI_value)]

        if type(country_value) != list:
            country_value = [country_value]
            if country_value == ['all_values']:
                dff = df_VEI
            else:
                dff = df_VEI[df_VEI['Country'].isin(country_value)]
        else:
            dff = df_VEI[df_VEI['Country'].isin(country_value)]
        fig_VEI_density = cc.plot_VEI_density(dff)
        fig_VEI_density.update_layout(margin={'l': 40, 'b': 20, 't': 40, 'r': 0})
        fig_NumErup_Dur = cc.plot_NumErup_Dur(dff)
        fig_NumErup_Dur.update_layout(margin={'l': 40, 'b': 20, 't': 40, 'r': 0})
        return fig_VEI_density, fig_NumErup_Dur