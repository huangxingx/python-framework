#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @author: x.huang
# @date:17-8-1

import os
import sys

from libs.loger import root_logger as logger

# 初始化环境
file_path = os.path.realpath(__file__)
project_dir = os.path.dirname(file_path)
os.chdir(project_dir)
sys.path.append(project_dir)

# start code
logger.warning('waring')
