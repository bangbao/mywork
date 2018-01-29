# coding: utf-8

import threading
from django.core.cache import cache


def get_redis_client():
    return cache.get_master_client()


class RedisQueue(object):
    def __init__(self):
        pass

    def push(self, one):
        pass

    def pop(self, ):
        pass


class Job(object):
    """任务类
    """

class Worker(object):
    def push_job(self, job):
        self.dataQueue.push(job)

    def pop_job(self):
        return self.dataQueue.pop()

    def do_job(self, job):
        return job.execute()


class ThreadWorker(Worker, threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.dataQueue = RedisQueue()
        self.name = self.__class__.__name__


    def run(self):
        print '%s : ready to work' % self.name
        while 1:
            try:
                job = self.pop_job()
            except:
                continue
            if job is None:
                print '%s: Got None, break thread' % self.name
                break

            self.do_job(job)
        print '%s: is stoped' % self.name

class ProcessWorker(Worker):
    pass