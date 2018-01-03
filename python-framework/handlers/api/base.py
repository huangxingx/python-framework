#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @author: x.huang
# @date:18-1-3

"""
BaseApiHandler： Api的基类
ApiHandler: Api 不带登录验证的基类
ApiAuthHandler: Api 带登录验证的基类

"""

from ..base.auth import AuthBaseHandler
from ..base.base import BaseRequestHandler


class BaseApiHandler(BaseRequestHandler):
    def __init__(self, *args, **kwargs):
        super(BaseApiHandler, self).__init__(*args, **kwargs)
        self.appuser = self.session.get('appuser')

    def get_current_user(self):
        if not self.appuser:
            return None
        phone = self.appuser.get('phone')
        if phone:
            return phone
        else:
            return None


class ApiHandler(BaseApiHandler):
    pass


class ApiAuthHandler(BaseApiHandler, AuthBaseHandler):
    pass
