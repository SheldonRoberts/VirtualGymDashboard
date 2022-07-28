import streamlit as st
import pandas as pd
import numpy as np

db_connection = 'crate://129.128.184.214:4200/'

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

def length_of_session(username:str, session_id:str) -> float:
    """
    Returns the length of a session in seconds
    """
    query = """
        SELECT MAX(TIME) - MIN(TIME) AS "Length"
        FROM frames
        WHERE "SessionId" = '{}';
    """.format(session_id)
    return pd.read_sql(query, con=db_connection)['Length'][0]

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

def get_session(session_id: str) -> pd.DataFrame:
    """
    Returns a dataframe of a session
    """
    query = """
        SELECT *
        FROM sessions
        WHERE "SessionId" = '{}'
        LIMIT 1;
    """.format(session_id)
    df = pd.read_sql(query, con=db_connection)
    df['Date'] = pd.to_datetime(df['Date'].map(lambda x: x.replace('.', ':')))
    return df

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

def get_relative_hand_pos(session_id: str) -> pd.DataFrame:
    """
    Returns a tuple of dataframes of relative hand positions for a session
    returns (left, right)
    """
    sql_query_left = f"""
        SELECT "LeftControllerAnchor_relx" AS "x", "LeftControllerAnchor_rely" AS "y", "LeftControllerAnchor_relz" AS "z"
        FROM frames
        WHERE "SessionId" LIKE '{session_id}'
        ORDER BY "time"
        LIMIT 10000;
        """

    sql_query_right = f"""
        SELECT "RightControllerAnchor_relx" AS "x", "RightControllerAnchor_rely" AS "y", "RightControllerAnchor_relz" AS "z"
        FROM frames
        WHERE "SessionId" LIKE '{session_id}'
        ORDER BY "time"
        LIMIT 10000;
        """

    data_left = pd.read_sql(sql_query_left, db_connection)
    data_right = pd.read_sql(sql_query_right, db_connection)
    return data_left, data_right

def get_max_reach(session_id: str) -> dict:
    """
    Returns a dictionary of max reach for a session
    """
    data_left, data_right = get_relative_hand_pos(session_id)
    left_xyz = data_left[['x', 'z', 'y']].to_numpy().transpose()
    right_xyz = data_right[['x', 'z', 'y']].to_numpy().transpose()

    left_max_y = left_xyz[1].max()
    left_max_z = left_xyz[2].max()
    left_min_x = left_xyz[0].min()
    left_min_z = left_xyz[2].min()
    right_max_x = right_xyz[0].max()
    right_max_y = right_xyz[1].max()
    right_max_z = right_xyz[2].max()
    right_min_z = right_xyz[2].min()

    z_offset = 1.65
    return {
        "left": abs(left_min_x),
        "right": abs(right_max_x),
        "forward": abs(max(left_max_y, right_max_y)),
        "upward": abs(max(left_max_z+z_offset, right_max_z+z_offset)),
        "downward": abs(min(left_min_z+z_offset, right_min_z+z_offset))
    }

def get_velocity(session_id: str) -> pd.DataFrame:
    """
    Returns a dataframe of velocity for a session
    """
    query = """
        SELECT "time", "LeftControllerAnchor_velx" AS "LeftX", "LeftControllerAnchor_vely" AS "LeftY", "LeftControllerAnchor_velz" AS "LeftZ", "RightControllerAnchor_velx" AS "RightX", "RightControllerAnchor_vely" AS "RightY", "RightControllerAnchor_velz" AS "RightZ", "LeftControllerAnchor_vel" as "Left", "RightControllerAnchor_vel" as "Right"
        FROM frames
        WHERE "SessionId" = '{}'
        ORDER BY "time"
        LIMIT 10000;
    """.format(session_id)
    return pd.read_sql(query, db_connection)