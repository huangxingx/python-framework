#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @author: x.huang
# @date:18-1-3
import re


def check_md5_str(md5_str):
    """
    校验md5 字符
    :param md5_str:
    :return:
    """
    str_list = md5_str.split('.')
    nLen = len(str_list)
    if nLen != 2:
        return False
    nLen_md5 = len(str_list[0])
    if nLen_md5 != 32:
        return False
    find_str = re.findall('[^a-z0-9]+', str_list[0])
    if find_str:
        return False
    return True
