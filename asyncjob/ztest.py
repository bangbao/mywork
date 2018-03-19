# coding: utf-8

import time
from .worker import ThreadWorker, ProcessWorker


def test():
    worker = ThreadWorker()
    # worker = ProcessWorker()
    worker.start()

    while 1:
        print worker.info()
        time.sleep(1)
        if not worker.is_alive():
            break


if __name__ == '__main__':
    test()