# coding: utf-8

import datetime
import time


def mktimestamp(timestr, fmt='%Y-%m-%d %H:%M:%S'):
    """转换时间字符串到时间戳
    Args:
        timestr: 时间字符串
        fmt: 对应的时间格式
    Returns:
        时间戳
    """
    dt = datetime.datetime.strptime(timestr, fmt)
    return dt2timestamp(dt)


def strftimestamp(timestamp, fmt='%Y-%m-%d %H:%M:%S'):
    """转换时间戳到字符串
    Args:
        timestamp: 时间戳
        fmt: 对应的时间格式
    Returns:
        时间字符串
    """
    dt = timestamp2dt(timestamp)
    return dt.strftime(fmt)


def dt2timestamp(dt):
    """转换日期时间对象到时间戳
    Args:
        dt: datetime.datetime()对象
    Returns:
        时间戳
    """
    struct_time = dt.timetuple()
    return int(time.mktime(struct_time))


def timestamp2dt(timestamp):
    """转换时间戳到日期时间对象
    Args:
        timestamp: 时间戳
    Returns:
        datetime.datetime()对象
    """
    return datetime.datetime.fromtimestamp(timestamp)


def strftime2dt(strftime, fmt='%Y-%m-%d %H:%M:%S'):
    """时间字符串转化为datetime.datetime对象
    Args:
        strftime: 时间字符串
    Returns:
        datetime.datetime()对象
    """
    return datetime.datetime.strptime(strftime, fmt)


def format_utc_datetime(dt, fmt='%Y-%m-%d %H:%M:%S', hours=8):
    """格式化utc时间, 默认加8
    Args:
        dt: datetime.datetime对象
        hours: 加的小时数
    Returns:
        时间字符串
    """
    dt = dt + datetime.timedelta(hours=hours)
    return dt.strftime(fmt)


def format_datetime(dt=None, fmt='%Y-%m-%d %H:%M:%S'):
    """格式化时间
    Args:
        dt: datetime.datetime对象
        fmt: 格式化串
    Returns:
        时间字符串
    """
    if dt is None:
        dt = datetime.datetime.now()
    return dt.strftime(fmt)


fmt_dt = format_datetime
fmt_utc_dt = format_utc_datetime


def guess_strftime2dt(strftime):
    """尝试把时间字符串转换成datetime.datetime对象
    """
    DATETIME_INPUT_FORMATS = [
        '%Y-%m-%d', '%m/%d/%Y', '%m/%d/%y',  # '2006-10-25', '10/25/2006', '10/25/06'
        '%b %d %Y', '%b %d, %Y',             # 'Oct 25 2006', 'Oct 25, 2006'
        '%d %b %Y', '%d %b, %Y',             # '25 Oct 2006', '25 Oct, 2006'
        '%B %d %Y', '%B %d, %Y',             # 'October 25 2006', 'October 25, 2006'
        '%d %B %Y', '%d %B, %Y',             # '25 October 2006', '25 October, 2006'
        '%Y-%m-%d %H:%M:%S',     # '2006-10-25 14:30:59'
        '%Y-%m-%d %H:%M:%S.%f',  # '2006-10-25 14:30:59.000200'
        '%Y-%m-%d %H:%M',        # '2006-10-25 14:30'
        '%Y-%m-%d',              # '2006-10-25'
        '%Y.%m.%d %H:%M:%S',
        '%Y.%m.%d %H:%M:%S.%f',
        '%Y.%m.%d %H:%M',
        '%Y.%m.%d',
        '%m/%d/%Y %H:%M:%S',     # '10/25/2006 14:30:59'
        '%m/%d/%Y %H:%M:%S.%f',  # '10/25/2006 14:30:59.000200'
        '%m/%d/%Y %H:%M',        # '10/25/2006 14:30'
        '%m/%d/%Y',              # '10/25/2006'
        '%m/%d/%y %H:%M:%S',     # '10/25/06 14:30:59'
        '%m/%d/%y %H:%M:%S.%f',  # '10/25/06 14:30:59.000200'
        '%m/%d/%y %H:%M',        # '10/25/06 14:30'
        '%m/%d/%y',              # '10/25/06'
    ]
    for fmt in DATETIME_INPUT_FORMATS:
        try:
            return datetime.datetime.strptime(strftime, fmt)
        except ValueError:
            continue
    raise ValueError('Guess strftime2dt fail: %s' % strftime)


def date_format(date_obj, format_str="-"):
    """将可以表示时间的数据转换为日期字符串"""
    if not(isinstance(date_obj, datetime.datetime)) and not isinstance(date_obj, datetime.date):
        date_obj = guess_strftime2dt(date_obj)
    if format_str == ".":
        return date_obj.strftime("%Y.%m.%d")
    elif format_str == "-":
        return date_obj.strftime("%Y-%m-%d")


def datetime_format(date_obj, format_str="-"):
    """将可以表示时间的数据转换为日期字符串"""
    if not(isinstance(date_obj, datetime.datetime)) and not isinstance(date_obj, datetime.date):
        date_obj = guess_strftime2dt(date_obj)
    if format_str == ".":
        return date_obj.strftime("%Y.%m.%d %H:%M:%S")
    elif format_str == "-":
        return date_obj.strftime("%Y-%m-%d %H:%M:%S")


def calc_month_delta(x, y):
    """计算两个日期之前的月数差
    Args:
        x: datetime.datetime对象
        y: datetime.datetime对象
    Returns:
        x, y相差的月份
    """
    return abs((x.year - y.year) * 12 + (x.month - y.month) * 1)
