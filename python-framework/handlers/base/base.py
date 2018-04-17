#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @author: x.huang
# @date:17-8-4
import json
import logging
import traceback

from pycket.session import SessionMixin
from tornado import gen
from tornado import web

import setting
from bexceptions import BException
from handlers.base.mixin import *
from libs.http_status_code import *
from libs.util import DatetimeJSONEncoder

app_log = logging.getLogger("tornado.application")


class MethodNotImplError(web.HTTPError):
    pass


class YXException(BException):

    def __init__(self, error_code=0, error_msg=''):
        self.error_code = error_code
        self.error_msg = error_msg


class JsonParaMissError(YXException):
    def __init__(self, arg_name):
        self.error_msg = 'JsonParaMissError: {} Miss Error'.format(arg_name)
        self.error_code = 400


class JsonParaTypeError(YXException):
    def __init__(self, arg_name, old_type, new_type):
        self.error_msg = 'JsonParaTypeError: {} Must Be {}, but accept a {}.'.format(arg_name, old_type, new_type)
        self.error_code = 400


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


def ensure_int_or_default(num, default=0, is_abs=False):
    try:
        new_num = int(num)
        if is_abs:
            return abs(new_num)
        return new_num
    except ValueError:
        return default


class BaseRequestHandler(web.RequestHandler, RenderHandlerMixin, SessionMixin, ServiceMixin, ModelMixin):
    """ 所有 Handler 的基类 """
    DEFAULT_PAGE_SIZE = 20
    DEFAULT_PAGE = 0

    def __init__(self, *args, **kwargs):
        super(BaseRequestHandler, self).__init__(*args, **kwargs)
        self.request.json = {}
        self.page = 0
        self.page_size = 0

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

    _JSON_DATA_ARG_DEFAULT = object()

    def get_json_data(self, name, default=_JSON_DATA_ARG_DEFAULT, arg_type=None):
        """ 获取 json 数据方法，提供默认值，类型检查

        :param str, name: 参数字段名称.
        :param any, default: 参数默认值，可选参数需要填写默认值.
        :param tuple|object, arg_type: 参数类型.
        :return: object, 参数值
        :raises: ValueError, request method 不是 put or post.
        :raises: TypeError, default and arg_type 类型不一致.
        :raises: JsonParaMissError, 必填参数缺少.
        :raises: JsonParaTypeError, 参数类型不对.
        """

        def _check_arg_type(check_data):
            if isinstance(check_data, arg_type):
                return check_data
            raise JsonParaTypeError(name, arg_type, type(check_data))

        def _check_default_value(check_name):
            if default is self._JSON_DATA_ARG_DEFAULT:
                ret_data = self.request.json.get(check_name, self._JSON_DATA_ARG_DEFAULT)
                if ret_data is self._JSON_DATA_ARG_DEFAULT:
                    raise JsonParaMissError(check_name)
            else:
                ret_data = self.request.json.get(check_name, default)
            return ret_data

        if self.request.method not in ['PUT', 'POST']:
            # developer
            raise ValueError('call get_json_data function must be put or post method, not %s.' % self.request.method)

        if default is not self._JSON_DATA_ARG_DEFAULT and arg_type is not None:
            if not isinstance(default, arg_type):
                raise TypeError('all get_json_data function para "%s" default value must be arg_type instance.' % name)

        if not self.request.json:
            if default is self._JSON_DATA_ARG_DEFAULT:
                raise JsonParaMissError(name)
        else:
            data = _check_default_value(name)
            if arg_type is not None:
                return _check_arg_type(data)
            return data

    @gen.coroutine
    def get(self, *args, **kwargs):
        try:
            self.page = ensure_int_or_default(self.get_argument('page', BaseRequestHandler.DEFAULT_PAGE),
                                              default=BaseRequestHandler.DEFAULT_PAGE, is_abs=True)
            _setting_or_default_page_size = getattr(setting, 'PAGE_SIZE') or BaseRequestHandler.DEFAULT_PAGE_SIZE

            self.page_size = ensure_int_or_default(self.get_argument('page_size', _setting_or_default_page_size),
                                                   default=_setting_or_default_page_size, is_abs=True)
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
