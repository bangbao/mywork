# coding: utf-8

import time
from django.core.cache import cache
from .base import try_except_return_default


class RedisConsts(object):
    """redis key格式定义
    """
    CHECK_PHONE_CODE_COUNT = 'check_phone_code:count:{}'          # 手机号发送验证码次数
    CHECK_PHONE_CODE_TOKEN = 'check_phone_code:token:{}'          # 手机号发送验证码token
    CHECK_PHONE_CODE_CAPTCHA = 'check_phone_code:captcha:{}'      # 手机号对应的验证码
    LIMIT_REQUEST_IP_COUNT = 'limit_request_ip:count:{}'          # 限制IP请求次数
    SINGLE_LIMIT_REQUEST = 'single_limit_request:{}:{}'           # 限制重复请求
    CRONJOB_DO_JOB_LOCK = 'cronjob_do_job_lock:{}'                # 定时任务执行加锁, 避免重复执行


class RedisLock(object):
    """redis分布式锁
    """
    @staticmethod
    @try_except_return_default(False)
    def require_lock(cache_key, timeout):
        """申请加锁
        """
        redis_client = cache.get_master_client()
        now = time.time()
        # 使用redis版本为2.2.12, set方法不支持额外参数, 故使用setnx实现锁
        # redis_client.set(cache_key, 1, nx=True, ex=TIMEOUT)
        if redis_client.setnx(cache_key, now):
            redis_client.expire(cache_key, timeout)
            return True
        # 出现异常, 判断时间超时, 重新加锁
        oldtime = redis_client.get(cache_key) or 0
        if now - float(oldtime) > timeout:
            redis_client.delete(cache_key)
        if redis_client.setnx(cache_key, now):
            redis_client.expire(cache_key, timeout)
            return True
        return False

    @staticmethod
    def release_lock(cache_key):
        """申请解锁
        """
        redis_client = cache.get_master_client()
        return redis_client.delete(cache_key)
