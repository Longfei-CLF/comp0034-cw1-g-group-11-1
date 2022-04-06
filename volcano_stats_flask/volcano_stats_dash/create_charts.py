
import pandas as pd
import plotly.express as px
import numpy as np
import plotly.graph_objs as go
from pathlib import Path

data_path = Path(__file__).parent.joinpath('data', 'Geo_Eruption_Results.xlsx')


df = pd.read_excel(data_path)
country_list = sorted(df.Country.unique())
volcano_list = sorted(df.Vol_name.unique())
VEI_list = sorted(df.VEI.unique())
StaYr_list = sorted(df.Sta_yr.unique())
all_country_vol_options = {}
for i in country_list:
    all_country_vol_options[i] = list(
        dict.fromkeys(df[df['Country'] == i]['Vol_name']))


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
        df_segmented = df[(df['Sta_yr'] == year)]
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
        fig_VEI_density.data[0].visible = True

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
    fig_VEI_density.update_layout(
        mapbox_style="stamen-terrain", mapbox_center_lon=180)
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
