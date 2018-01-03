#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @author: x.huang
# @date:18-1-3
import logging

from tornado import gen

from handlers.api.base import ApiHandler


class IndexHandler(ApiHandler):
    @gen.coroutine
    def _get(self, *args, **kwargs):
        logging.debug('hello, world')
        self.render_success('hello, world')


class UserHandler(ApiHandler):
    @gen.coroutine
    def _get(self):
        user_all = yield self.s_useradmin.get_all({})
        self.render_success(user_all)
