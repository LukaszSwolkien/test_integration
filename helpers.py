import datetime
import locale
import math


def is_int(s):
    try:
        if isinstance(s, str):
            num = to_num(s)
            if isinstance(num, float):
                return num.is_integer()
            return isinstance(num, int)
        elif isinstance(s, int):
            int(s)
            return True
        else:
            return False
    except ValueError:
        return False


def is_num(s):
    try:
        locale.atoi(str(s))
    except ValueError:
        try:
            num = locale.atof(str(s))
            return not math.isnan(num)
        except ValueError:
            return False
    return True


def to_num(s):
    strnum = str(s)
    strnum = strnum.split(" ")[0]
    x = strnum if is_num(strnum[0]) else strnum[1:]  # remove currency char if needed
    x = x.replace(",", "")
    try:
        return locale.atoi(x)
    except ValueError:
        return locale.atof(x)


def to_str(value):
    try:
        strval = u"".join(value)
    except TypeError:
        strval = str(value, errors="ignore")
    return strval


def to_timestamp(dt, epoch=datetime.datetime(1970, 1, 1)):
    td = dt - epoch
    # return td.total_seconds() - there is a bug with precision in python 2.7
    return (td.microseconds + (td.seconds + td.days * 86400) * 10 ** 6) / 10 ** 6


def create_utc_timestamp():
    """timestamp in seconds"""
    dt = datetime.datetime.utcnow()
    return to_timestamp(dt)
