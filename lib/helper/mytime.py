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


def format_datetime(dt, fmt='%Y-%m-%d %H:%M:%S'):
    """格式化时间
    Args:
        dt: datetime.datetime对象
        hours: 加的小时数
    Returns:
        时间字符串
    """
    return dt.strftime(fmt)