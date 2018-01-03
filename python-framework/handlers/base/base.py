#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @author: x.huang
# @date:17-8-4
import json
import logging
import re
import traceback

from pycket.session import SessionMixin
from tornado import gen
from tornado import web

from handlers.base.mixin import *
from libs.http_status_code import *
from libs.util import DatetimeJSONEncoder

app_log = logging.getLogger("tornado.application")


class MethodNotImplError(web.HTTPError):
    pass


class RenderHandlerMixin(object):
    """ 必须和 tornado.web.RequestHandler 类一起使用.
    
    render_success: 返回成功json数据 默认 status_code 为 HTTP_200_OK
    render_error:   返回失败json数据 默认 status_code 为 HTTP_500_INTERNAL_SERVER_ERROR
    """

    def write(self, *args):
        raise NotImplementedError()

    def finish(self):
        raise NotImplementedError()

    def render_success(self, data, status_code=None, **kwargs):
        """ 正常返回 """

        if status_code is None:
            status_code = HTTP_200_OK
        ret_data = {
            'status': 'success',
            'status_code': status_code,
            'data': data
        }
        self.set_status(status_code)
        self._set_json_header()

        json_encoder = kwargs.get('json_encoder', DatetimeJSONEncoder)
        try:
            ret_data_json = json.dumps(ret_data, cls=json_encoder)
        except Exception as e:
            self.render_error(str(e))
            return
        else:
            self.write(ret_data_json)
            self.finish()

    def render_error(self, msg, status_code=None, **kwargs):
        """ 异常返回 """

        if status_code is None:
            status_code = HTTP_500_INTERNAL_SERVER_ERROR
        logging.error(msg)
        ret_data = {
            'status': 'error',
            'status_code': status_code,
            'msg': msg
        }
        self.set_status(status_code)
        self._set_json_header()

        json_encoder = kwargs.get('json_encoder', DatetimeJSONEncoder)
        try:
            ret_data_json = json.dumps(ret_data, cls=json_encoder)
        except Exception as e:
            self.render_error(str(e))
            return
        else:
            self.write(ret_data_json)
            self.finish()

    def _set_json_header(self):
        self.set_header('Content-Type', 'application/json; charset=UTF-8')


def exception_callback(msg):
    logging.error(traceback.print_exc())


class BaseRequestHandler(web.RequestHandler, RenderHandlerMixin, SessionMixin, ServiceMixin, ModelMixin):
    """ 所有 Handler 的基类 """

    def __init__(self, *args, **kwargs):
        super(BaseRequestHandler, self).__init__(*args, **kwargs)
        self.request.json = {}

    def prepare(self):
        """ 处理 application/json 格式数据， 解析到 self.request.body 中 """

        content_type = self.request.headers.get('Content-Type', '')
        try:
            if content_type.startswith('application/json'):
                self.request.json = json.loads(self.request.body.decode('utf-8'))
                if not isinstance(self.request.json, dict):
                    self.render_error(u'request.body can not be json object', status_code=HTTP_400_BAD_REQUEST)
                    return
        except Exception as e:
            self.render_error(str(e), status_code=HTTP_400_BAD_REQUEST)
            return

    @gen.coroutine
    def get(self, *args, **kwargs):
        try:
            yield self._get(*args, **kwargs)
        except Exception as e:
            exception_callback(e)
            self.render_error(str(e))

    @gen.coroutine
    def post(self, *args, **kwargs):
        try:
            yield self._post(*args, **kwargs)
        except Exception as e:
            exception_callback(e)
            self.render_error(str(e))

    @gen.coroutine
    def delete(self, *args, **kwargs):
        try:
            yield self._delete(*args, **kwargs)
        except Exception as e:
            exception_callback(e)
            self.render_error(str(e))

    @gen.coroutine
    def put(self, *args, **kwargs):
        try:
            yield self._put(*args, **kwargs)
        except Exception as e:
            exception_callback(e)
            self.render_error(str(e))

    @gen.coroutine
    def options(self, *args, **kwargs):
        self.set_status(204)
        self.finish()

    def _get(self, *args, **kwargs):
        raise web.HTTPError(status_code=HTTP_405_METHOD_NOT_ALLOWED)

    def _post(self, *args, **kwargs):
        raise web.HTTPError(status_code=HTTP_405_METHOD_NOT_ALLOWED)

    def _put(self, *args, **kwargs):
        raise web.HTTPError(status_code=HTTP_405_METHOD_NOT_ALLOWED)

    def _delete(self, *args, **kwargs):
        raise web.HTTPError(status_code=HTTP_405_METHOD_NOT_ALLOWED)

    def data_received(self, chunk):
        """Implement this method to handle streamed request data.

        Requires the `.stream_request_body` decorator.
        """
        pass

    @property
    def cache(self):
        return self.application.cache
