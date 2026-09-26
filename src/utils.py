import time


def ms_to_time(ms):
    return time.strftime("%M:%S", time.gmtime(ms / 1000))


def current_milli_time():
    return round(time.time() * 1000)
