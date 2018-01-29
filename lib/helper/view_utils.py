# -*- coding: utf-8 -*-
import datetime
from django.shortcuts import get_object_or_404, get_list_or_404
from django.db.models.base import ModelBase
from django.db.models.manager import Manager
from django.db.models.query import QuerySet
from django.http import Http404

from utils.http import FilterException

"""自定义APIView的功能函数"""


def get_data_or_error(data, keyword, error_msg, to_type=None):
    """
    从data中获取键为keyword数据，不存在则返回错误信息
    :param data: 请求数据 dict
    :param keyword: 需获取数据键值 str
    :param error_msg: 错误提示信息 str
    :param to_type: 需要转换的类型
    :return:
    """
    if data.get(keyword, None):
        if to_type:
            return to_type(data.get(keyword))
        return data.get(keyword)
    else:
        raise FilterException(msg=error_msg)


DEFAULT = object()


def make_choice_to_meta(choices):
    """
    将choices中定义的数据转化为[{"code": 1, "name": "233"}, ]的形式
    :param choices:
    :return:
    """
    return [{"code": i[0], "name": i[1]} for i in choices]


def validate(data, key, default=DEFAULT, func=str, msg=''):
    """从data中获取键为key数据，并func处理
    """
    try:
        return func(data[key])
    except (KeyError, ValueError):
        if default is not DEFAULT:
            return default
        raise FilterException(msg=msg)


def get_object_or_error(klass, filter_kwargs, error_msg=None):
    """
    根据传入的QuerySet, Manager, Model 和过滤参数查询该对象
    如果获取失败，当error_msg为None，则返回False
                当传入了error_msg，则返回自定义错误信息
    :param klass: QuerySet, Manager, Model
    :param error_msg:  自定义错误信息
    :param filter_kwargs: 查询条件
    :return:
    """
    try:
        return get_object_or_404(klass, **filter_kwargs)
    except Http404:
        if error_msg is not None:
            raise FilterException(msg=error_msg)
        return False
    except Exception as e:
        if isinstance(klass, QuerySet):
            return klass.filter(**filter_kwargs).first()
        elif isinstance(klass, Manager):
            return klass.all().filter(**filter_kwargs).first()
        elif isinstance(klass, ModelBase):
            return klass._default_manager.all().filter(**filter_kwargs).first()
        else:
            return e


def get_queryset_or_error(queryset, filter_kwargs, error_msg):
    """
    根据传入的QuerySet和过滤参数查询该对象查询集，如果获取失败，则返回自定义错误信息
    :param queryset:
    :param filter_kwargs:
    :param error_msg:
    :return:
    """
    try:
        return get_list_or_404(queryset, **filter_kwargs)
    except Http404:
        raise FilterException(msg=error_msg)


def get_filter_kwargs(request, filter_keywords):
    """
    获取过滤参数
    :param request:
    :param filter_keywords:
    :return:
    """
    req_data = request.query_params
    filter_kwargs = dict()
    for keyword in filter_keywords:
        if req_data.get(keyword, None):
            filter_kwargs[keyword] = req_data.get(keyword)
    return filter_kwargs


def get_filter_queryset(queryset, filter_kwargs, order_kwargs):
    """
    对查询集进行过滤
    :param queryset: QuerySet
    :param filter_kwargs: 过滤字段
    :param order_kwargs: 排序字段
    :return:
    """
    return queryset.filter(**filter_kwargs).order_by(order_kwargs)


def get_serializer_class(self, method=None):
    """
    获取序列化类
    :param self: ViewSet
    :param method: HTTP Method
    :return:
    """
    if method:
        return self.serializer_class_dict[method]
    else:
        if self.serializer_class:
            return self.serializer_class
        else:
            return self.serializer_class_list[0]


def get_serializer_data(queryset, serializer, many=False):
    """
    对查询集进行序列化
    :param queryset:
    :param serializer:
    :param many:
    :return:
    """
    if many:
        return serializer(queryset, many=True).data
    else:
        return serializer(queryset).data


def get_url_pk(**kwargs):
    """获取url中的指定资源id"""
    return int(get_data_or_error(kwargs, "pk", error_msg=u"url存在异常"))


def get_value_from_choices(choices, key):
    """将Choices中的数值转化为对应字符串"""
    for choice in choices:
        if choice[0] == key:
            return choice[1]


def create_date(date_str, date_class="datetime"):
    """将可以表示时间的数据转换为datetime对象"""
    if date_class == "date":
        date_obj = datetime.datetime
    else:
        date_obj = datetime.datetime
    if "-" in date_str:
        return date_obj.strptime(date_str, "%Y-%m-%d")
    elif "." in date_str:
        return date_obj.strptime(date_str, "%Y.%m.%d")

