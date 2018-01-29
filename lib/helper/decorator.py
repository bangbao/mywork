# encoding=utf8

import functools
from .rediser import RedisConsts, RedisLock
from .base import get_func_fullname
from .http import JsonResponse400


class single_limit_request(object):
    """限制频繁重复提交请求
    Args:
        request_index: request参数位置
        timeout: 锁超时时间
        auto_release_lock: 执行完成后是否自动释放锁
    """
    TIMEOUT = 5

    def __init__(self, request_index=0, timeout=TIMEOUT, auto_release_lock=True):
        self.request_index = request_index
        self.timeout = timeout
        self.auto_release_lock = auto_release_lock

    def __call__(self, func):
        @functools.wraps(func)
        def wraper(*args, **kwargs):
            request = args[self.request_index]
            user_id = request.user.id
            funcname = get_func_fullname(func)
            cache_key = RedisConsts.SINGLE_LIMIT_REQUEST.format(funcname, user_id)
            if RedisLock.require_lock(cache_key, self.timeout):
                try:
                    return func(*args, **kwargs)
                finally:
                    if self.auto_release_lock:
                        RedisLock.release_lock(cache_key)
            else:
                return JsonResponse400(u'正在处理中, 请不要频繁操作.')
        return wraper


class single_limit_cronjob(object):
    """限制重复执行定时任务
    Args:
        cronjob_index: cronjob参数位置
        timeout: 锁超时时间
        auto_release_lock: 执行完成后是否自动释放锁
    """
    TIMEOUT = 3600

    def __init__(self, cronjob_index=0, timeout=TIMEOUT, auto_release_lock=True):
        self.cronjob_index = cronjob_index
        self.timeout = timeout
        self.auto_release_lock = auto_release_lock

    def __call__(self, func):
        @functools.wraps(func)
        def wraper(*args, **kwargs):
            cronjob = args[self.cronjob_index]
            cronjob_id = cronjob.id
            cache_key = RedisConsts.CRONJOB_DO_JOB_LOCK.format(cronjob_id)
            if RedisLock.require_lock(cache_key, self.timeout):
                try:
                    return func(*args, **kwargs)
                finally:
                    if self.auto_release_lock:
                        RedisLock.release_lock(cache_key)
            else:
                return False
        return wraper
