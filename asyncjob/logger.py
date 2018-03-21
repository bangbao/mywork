# coding: utf-8

import logging


logger = logging.getLogger('asyncjob')


def print_log(s):
    print s
    logger.info(s)


def info_log(s):
    logger.info(s)


def err_log(s):
    logger.error(s)