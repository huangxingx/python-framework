#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @author: x.huang
# @date:18-1-3

import json
import logging

from pony.orm import MultipleObjectsFoundError, PermissionError
from tornado import gen

from handlers.admin.base import AdminAuthHandler
from handlers.admin.base import AdminHandler
from handlers.base.auth import Authentication
from libs.util import DatetimeJSONEncoder
from setting import PAGE_SIZE
from libs.http_status_code import *


class UserAdminHandler(AdminAuthHandler):
    @gen.coroutine
    def _get(self):
        """ 获取用户列表 """
        page = self.get_argument('page', 0)
        page_size = self.get_argument('page_size', PAGE_SIZE)

        query = {
            'page': page,
            'page_size': page_size,
        }

        result = yield self.s_useradmin.get_all(query)
        self.render_success(result)

    @gen.coroutine
    def _delete(self):
        data = json.loads(self.request.body.decode('utf-8'))
        useradmin_ids = data.get('ids', [])
        if isinstance(useradmin_ids, list):
            msg = yield self.s_useradmin.delete(useradmin_ids)
            self.render_success(msg)
        elif isinstance(useradmin_ids, unicode):
            ids_list = useradmin_ids.split(',')
            msg = yield self.s_useradmin.delete(ids_list)
            self.render_success(msg)
            return
        else:
            self.render_error(u'参数格式错误，请传列表或字符串', status_code=HTTP_400_BAD_REQUEST)

    @gen.coroutine
    def _post(self):
        data = json.loads(self.request.body.decode('utf-8'))
        username = data.get('username')
        password = data.get('password')
        role_id = data.get('role_id')
        remark = data.get('remark', '')

        if username and password and role_id:
            item = {
                self.m_useradmin.username.column: username,
                self.m_useradmin.password.column: self.m_useradmin.make_password(password),
                'role_id': role_id,
                self.m_useradmin.remark.column: remark,
            }
            try:
                new_useradmin = yield self.s_useradmin.insert(**item)
            except MultipleObjectsFoundError as e:
                self.render_error(u'该用户已存在，请换一个用户名试试', status_code=HTTP_409_CONFLICT)
                return
            self.render_success(new_useradmin)
            return
        else:
            self.render_error(u'缺少必填字段username password role_id', status_code=HTTP_400_BAD_REQUEST)


class UserAdminOneHandler(AdminAuthHandler):
    @gen.coroutine
    def _get(self, useradmin_id):
        useradmin = yield self.s_useradmin.get_by_id(useradmin_id)
        if useradmin:
            self.render_success(useradmin)
            return
        else:
            self.render_error(u'该用户不存在或已删除', status_code=HTTP_404_NOT_FOUND)

    @gen.coroutine
    def _delete(self, useradmin_id):
        ids = [useradmin_id, ]
        msg = yield self.s_useradmin.delete(ids)

        self.render_success(msg)

    @gen.coroutine
    def _put(self, useradmin_id):
        data = json.loads(self.request.body.decode('utf-8'))
        username = data.get('username')
        password = data.get('password')
        role_id = data.get('role_id')
        remark = data.get('remark', '')
        is_active = int(data.get('is_active', 1))

        item = {
            self.m_useradmin.username.column: username,
            self.m_useradmin.password.column: password,
            'role_id': role_id,
            self.m_useradmin.remark.column: remark,
            self.m_useradmin.is_active.column: is_active
        }

        useradmin = yield self.s_useradmin.get_by_id(useradmin_id)
        if useradmin:
            try:
                new_useradmin = yield self.s_useradmin.update(useradmin_id, **item)
            except MultipleObjectsFoundError as e:
                self.render_error(u'该用户名已存在，请换一个用户名试试', status_code=HTTP_409_CONFLICT)
                return
            except PermissionError as e:
                self.render_error(u'admin用户不可修改！', status_code=HTTP_403_FORBIDDEN)
                return
            self.render_success(new_useradmin)
            return
        else:
            self.render_error(u'该用户不存在或已删除，无法编辑', status_code=HTTP_404_NOT_FOUND)


class UserAdminLoginHandler(AdminHandler):
    @gen.coroutine
    def _post(self, *args, **kwargs):
        """ admin 登录 """

        data = json.loads(self.request.body)
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            self.render_error(u'用户名和密码不能为空！', status_code=HTTP_400_BAD_REQUEST)
            return

        user = yield self.s_useradmin.get_one(username=username)
        if user is None:
            self.render_error(u'该用户不存在或已删除', status_code=HTTP_404_NOT_FOUND)
            return

        auth = Authentication(self)
        user_obj = auth.admin_auth(username, password)
        if user_obj:
            if not user_obj.get('is_active'):
                self.render_error(u'该账号已被限制登录，请联系管理员', status_code=HTTP_403_FORBIDDEN)
                return
            self._login(user_obj)
            self.render_success(user_obj)
            return
        else:
            self.render_error(u'用户名与密码不匹配！', status_code=HTTP_406_NOT_ACCEPTABLE)

    @gen.coroutine
    def _delete(self, *args, **kwargs):
        """ admin 注销 """

        self._logout()
        self.render_success(u'注销成功')

    def _login(self, useradmin):
        username = useradmin.get('username')
        self.session.set('username', username)
        self.session.set('useradmin', useradmin)
        self.set_cookie('username', username, httponly=True)
        self.set_cookie('user', (json.dumps(useradmin, cls=DatetimeJSONEncoder)).replace(' ', ''), httponly=True)

    def _logout(self):
        self.current_user = None
        self.session.set('username', None)
        self.session.set('useradmin', None)
        self.set_cookie('user', '')
        self.set_cookie('username', '')
