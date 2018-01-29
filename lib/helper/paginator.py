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
        'page_size': per_page,                 # 每页数量
    }


def get_paginator_serializer_data(request, queryset, serializer_class=None):
    """
    对数据进行分页
    :param request: Http Request
    :param queryset: QuerySet
    :param serializer_class: 序列化类
    :return:
    """
    page_size = request.query_params.get("page_size", 12)
    page = request.query_params.get("page", 1)
    pagination_data = get_paginator_pagination(queryset, page_size, page)
    page_data = get_paginator_page(queryset, page_size, page)
    if serializer_class:
        page_data = serializer_class(page_data, many=True).data
    return page_data, pagination_data
