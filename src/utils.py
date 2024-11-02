import time
from enum import Enum


class Format(Enum):
    LOCAL: int = 0
    SERVER: int = 1


def ms_to_time(ms):
    return time.strftime("%M:%S", time.gmtime(ms / 1000))


def current_milli_time():
    return round(time.time() * 1000)
