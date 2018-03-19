# coding: utf-8

import threading
import inspect
import traceback
import cPickle as pickle
from uuid import uuid4
from functools import partial


dumps = partial(pickle.dumps, protocol=pickle.HIGHEST_PROTOCOL)
loads = pickle.loads


class JobStatus(object):
    QUEUED = 'queued'
    FINISHED = 'finished'
    FAILED = 'failed'
    STARTED = 'started'
    DEFERRED = 'deferred'


class Job(object):
    """任务类
    """
    # Job construction
    @classmethod
    def create(cls, func, args=None, kwargs=None, status=None, timeout=None):
        """Creates a new Job instance for the given function, arguments, and
        keyword arguments.
        """
        if args is None:
            args = ()
        if kwargs is None:
            kwargs = {}

        if not isinstance(args, (tuple, list)):
            raise TypeError('{0!r} is not a valid args list'.format(args))
        if not isinstance(kwargs, dict):
            raise TypeError('{0!r} is not a valid kwargs dict'.format(kwargs))

        job = cls()
        job._id = str(uuid4())

        # Set the core job tuple properties
        job._instance = None
        if inspect.ismethod(func):
            job._instance = func.__self__
            job._func_name = func.__name__
        elif inspect.isfunction(func) or inspect.isbuiltin(func):
            job._func_name = '{0}.{1}'.format(func.__module__, func.__name__)
        elif isinstance(func, basestring):
            job._func_name = func
        elif not inspect.isclass(func) and hasattr(func, '__call__'):  # a callable class instance
            job._instance = func
            job._func_name = '__call__'
        else:
            raise TypeError('Expected a callable or a string, but got: {0}'.format(func))

        job._args = args
        job._kwargs = kwargs
        job._timeout = timeout
        job._status = status
        job._result = None

        return job

    def to_dict(self):
        return {
            'id': self._id,
            'func_name': self._func_name,
            'args': self._args,
            'kwargs': self._kwargs,
            'status': self._status,
            'timeout': self._timeout,
            'result': self._result,
        }

    def from_dict(self, data):
        self._id = data['id']
        self._func_name = data['func_name']
        self._args = data['args']
        self._kwargs = data['kwargs']
        self._status = data['status']
        self._timeout = data['timeout']
        self._result = data.get('result', None)

    @classmethod
    def loads(cls, data):
        data = loads(data)
        obj = cls()
        obj.from_dict(data)
        return obj

    def dumps(self):
        data = self.to_dict()
        return dumps(data)

    def get_func(self):
        """获取执行函数对象
        """
        try:
            modname, funcname = str(self.func_name).rsplit('.', 1)
            module = __import__(modname, globals(), locals(), [funcname])
            func = getattr(module, funcname)
            return func
        except (ImportError, AttributeError, ValueError):
            return None

    def execute(self):
        """执行任务
        """
        args, kwargs = self._args, self._kwargs
        func = self.get_func()
        if not func:
            return self.failure_callback('func not found')

        try:
            result = func(*args, **kwargs)
            return self.success_callback(result)
        except:
            errmsg = traceback.format_exc()
            return self.failure_callback(errmsg)

    def success_callback(self, result):
        """执行函数成功处理
        """
        self._result = dumps(result)
        return True

    def failure_callback(self, errmsg):
        """执行函数失败处理
        """
        self._status = 2
        self._result = errmsg
        return False

    def __str__(self):
        return self.to_dict()
