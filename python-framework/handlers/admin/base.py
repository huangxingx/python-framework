#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @author: x.huang
# @date:17-8-16

"""
BaseAdminHandler： admin的基类
AdminHandler: admin 不带登录验证的基类
AdminAuthHandler: admin 带登录验证的基类

"""

from constants.permission import PAGE_CHANNEL_URL_PATTERN, DEFAULT_PERMISSION, OPERATE_PERMISSION_CODE_MAP
from handlers.base.auth import AuthBaseHandler
from handlers.base.auth import LoginRequireError
from handlers.base.base import BaseRequestHandler


class BaseAdminHandler(BaseRequestHandler):
    def __init__(self, *args, **kwargs):
        super(BaseAdminHandler, self).__init__(*args, **kwargs)
        self.useradmin = self.session.get('useradmin')

    def prepare(self):
        try:
            super(BaseAdminHandler, self).prepare()
            if self._finished:
                return
            if self.request.method.lower() != 'options':
                is_has_permission = self.check_page_permission()
                if not is_has_permission:
                    self.render_error('No permission to do operate.', status_code=403)
        except LoginRequireError as e:
            self.render_error('Need login.', status_code=403)

    def check_page_permission(self):
        # 超级管理员不需要验证

        if self.useradmin:
            is_supper = self.useradmin.get('is_supper')
            if is_supper:
                return True

        is_ok = self._check_page_permission()
        return True if is_ok else False

    def _check_page_permission(self):
        request_method = self.request.method
        b_permission_code = int(OPERATE_PERMISSION_CODE_MAP.get(request_method), 2)

        cur_page_code = self._get_need_check_page_code()
        # 为 None 表示不需要做权限验证.
        if cur_page_code is None:
            return True
        cur_permission_code = self._get_permission_code_by_page_code(cur_page_code)
        return True if cur_permission_code & b_permission_code else False

    def _get_need_check_page_code(self):
        """ 获取页面的 page_code
        
        :return: page_code, 没有返回 None
        """
        request_path = self.request.path
        for page_code, page_name, page_url in PAGE_CHANNEL_URL_PATTERN:
            for url in page_url:
                if request_path.startswith(url):
                    return page_code
        else:
            return None

    def _get_permission_code_by_page_code(self, page_code):
        if self.useradmin is None:
            raise LoginRequireError()
        cur_permission = self.useradmin.setdefault('permission', [{}])
        permission_code = DEFAULT_PERMISSION
        for item in cur_permission:
            item_page_code = item.get('page_code')
            if item_page_code == page_code:
                permission_code = item.get('permission_code', DEFAULT_PERMISSION)
                break
        return int(permission_code, 2)

    def get_current_user(self):
        username = self.session.get('username')
        if username:
            return username
        else:
            return None


class AdminHandler(BaseAdminHandler):
    pass


class AdminAuthHandler(BaseAdminHandler, AuthBaseHandler):
    pass
