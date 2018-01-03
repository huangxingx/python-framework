#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
@file: celery_worker.py
@author: tangcc
@time: 2017-10-27 13:55:45
"""

from celery import platforms
from celery.bin import worker

from celery_app import app

platforms.C_FORCE_ROOT = True


def worker_start():
    worker_obj = worker.worker(app=app.celery_obj)
    worker_obj.run(concurrency=4, traceback=False, loglevel='INFO')


if __name__ == "__main__":
    worker_start()
