# encoding=utf8

import time
import json
import inspect
import functools
from django.core.cache import cache
from django.http import HttpResponse
from .rediser import RedisConsts


TIMEOUT = 5


class single_limit_request(object):
    """限制频繁重复提交请求
    Args:
        request_index: request参数位置
        timeout: 锁超时时间
        auto_release_lock: 执行完成后是否自动释放锁
    """
    def __init__(self, request_index=0, timeout=TIMEOUT, auto_release_lock=True):
        self.redis_client = cache.get_master_client()
        self.request_index = request_index
        self.timeout = timeout
        self.auto_release_lock = auto_release_lock

    def require_lock(self, cache_key):
        """申请加锁
        """
        now = time.time()
        # 使用redis版本为2.2.12, set方法不支持额外参数, 故使用setnx实现锁
        # redis_client.set(cache_key, 1, nx=True, ex=TIMEOUT)
        if self.redis_client.setnx(cache_key, now):
            self.redis_client.expire(cache_key, self.timeout)
            return True
        # 出现异常, 判断时间超时, 重新加锁
        oldtime = self.redis_client.get(cache_key) or 0
        if now - float(oldtime) > self.timeout:
            self.redis_client.delete(cache_key)
        if self.redis_client.setnx(cache_key, now):
            self.redis_client.expire(cache_key, self.timeout)
            return True
        return False

    def release_lock(self, cache_key):
        """申请解锁
        """
        return self.redis_client.delete(cache_key)

    def __call__(self, func):
        @functools.wraps(func)
        def wraper(*args, **kwargs):
            request = args[self.request_index]
            user_id = request.user.id
            funcname = get_func_fullname(func)
            cache_key = RedisConsts.SINGLE_LIMIT_REQUEST.format(funcname, user_id)
            if self.require_lock(cache_key):
                try:
                    return func(*args, **kwargs)
                finally:
                    if self.auto_release_lock:
                        self.release_lock(cache_key)
            else:
                return JsonResponse400(u'正在处理中, 请不要频繁操作.')
        return wraper


def JsonResponse400(msg):
    resp = {'status': False,
            'msg': msg,
            'errors': {'detail': msg}}
    return json_response(resp, 400)


def json_response(data, status=200):
    """ Return json response
    """
    response = HttpResponse(json.dumps(data, ensure_ascii=False),
                            content_type='application/json; charset=utf-8',
                            status=status)
    return response


def get_func_fullname(func):
    """获取函数全名
    """
    if inspect.isfunction(func):
        fullname = '%s.%s' % (func.__module__, func.__name__)
    elif inspect.ismethod(func):
        im_class = func.im_class
        fullname = '%s.%s.%s' % (im_class.__module__, im_class.__name, func.__name__)
    else:
        fullname = func.__name__
    return fullname


