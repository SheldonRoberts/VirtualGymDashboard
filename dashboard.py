import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import plotly.express as px
import plotly.graph_objects as go
from helpers import *
from queries import *
from plots import *

st.set_page_config(layout="wide")
st.title('Virtual Gym Dashboard')

# make a dropdown menu to select a user
username = st.selectbox('User', get_users())

# display some metrics about the user
# create 4 columns
metric1, metric2, metric3, metric4 = st.columns(4)
metric1.metric('Platform', get_sessions(username)["Platform"][0])
metric2.metric('Sessions', len(get_sessions(username)))
metric3.metric('Time Played', seconds_to_time(time_played(username)))
metric4.metric('Last Played', time_ago(str(get_sessions(username).iloc[0]["Date"]).split(' ')[0]))

st.write(plot_calendar(username))

# make a dropdown menu to select a session
session_id = st.selectbox('Session', get_sessions(username)["SessionId"].tolist())

# display some metrics about the session
# create 3 columns
metric1, metric2, metric3 = st.columns(3)
metric1.metric('Date', str(get_sessions(username)["Date"][0]).split()[0])
metric2.metric('Length', seconds_to_time(length_of_session(username, session_id)))
metric3.metric('Game', get_sessions(username)["Game"][0])

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

if session_df is not None:
    with st.expander("See raw data"):
        st.write(session_df)
    # make a plot of the session data
    st.subheader('Range Of Motion Plot')
    st.plotly_chart(plot_hand_replay(session_id))

    reach = get_max_reach(session_id)
    st.subheader("Max reach (cm)")
    reach_left, reach_right, reach_up, reach_down, reach_forward = st.columns(5)
    reach_left.metric("Left from center", round(reach["left"]*100, 1))
    reach_right.metric("Right from center", round(reach["right"]*100, 1))
    reach_up.metric("Up (from ground)", round(reach["upward"]*100, 1))
    reach_down.metric("Down (above ground)", round(reach["downward"]*100, 1))
    reach_forward.metric("Forward from center", round(reach["forward"]*100, 1))
    st.write("*Note: These metrics are unreliable if the controllers were ever dropped. We need to remove outliers to improve this metric.")

    st.info("More metrics to be added here soon...")


