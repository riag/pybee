
from datetime import datetime
from datetime import timedelta
import calendar


def now(ignore_microsecond=True):
    dt = datetime.now()
    if not ignore_microsecond:
        return dt
    return from_int(to_int(dt))


def today():
    t = now()
    return datetime.datetime(t.year, t.month, t.day)


def tomorrow():
    t = now()
    y = t + timedelta(days=1)
    return datetime(y.year, y.month, y.day)


def yesterday():
    t = now()
    y = t - timedelta(days=1)
    return datetime(y.year, y.month, y.day)


def to_str(date, fmt='%Y-%m-%d %H:%M:%S'):
    return date.strftime(fmt)


def from_str(s, fmt='%Y-%m-%d %H:%M:%S'):
    return datetime.strptime(s, fmt)


def to_int(date):
    return calendar.timegm(date.utctimetuple())


def from_int(timestamp):
    return datetime.utcfromtimestamp(timestamp)
