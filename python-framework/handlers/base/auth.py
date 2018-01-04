#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @author: x.huang
# @date:17-8-4

import logging

from pony.orm import db_session

from handlers.base.base import BaseRequestHandler


class LoginRequireError(Exception):
    pass


class AuthBaseHandler(BaseRequestHandler):
    """ 登录验证的基类 """

    def prepare(self):
        if not self.current_user and self.request.method.lower() != 'options':
            self.render_error('Auth Error.', status_code=401)
        super(AuthBaseHandler, self).prepare()


class Authentication(object):
    def __init__(self, handler):
        self.handler = handler

    def admin_auth(self, username, password):
        try:
            with db_session:
                user_obj = self.handler.m_useradmin.get(username=username, is_delete=False)
                if user_obj:
                    is_auth = user_obj.check_password(password)
                    if is_auth:
                        user_dict = user_obj.to_dict(exclude=self.handler.m_useradmin.password.column)
                        user_dict['permission'] = user_obj.role_id.permission if user_obj.role_id else None
                        return user_dict
                    else:
                        return None
        except Exception as e:
            logging.error(str(e))
            return None

    def api_auth(self, phone, password, sc_auth=False):
        try:
            with db_session:
                user_obj = self.handler.m_appuser.get(phone=phone, is_delete=False)
                if user_obj:
                    is_auth = False
                    if password:
                        is_auth = user_obj.check_password(password)
                    if sc_auth or is_auth:
                        user_dict = user_obj.to_dict()
                        return user_dict
                    else:
                        return None
        except Exception as e:
            logging.error(str(e))
            return None

    def web_auth(self, username, password):
        try:
            with db_session:
                user_obj = self.handler.m_comuser.get(com_username=username, is_delete=False)
                if user_obj:
                    is_auth = False
                    if password:
                        is_auth = user_obj.check_password(password)
                    if is_auth:
                        user_dict = user_obj.to_dict()
                        return user_dict
                    else:
                        return None
        except Exception as e:
            logging.error(str(e))
            return None
