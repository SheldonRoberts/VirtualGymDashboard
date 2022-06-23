import streamlit as st
import pandas as pd
import numpy as np

db_connection = 'crate://142.244.110.140:8004'

@st.cache
def time_played(username:str) -> float:
    """
    Returns the time played by a user
    """
    query = """
        SELECT SUM("Length") AS "Time"
        FROM (
            SELECT MAX(TIME) - MIN(TIME) AS "Length"
            FROM frames
            WHERE "SessionId" IN (
                SELECT DISTINCT "SessionId"
                FROM sessions
                WHERE "UserName" = '{}'
        )
        GROUP BY "SessionId" limit 100
        ) AS T;
    """.format(username)
    return pd.read_sql(query, db_connection)['Time'][0]

def days_user_played(username:str) -> pd.DataFrame:
    """
    Returns a list of the days a user played
    """
    query = """
        SELECT "Date", COUNT("Date") AS "sessions"
        FROM sessions
        WHERE "UserName" = '{}'
        GROUP BY "Date"
    """.format(username)
    df = pd.read_sql(query, db_connection)
    df['Date'] = pd.to_datetime(df['Date'].map(lambda x: x.split('T')[0]))
    return df


@st.cache
def get_users() -> list:
    """
    Returns a list of users from the database
    """
    query = """
        SELECT DISTINCT "UserName"
        FROM sessions limit 100;
    """
    return pd.read_sql(query, con=db_connection)['UserName'].tolist()

def get_sessions(user: str) -> list:
    """
    Returns a dataframe of sessions for a user
    """
    query = """
        SELECT *
        FROM sessions
        WHERE "UserName" = '{}';
    """.format(user)
    df = pd.read_sql(query, con=db_connection)
    df['Date'] = pd.to_datetime(df['Date'].map(lambda x: x.replace('.', ':')))
    df = df.sort_values('Date', ascending=False)
    return df

@st.cache
def get_session_data(session_id: str) -> pd.DataFrame:
    """
    Returns a dataframe of session data for a session
    """
    query = """
        SELECT *
        FROM frames
        WHERE "SessionId" = '{}';
    """.format(session_id)
    print(query)
    return pd.read_sql(query, con=db_connection)
