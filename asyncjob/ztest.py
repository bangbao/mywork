# coding: utf-8

import time
import datetime
from .api import enqueue, start_worker, test_job, push_to_asyncjob


def test():
    worker = start_worker()

    push_to_asyncjob(test_job, 12)
    #test_job(12)
    #test_job(20)

    while 1:
        #print worker.info()
        time.sleep(1)
        if not worker.is_alive():
            break


if __name__ == '__main__':
    test()