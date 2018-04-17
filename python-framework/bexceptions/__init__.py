#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @author: x.huang
# @date:17/04/18


class BException(BaseException):
    """ 业务异常基类 """

    def __init__(self, error_code=0, error_msg=''):
        self.error_code = error_code
        self.error_msg = error_msg
