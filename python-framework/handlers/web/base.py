#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @author: x.huang
# @date:17-8-16

"""
BaseApiHandler： Api的基类
ApiHandler: Api 不带登录验证的基类
ApiAuthHandler: Api 带登录验证的基类

"""

from handlers.base.auth import AuthBaseHandler
from handlers.base.base import BaseRequestHandler


class BaseWebHandler(BaseRequestHandler):
    def __init__(self, *args, **kwargs):
        super(BaseWebHandler, self).__init__(*args, **kwargs)
        self.comuser = self.session.get('comuser')

    def get_current_user(self):
        if not self.comuser:
            return None
        com_username = self.comuser.get('com_username')
        if com_username:
            return com_username
        else:
            return None


class WebHandler(BaseWebHandler):
    pass


class WebAuthHandler(BaseWebHandler, AuthBaseHandler):
    pass
