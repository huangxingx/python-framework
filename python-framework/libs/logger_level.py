#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @author: x.huang
# @date:17-8-2
import logging

import os

PRJ_DIR = os.path.dirname(os.path.dirname(__file__))
os.chdir(PRJ_DIR)


class Logger(object):
    def __init__(self, app, level):
        self.app = app
        self.level = level
        self.LEVEL = getattr(logging, level.upper())

        self._logger = dict()
        levels = ['info', 'warning', 'error', 'critical', 'debug']
        log_path_format = './logs/{}.{}.log'
        stream_handler = logging.StreamHandler()
        formatter = self.get_log_format()
        stream_handler.setFormatter(formatter)

        for level_it in levels:
            logger = logging.getLogger(level_it)
            file_handler = logging.FileHandler(log_path_format.format(self.app, level_it))
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)
            logger.addHandler(stream_handler)
            logger.setLevel(self.LEVEL)
            self._logger[level_it] = logger

    @staticmethod
    def get_log_format():
        fmt = '%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s'
        datefmt = '%Y-%m-%d %H:%M:%S'
        return logging.Formatter(fmt=fmt, datefmt=datefmt)

    def debug(self, msg):
        self._logger['debug'].debug(msg)

    def info(self, msg):
        self._logger['info'].info(msg)

    def warning(self, msg):
        self._logger['warning'].warning(msg)

    def error(self, msg):
        self._logger['error'].error(msg)

    def critical(self, msg):
        self._logger['critical'].critical(msg)


if __name__ == '__main__':
    logger = Logger('web', 'error')
    logger.info('this is web info')
    # logger.error('this is web error')
    logger.critical('this is web critical')
