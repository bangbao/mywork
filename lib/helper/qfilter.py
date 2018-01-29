# coding: utf-8

from django.db.models import Q


def get_separate_qfilter(field_key, value, separate=','):
    """获取指定分隔符拼装值的过滤器
    Args:
        field_key: 字段名
        value: 要查找的值
        separate: 数据库存储使用的分隔符
    Returns:
        Q: 过滤器
    """
    value = str(value)
    startswith_key = '%s__startswith' % field_key
    startswith_val = '%s%s' % (value, separate)
    endswith_key = '%s__endswith' % field_key
    endswith_val = '%s%s' % (separate, value)
    contains_key = '%s__contains' % field_key
    contains_val = '%s%s%s' % (separate, value, separate)

    qfilter = Q(**{field_key: value})
    qfilter |= Q(**{startswith_key: startswith_val})
    qfilter |= Q(**{endswith_key: endswith_val})
    qfilter |= Q(**{contains_key: contains_val})
    return qfilter


def get_keyword_qfilter(field_keys, keyword, separate=' '):
    """关键词过滤器
    Args:
        field_keys: 字段名列表
        keyword: 关键词串
        separate: 关键词串使用的分隔符
    Returns:
        Q: 过滤器
    """
    keywords = keyword.split(separate)
    qfilter = Q()
    for word in keywords:
        for key in field_keys:
            fkey = '%s__contains' % key
            qfilter |= Q(**{fkey: word})
    return qfilter


def get_or_qfilter(qfilter=None, **kwargs):
    """合并或过滤器
    """
    qfilter = qfilter or Q()
    for fkey, fval in kwargs.iteritems():
        qfilter |= Q(**{fkey: fval})
    return qfilter


def get_and_qfilter(qfilter=None, **kwargs):
    """合并和过滤器
    """
    qfilter = qfilter or Q()
    for fkey, fval in kwargs.iteritems():
        qfilter &= Q(**{fkey: fval})
    return qfilter

