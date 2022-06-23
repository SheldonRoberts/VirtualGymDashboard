from datetime import datetime

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
    