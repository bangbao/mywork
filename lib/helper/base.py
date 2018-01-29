# coding: utf-8

import inspect
import functools
import traceback



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



class try_except_return_default(object):
    """函数执行出现异常时返回默认值
    Attributes:
        default: request参数位置
        error: 扑捉的异常类, 不传扑捉所有异常
    """
    def __init__(self, default, error=None, print_exc=True):
        self.default = default
        self.error = error or Exception
        self.print_exc = print_exc

    def __call__(self, func):
        @functools.wraps(func)
        def wraper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except self.error:
                return self.default
            finally:
                if self.print_exc:
                    traceback.print_exc()
        return wraper
