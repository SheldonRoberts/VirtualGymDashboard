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
    Ex: 30 minutes ago
    Ex: 5 hours ago
    Ex: 1 day ago
    Ex: 3 weeks ago
    """
    now = datetime.now()
    then = datetime.strptime(date, '%Y-%m-%d')
    delta = now - then
    if delta.days == 1:
        return "{} day ago".format(delta.days)
    elif delta.days > 1:
        return "{} days ago".format(delta.days)
    elif delta.seconds > 3600:
        return "{} hours ago".format(delta.seconds // 3600)
    elif delta.seconds > 60:
        return "{} minutes ago".format(delta.seconds // 60)
    else:
        return "{} seconds ago".format(delta.seconds)
    
def get_max_velocity(data: pd.DataFrame, column: str) -> float:
    """
    Returns the max velocity of a dataframe
    """
    # grab the average of the 20 largest values of "Left" in data
    return data[column].nlargest(20).mean()