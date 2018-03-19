# coding: utf-8

import signal
import traceback
import threading
import multiprocessing
from .job import Job, JobStatus
from .queue import RedisQueue
from .logger import logger

REDIS_KEY_QUEUE = 'asyncjob:queue'


class Worker(object):
    def __init__(self):
        self.job_class = Job
        self._request_stop = False
        self._current_job = None
        self.set_signal_handle()

    def push_job(self, job):
        data = job.dumps()
        self.dataQueue.push(data)
        return job

    def pop_job(self):
        data = self.dataQueue.pop()
        print data
        if data and data != 'None':
            return self.job_class.loads(data)
        if data == 'None':
            return None
        return data

    def do_job(self, job):
        self._current_job = job
        return job.execute()

    def request_stop(self, sig, frame):
        self._request_stop = True
        self.dataQueue.push(None)

    def set_signal_handle(self):
        signal.signal(signal.SIGINT, self.request_stop)
        signal.signal(signal.SIGTERM, self.request_stop)

    def info(self):
        return {
            'count': self.dataQueue.count(),
            'current_job': self._current_job,
        }

    def log(self, s):
        print s
        logger.info(s)

    def enqueue(self, f, *args, **kwargs):
        """Creates a job to represent the delayed function call and enqueues
        it.
        """
        if not isinstance(f, basestring) and f.__module__ == '__main__':
            raise ValueError('Functions from the __main__ module cannot be processed '
                             'by workers')
        timeout = kwargs.pop('timeout', None)

        if 'args' in kwargs or 'kwargs' in kwargs:
            assert args == (), 'Extra positional arguments cannot be used when using explicit args and kwargs'  # noqa
            args = kwargs.pop('args', None)
            kwargs = kwargs.pop('kwargs', None)

        job = self.job_class.create(f, args=args, kwargs=kwargs,
                                    status=JobStatus.QUEUED, timeout=timeout)
        job = self.push_job(job)
        return job


class ThreadWorker(Worker, threading.Thread):
    def __init__(self):
        Worker.__init__(self)
        threading.Thread.__init__(self)
        self.dataQueue = RedisQueue(REDIS_KEY_QUEUE)
        self.name = self.__class__.__name__

    def run(self):
        self.log('%s: ready to work' % self.name)
        while 1:
            if self._request_stop:
                self.log('%s: got _request_stop' % self.name)
                break
            try:
                job = self.pop_job()
            except Exception:
                e = traceback.format_exc()
                self.log('%s: Got error, %s' % (self.name, e))
                continue
            if job is None:
                self.log('%s: Got None, break' % self.name)
                break
            if not job:
                continue

            self.do_job(job)
        self.log('%s: is stoped' % self.name)


class ProcessWorker(Worker, multiprocessing.Process):
    def __init__(self):
        Worker.__init__(self)
        multiprocessing.Process.__init__(self)
        self.dataQueue = RedisQueue(REDIS_KEY_QUEUE)
        self.name = self.__class__.__name__

    def run(self):
        self.log('%s: ready to work' % self.name)
        while 1:
            if self._request_stop:
                self.log('%s: got _request_stop' % self.name)
                break
            try:
                job = self.pop_job()
            except Exception:
                e = traceback.format_exc()
                self.log('%s: Got error, %s' % (self.name, e))
                continue
            if job is None:
                self.log('%s: Got None, break' % self.name)
                break
            if not job:
                continue

            self.do_job(job)
        self.log('%s: is stoped' % self.name)
