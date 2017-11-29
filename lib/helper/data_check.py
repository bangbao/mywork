# -*- coding: utf-8 -*-

from django.shortcuts import get_object_or_404, get_list_or_404
from django.db.models.base import ModelBase
from django.db.models.manager import Manager
from django.db.models.query import QuerySet
from django.http import Http404

from utils.http import FilterException


def get_data_or_error(data, keyword, error_msg):
    """
    从data中获取键为keyword数据，不存在则返回错误信息
    :param data: 请求数据 dict
    :param keyword: 需获取数据键值 str
    :param error_msg: 错误提示信息 str
    :return:
    """
    if data.get(keyword, None):
        return data.get(keyword)
    else:
        raise FilterException(msg=error_msg)

DEFAULT = object()
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


def get_queryset_or_error(queryset, error_msg, **kwargs):
    """
    根据传入的QuerySet和过滤参数查询该对象查询集，如果获取失败，则返回自定义错误信息
    :param queryset:
    :param error_msg:
    :param kwargs:
    :return:
    """
    try:
        return get_list_or_404(queryset, **kwargs)
    except Http404:
        raise FilterException(msg=error_msg)
