# coding: utf-8

import time
import datetime
from .api import enqueue, start_worker, test_job


def test():
    worker = start_worker()
    enqueue(test_job, b=str(datetime.datetime.now()))
    time.sleep(1)
    enqueue(test_job, b=str(datetime.datetime.now()))
    time.sleep(1)

    while 1:
        #print worker.info()
        time.sleep(1)
        if not worker.is_alive():
            break


if __name__ == '__main__':
    test()