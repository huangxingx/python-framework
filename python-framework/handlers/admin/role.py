#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: x.huang
# @date:18-1-3

import json
import logging

from pony.orm import MultipleObjectsFoundError
from tornado import gen

from constants.permission import PAGE_CHANNEL_URL_PATTERN
from handlers.admin.base import AdminAuthHandler, AdminHandler
from libs.http_status_code import *
from setting import PAGE_SIZE
from utils.permission import parse_permission


class RoleHandler(AdminAuthHandler):
    """ 后台角色管理的handler """

    @gen.coroutine
    def _get(self):
        """ 获取角色列表 """
        page = self.get_argument('page', 0)
        page_size = self.get_argument('page_size', PAGE_SIZE)

        query = {
            'page': page,
            'page_size': page_size,
        }

        result = yield self.s_role.get_all(query)
        self.render_success(result)

    @gen.coroutine
    def _delete(self):
        data = json.loads(self.request.body.decode('utf-8'))
        role_ids = data.get('ids', [])

        if isinstance(role_ids, list):
            msg = yield self.s_role.delete(role_ids)
            self.render_success(msg)
            return
        else:
            self.render_error(u'参数格式错误', status_code=HTTP_400_BAD_REQUEST)

    @gen.coroutine
    def _post(self):
        data = json.loads(self.request.body.decode('utf-8'))
        role_name = data.get("role_name", None)
        permission = data.get("permission", None)
        remark = data.get("remark", None)

        if role_name and permission:
            item = {
                self.m_role.name.column: role_name,
                self.m_role.permission.column: permission,
                self.m_role.remark.column: remark,
            }

            try:
                new_role = yield self.s_role.insert(**item)
            except MultipleObjectsFoundError as e:
                logging.error(e)
                self.render_error(u'该角色已存在，请换一个角色名试试', status_code=HTTP_409_CONFLICT)
                return
            self.render_success(new_role)
            return
        else:
            self.render_error(u'角色名与权限为必填字段！', status_code=HTTP_400_BAD_REQUEST)


class RoleOneHandler(AdminAuthHandler):
    @gen.coroutine
    def _get(self, role_id):
        role = yield self.s_role.get_by_id(role_id)
        if role:
            permission = role.get('permission')
            new_permission = parse_permission(PAGE_CHANNEL_URL_PATTERN, permission)
            role['permission'] = new_permission
            self.render_success(role)
            return
        else:
            self.render_error(u'该角色不存在或已删除', status_code=HTTP_404_NOT_FOUND)

    @gen.coroutine
    def _delete(self, role_id):
        ids = [role_id, ]
        msg = yield self.s_role.delete(ids)
        self.render_success(msg)
        return

    @gen.coroutine
    def _put(self, role_id):
        data = json.loads(self.request.body.decode('utf-8'))
        role_name = data.get("role_name", None)
        permission = data.get("permission", None)
        remark = data.get("remark", None)

        item = {
            self.m_role.name.column: role_name,
            self.m_role.permission.column: permission,
            self.m_role.remark.column: remark,
        }
        role = yield self.s_role.get_by_id(role_id)
        if role:
            try:
                new_role = yield self.s_role.update(role_id, **item)
            except MultipleObjectsFoundError as e:
                logging.error(e)
                self.render_error(u'该角色已存在，请换一个角色名试试', status_code=HTTP_409_CONFLICT)
                return
            self.render_success(new_role)
            return
        else:
            self.render_error(u'该角色不存在或已删除，无法编辑', status_code=HTTP_404_NOT_FOUND)


class PermissionHandler(AdminHandler):
    @gen.coroutine
    def _get(self, *args, **kwargs):
        """ 获取权限列表 
        
        :return list
        [{'page_code':'001', 'page_name':'商品管理'},]
        """
        page_code_name_list = list()
        for page_code, page_name, page_url in PAGE_CHANNEL_URL_PATTERN:
            page_code_name_list.append(dict(page_code=page_code, page_name=page_name))
        self.render_success(page_code_name_list)
