import datetime

""" Utility functions to convert and manipulate datetime.time objects"""


def convert_to_seconds(time_obj) -> int:
    """Converts a datetime.time object into seconds and returns and Int type"""
    seconds = (
        (time_obj.hour * 3600)
        + (time_obj.minute * 60)
        + (time_obj.second)
    )
    return seconds


def convert_to_time_object(seconds):
    """Converts string of numbers representing seconds to datetime.time object"""
    min, sec = divmod(seconds, 60)
    hour, min = divmod(min, 60)
    return datetime.time(hour, min, sec)
