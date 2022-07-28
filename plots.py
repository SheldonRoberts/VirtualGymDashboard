import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from mpl_toolkits.mplot3d import Axes3D
import plotly.express as px
import plotly.graph_objects as go
from plotly_calplot import calplot
from queries import *

@st.cache
def plot_scatter(df, labels):
    # in unity, z is up and y is forward so we need to flip the z and y
    fig = px.scatter_3d(df,
        x=labels[0],
        y=labels[1],
        z=labels[2],
        labels={
            labels[0]: "X",
            labels[1]: "Y",
            labels[2]: "Z"
    })
    # add an x to the figure at y = 1.5 x = 0 z = 0
    fig.add_trace(go.Scatter3d(x=[0], y=[0], z=[1.4], mode='text', text=['x'], textposition='top center'))
    return fig

def plot_calendar(username: str) -> calplot:
    # display a calendar of the days the user played
    df = days_user_played(username)
    fig = calplot(
            df,
            x="Date",
            y="sessions",
            gap = 1,
            colorscale=[
                    (0.00, "#0E1117"),   (0.33, "#444"),
                    (0.33, "#444"), (0.66, "#999"),
                    (0.66, "#444"),  (1.00, "#DDD")],
            month_lines_width=2

    )
    fig.update_layout(paper_bgcolor="#13161C", plot_bgcolor="#252A33")
    return fig

def plot_hand_replay(session_id: str):
    # display a 3d plot of the hand replay of a session
    # animation function
    data_left, data_right = get_relative_hand_pos(session_id)
    left_xyz = data_left[['x', 'z', 'y']].to_numpy().transpose()
    right_xyz = data_right[['x', 'z', 'y']].to_numpy().transpose()

    # return a simple scatter plot of left_xyz and right_xyz with a 3d axis using plotly
    fig = px.scatter_3d()

    fig.add_trace(
        go.Scatter3d(
            x=left_xyz[0],
            y=left_xyz[1],
            z=left_xyz[2],
            opacity=0.3,
            mode='markers',
            name='left hand positions'
        )
    )
    fig.add_trace(
        go.Scatter3d(
            x=right_xyz[0],
            y=right_xyz[1],
            z=right_xyz[2],
            opacity=0.3,
            mode='markers',
            name="right hand positions"
        )
    )
    # add a red line from 0,0,0 to 0,1,0
    fig.add_trace(
        go.Scatter3d(
            x=[0, 0],
            y=[0, 1],
            z=[0, 0],
            mode='lines',
            line=dict(color='yellow', width=4),
            name="forward facing"

        )
    )
    fig.add_trace(
        go.Scatter3d(
            x=[0, 0],
            y=[0, 0],
            z=[0, -1],
            mode='lines',
            line=dict(color='purple', width=4),
            name="body position"

        )
    )
    fig.update_layout(paper_bgcolor="#13161C", plot_bgcolor="#252A33")
    return fig

def plot_velocity_time(session_id: str, column: str, line=None):
    # display a plot of the velocity of the right and left hand on one graph
    data = get_velocity(session_id)
    fig = px.line(data, x="time", y=column)
    fig.update_layout(paper_bgcolor="#13161C", plot_bgcolor="#252A33")
    if line is not None:
        # add a red line at the max velocity
        fig.add_trace(
            go.Scatter(
                x=[0, data["time"].max()],
                y=[line, line],
                mode='lines',
                line=dict(color='red', width=4),
                name="max velocity"
            )
        )
    return fig


        