from datetime import datetime
import pandas as pd

def seconds_to_time(seconds: int) -> str:
    """
    Converts seconds to a string
    """
    minutes = seconds // 60
    seconds = seconds % 60
    return "{} min".format(minutes) if minutes else "{} sec".format(seconds)

def time_ago(date: str) -> str:
    """
    Returns a string of how long ago a date was.
    Ex: 1 day ago
    Ex: 3 weeks ago
    """
    now = datetime.now()
    then = datetime.strptime(date, '%Y-%m-%d')
    delta = now - then
    if delta.days == 0:
        return "{} ago".format(delta.seconds // 3600)
    elif delta.days == 1:
        return "1 day ago"
    elif delta.days > 1:
        return "{} days ago".format(delta.days)

def max_reach(df_right, df_left: pd.DataFrame) -> dict:
    left_max_y = df_left[1].max()
    left_max_z = df_left[2].max()
    left_min_x = df_left[0].min()
    right_max_x = df_right[0].max()
    right_max_y = df_right[1].max()
    right_max_z = df_right[2].max()

    print("left: " + str(abs(left_min_x)))
    print("right: " + str(abs(right_max_x)))
    print("forward: " + str(abs(max(left_max_y, right_max_y))))
    print("upward: " + str(abs(max(left_max_z, right_max_z))))
    return {}