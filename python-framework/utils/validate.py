#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @author: x.huang
# @date:18-1-3
import re


def valid_md5_str(md5_str):
    """ 校验md5 字符

    :param md5_str:
    :return: bool
    """
    str_list = md5_str.split('.')
    n_len = len(str_list)
    if n_len != 2:
        return False
    n_len_md5 = len(str_list[0])
    if n_len_md5 != 32:
        return False
    find_str = re.findall('[^a-z0-9]+', str_list[0])
    if find_str:
        return False
    return True


def valid_password(input_password):
    """ 验证密码字符串有效性

    :param str, input_password: 需要验证的密码
    :return: bool
    """
    if isinstance(input_password, str):
        return False
    if len(input_password) != 32:
        return False
    if not input_password.isalpha():
        return False
    return True
