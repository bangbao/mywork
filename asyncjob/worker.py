# coding: utf-8

import os
import time
import datetime
import signal
import traceback
import threading
import multiprocessing
from .logger import print_log


REDIS_KEY_WORKER = 'asyncjob:worker:{}'


class Worker(object):
    def __init__(self, connection, queue):
        self.connection = connection
        self.queue = queue

        self.name = '%s:%s' % (self.__class__.__name__, os.getpid())
        self.key = REDIS_KEY_WORKER.format(self.name)

        self._request_stop = False
        self._current_job = None

        self.set_signal_handle()

    def do_job(self, job):
        self._current_job = job
        self.log('job(%s) started' % job)
        try:
            return job.execute()
        finally:
            self._current_job = None
            self.log('job(%s) finished' % job)

    def request_stop(self, sig, frame):
        if not self._request_stop:
            self._request_stop = True
            self.queue.push(None)

    def set_signal_handle(self):
        signal.signal(signal.SIGINT, self.request_stop)
        signal.signal(signal.SIGTERM, self.request_stop)

    def info(self):
        return {
            'count': self.queue.count(),
            'current_job': self._current_job,
            'time': time.strftime('%Y-%m-%d %H:%M:%S'),
        }

    def log(self, s):
        print_log(s)

    def heartbeat(self):
        info = self.info()
        pipeline = self.connection.pipeline()
        pipeline.hmset(self.key, info)
        pipeline.expire(self.key, 3600)
        pipeline.execute()
        print self.key, info
        # self.log('%s: hello, I am alive' % self.name)

    def run(self):
        self.log('%s: ready to work' % self.name)
        while 1:
            if self._request_stop:
                self.log('%s: got _request_stop' % self.name)
                break
            self.heartbeat()
            try:
                job = self.queue.pop_job()
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


class ThreadWorker(Worker, threading.Thread):
    def __init__(self, connection, queue):
        threading.Thread.__init__(self)
        Worker.__init__(self, connection, queue)


class ProcessWorker(Worker, multiprocessing.Process):
    def __init__(self, connection, queue):
        multiprocessing.Process.__init__(self)
        Worker.__init__(self, connection, queue)

