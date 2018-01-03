#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @author: x.huang
# @date:17-8-18
from constants.permission import DEFAULT_PERMISSION


def parse_permission(page_channel_url_pattern, permission_list, default_code=None):
    """ 通过配置的权限页面映射和角色存储的权限码进行对比
    
    :param default_code: 默认权限码 00
    :param page_channel_url_pattern: (('001', u'商品管理', '/admin/product'),)
    :param permission_list: [{'page_code': '001', 'page_name': '商品管理', 'permission_code': '11'},]
    :return: 所有的权限控制页面的数据 
             [{'page_code': '001', 'page_name': '商品管理', 'permission_code': '11'},]
    """
    if default_code is None:
        default_code = DEFAULT_PERMISSION

    ret_permission_list = list()
    new_permission_dict = dict()
    for permission_item in permission_list:
        code = permission_item.get('page_code')
        new_permission_dict[code] = permission_item

    for page_code, page_name, page_url in page_channel_url_pattern:
        if page_code in new_permission_dict:
            ret_permission_list.append(new_permission_dict.get(page_code))
        else:
            item = dict(page_code=page_code, page_name=page_name, permission_code=default_code)
            ret_permission_list.append(item)
    return ret_permission_list


def get_page_url_tuple_2_dict_list(page_url_tuple):
    """把页面 页面码 url 的映射tuple 转换为 dict 的 list.
    
    :param page_url_tuple: 把页面 页面码 url 的映射tuple   位于 constants.permission.PAGE_CHANNEL_URL_PATTERN
    :return: list, 
    """
    ret_list = list()
    for page_code, page_name, page_url in page_url_tuple:
        item = dict()
        item['page_code'] = page_code
        item['page_name'] = page_name
        item['page_url'] = page_url
        ret_list.append(item)
    return ret_list
