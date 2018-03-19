# coding: utf-8

import redis
from django.core.cache import cache


def get_redis_client():
    try:
        return cache.get_master_client()
    except:
        return redis.StrictRedis()


class RedisQueue(object):
    def __init__(self, redis_key):
        self.redis_key = redis_key
        self.redis_client = get_redis_client()

    def push(self, one):
        self.redis_client.lpush(self.redis_key, one)

    def pop(self):
        result = self.redis_client.blpop(self.redis_key, timeout=1)
        if result:
            return result[1]
        return ''

    def count(self):
        return self.redis_client.llen(self.redis_key)