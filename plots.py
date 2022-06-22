import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import plotly.express as px
import plotly.graph_objects as go

@st.cache
def plot_scatter(df: pd.DataFrame, labels: list[str]) -> px.scatter_3d:
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