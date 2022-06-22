import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import plotly.express as px
import plotly.graph_objects as go
from helpers import seconds_to_time
from queries import *
from plots import *

st.set_page_config(layout="wide")
st.title('Virtual Gym Dashboard')
st.markdown('Select a user to see their progress')




# make a dropdown menu to select a user
username = st.selectbox('User', get_users())

# display some metrics about the user
# create 4 columns
metric1, metric2, metric3, metric4 = st.columns(4)

metric1.metric('Platform', get_sessions(username)["Platform"][0])
metric2.metric('Sessions', len(get_sessions(username)))
metric3.metric('Time Played', seconds_to_time(time_played(username)))

# make a dropdown menu to select a session
session_id = st.selectbox('Session', get_sessions(username)["SessionId"].tolist())

# make a button to load the session data
session_df = None
col1, col2 = st.columns([1, 3])

with col1:
    loading_button = st.button('Load Session Data')
with col2:
    loading_text = st.empty()

if loading_button:
    loading_text.text('Loading session data...')
    session_df = get_session_data(session_id)
    loading_text.text('Session data loaded!')


with st.expander("See data"):
    st.write(session_df)

if session_df is not None:
    # make a plot of the session data
    df_right_xyz = session_df[
        ['CenterEyeAnchor_posx', 'CenterEyeAnchor_posz', 'CenterEyeAnchor_posy']
    ]
    st.plotly_chart(plot_scatter(df_right_xyz, ['CenterEyeAnchor_posx', 'CenterEyeAnchor_posz', 'CenterEyeAnchor_posy']))





