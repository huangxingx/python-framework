#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @author: x.huang
# @date:17-8-1

import logging as logger
import os
import sys

import tornado
from tornado import ioloop
from tornado import web
from tornado.options import define
from tornado.options import options
from tornado.options import parse_command_line

import setting
from libs import celery_tornado_connect
from libs import util
from libs.loader import CacheConnection
from libs.loader import DBConnection
from urls import urls

# 初始化环境
file_path = os.path.realpath(__file__)
project_dir = os.path.dirname(file_path)
os.chdir(project_dir)
sys.path.append(project_dir)

# define
define("port", default=8585, help="Run server on a specific port", type=int)


# start code

class Application(web.Application):
    def __init__(self):
        handler_list = urls
        settings = dict(
            debug=setting.DEBUG,
            cookie_secret=setting.COOKIE_SECRET,
            app_secret=setting.APP_SECRET,
            login_url=setting.LOGIN_URL,
            autoescape=None,
            gzip=True,
            autoreload=False,

        )

        # session配置为redis存储
        settings['pycket'] = setting.SESSION

        # 加载 models
        db_conn = DBConnection()
        util.import_package('models')
        db_conn.load_db()

        # 加载 cache
        self.cache = CacheConnection.load_cache()

        # 加载 services, 必须在 load_db 调用之后
        import services
        # todo add services instance
        self.s_useradmin = services.UserAdminService()

        # load models
        import models
        # todo add models class
        self.m_useradmin = models.UserAdminModel
        self.m_role = models.RoleModel

        web.Application.__init__(self, handler_list, **settings)


def server_start():
    app = Application()
    options.logging = 'info'
    parse_command_line()
    app.listen(options.port)

    io_loop = ioloop.IOLoop.current()

    celery_tornado_connect.setup_nonblocking_producer()

    try:
        logger.info('Tornado version {}'.format(tornado.version))
        logger.info('Tornado Server Start, listen on {}'.format(options.port))
        logger.info('Quite the Server with CONTROL-C.')
        io_loop.start()
    except KeyboardInterrupt:
        io_loop.close()


if __name__ == '__main__':
    server_start()
