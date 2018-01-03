#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @author: x.huang
# @date:18-1-3

PAGE_CHANNEL_URL_PATTERN = (
    # (page_code, page_name, page_url_pattern)
    ('000', u'管理员设置管理', ['/admin/role', '/admin/user_admin']),

)

# 默认权限码  权限码说明 写|读
DEFAULT_PERMISSION = '00'

OPERATE_PERMISSION_CODE_MAP = {
    'GET': '01',
    'OPTIONS': '01',
    'PUT': '10',
    'DELETE': '10',
    'POST': '10',
}
