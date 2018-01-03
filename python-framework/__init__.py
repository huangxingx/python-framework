#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @author: x.huang
# @date:17-8-1


import os
import sys

file_path = os.path.realpath(__file__)
project_dir = os.path.dirname(file_path)
os.chdir(project_dir)
sys.path.append(project_dir)
print('python-framework.__init__')
