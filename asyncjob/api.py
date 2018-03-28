# coding: utf-8

import time
import functools
from .worker import ThreadWorker, ProcessWorker
from .job import Job, JobStatus
from .queue import RedisQueue, get_redis_client


worker = None
queue = None
connection = None


def get_connection():
    global connection
    if connection is None:
        connection = get_redis_client()
    return connection


def get_worker(worker_class=ThreadWorker):
    global worker
    if worker is None:
        connection = get_connection()
        queue = get_queue()
        worker = worker_class(connection, queue)
    return worker


def get_queue(queue_class=RedisQueue):
    global queue
    if queue is None:
        connection = get_connection()
        queue = queue_class(connection, job_class=Job)
    return queue


def start_worker(num=1):
    assert num == 1
    worker = get_worker()
    if not worker.is_alive():
        worker.start()
    return worker


def enqueue(f, *args, **kwargs):
    """加入异步任务
    """
    if not isinstance(f, basestring) and f.__module__ == '__main__':
        raise ValueError('Functions from the __main__ module cannot be processed')
    timeout = kwargs.pop('timeout', None)

    job = Job.create(f, args=args, kwargs=kwargs, status=JobStatus.QUEUED, timeout=timeout)
    queue = get_queue()
    queue.push_job(job)
    return job


def push_to_asyncjob(f, *args, **kwargs):
    """加入异步任务
    """
    start_worker()
    enqueue(f, *args, **kwargs)


class asyncjob(object):
    """异步任务
    Args:
        use_async: 是否异步执行
    """
    def __init__(self, use_async=True):
        self.use_async = use_async
        if self.use_async:
            self.worker = start_worker()

    def __call__(self, func):
        @functools.wraps(func)
        def wraper(*args, **kwargs):
            if self.use_async:
                print locals()
                print dir(func)
                print dir(self)
                print 'using async: %s %s %s' % (func.__name__, args, kwargs)
                #return enqueue(func, *args, **kwargs)
            return func(*args, **kwargs)
        return wraper


#@asyncjob()
def test_job(b):
    count = b
    while count > 0:
        count -= 1
        time.sleep(1)
        print 'test_job: %s' % locals()

#
# @asyncjob()
# def test_job2(a):
#     num = a
#     while num > 0:
#         num -= 1
#         time.sleep(1)
#         print 'test_job2: %s' % locals()
