def seconds_to_time(seconds: int) -> str:
    """
    Converts seconds to a string
    """
    minutes = seconds // 60
    seconds = seconds % 60
    return "{} min".format(minutes) if minutes else "{} sec".format(seconds)