#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @author: x.huang
# @date:17-8-1

import logging.config
import os

cur_dir = os.path.dirname(__file__)
project_dir = os.path.realpath(os.path.dirname(cur_dir))
os.chdir(project_dir)

log_ini_path = os.path.join(cur_dir, './logger.ini')

logging.config.fileConfig(log_ini_path)

# logger
root_logger = logging.getLogger('root')
web_logger = logging.getLogger('web')
api_logger = logging.getLogger('api')
admin_logger = logging.getLogger('admin')

if __name__ == '__main__':
    root_logger.warning('this is root debug')
    web_logger.warning('this is web debug')
    api_logger.warning('this is api debug')
    admin_logger.warning('this is admin debug')
