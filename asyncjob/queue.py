# coding: utf-8

import redis
from django.core.cache import cache

REDIS_KEY_QUEUE = 'asyncjob:queue'
_local_redis_client = None


def get_redis_client():
    try:
        return cache.get_master_client()
    except:
        global _local_redis_client
        if _local_redis_client is None:
            _local_redis_client = redis.StrictRedis()
        return _local_redis_client


class RedisQueue(object):
    def __init__(self, connection, redis_key=None, job_class=None):
        self.redis_key = redis_key or REDIS_KEY_QUEUE
        self.connection = connection
        self.job_class = job_class

    def push(self, one):
        self.connection.rpush(self.redis_key, one)

    def pop(self):
        result = self.connection.blpop(self.redis_key, timeout=1)
        if result:
            return result[1]
        return ''

    def count(self):
        return self.connection.llen(self.redis_key)

    def push_job(self, job):
        data = job.dumps()
        self.push(data)
        return job

    def pop_job(self):
        data = self.pop()
        if data and data != 'None':
            return self.job_class.loads(data)
        if data == 'None':
            return None
        return data
