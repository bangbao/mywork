# coding: utf-8

import time
from .worker import ThreadWorker, ProcessWorker

worker = None

def get_worker(woker_class=ThreadWorker):
    global worker
    if worker is None:
        worker = woker_class()
        worker.start()
    return worker


def enqueue(f, *args, **kwargs):
    worker = get_worker()
    worker.enqueue(f, *args, **kwargs)


def test():
    worker = get_worker()

    while 1:
        print worker.info()
        time.sleep(1)
        if not worker.is_alive():
            break


if __name__ == '__main__':
    test()