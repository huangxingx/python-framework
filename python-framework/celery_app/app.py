#! /usr/bin/env python
# -*- coding: utf-8 -*-
# @author: x.huang
# @date:18-1-3


import logging

from celery import Celery

import setting

celery_obj = Celery('app', broker=setting.BROKER_URL, backend=setting.CELERY_RESULT_BACKEND)


@celery_obj.task
def upload_from_file(bucket_obj, obj_name, src_name):
    """
    上传本地文件到
    :param bucket_obj: oss bucket对象
    :param src_name: 本地文件名
    :param obj_name: oss文件对象名
    :return:
    """

    oss_result = bucket_obj.put_object_from_file(obj_name, src_name)
    try:
        resp = {'status': oss_result.resp.status, 'url': oss_result.resp.response.url}
        return resp
    except Exception as e:
        logging.error(str(e))
        return {'status': 500, 'url': ''}
