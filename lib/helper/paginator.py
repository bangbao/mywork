# coding: utf-8

from django.core.paginator import Paginator


def get_paginator_page(query_list, per_page=20, page=1, raise_error=False):
    """获取指定分页数据query
    """
    paginator = Paginator(query_list, per_page)
    try:
        return paginator.page(page)
    except Exception as e:
        if raise_error:
            raise e
    return []


def get_paginator_pagination(query_list, per_page=20, page=1):
    """返回分页共用数据
    """
    paginator = Paginator(query_list, per_page)
    return {
        'count': paginator.count,              # 总数量
        'page': page,                          # 当前页码
        'pages': paginator.num_pages,          # 总页码
    }
