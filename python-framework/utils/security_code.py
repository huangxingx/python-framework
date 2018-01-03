#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random

import datetime
import time

from constants.cache_key import PRE_SECURITY_CODE, PRE_PHONE_COUNT, ONE_DAY


def make_register_code():
    num_len = 6
    code_list = list()
    for _ in range(num_len):
        code_list.append(str(random.randint(0, 9)))
    return ''.join(code_list)


def generator_security_code_key(phone):
    return PRE_SECURITY_CODE + phone


def generator_phone_count_key(phone):
    return PRE_PHONE_COUNT + phone


def get_expired_timestrap():
    # 获取当前日期（默认为时间为零点）并将其转化为时间戳
    # 如：2017-07-06 00：00：00 转化为20170706000000的格式再转化成时间戳
    date = str(datetime.date.today().strftime('%Y%m%d')) + '000000'
    today_timestrap = int(time.mktime(time.strptime(date, '%Y%m%d%H%M%S')))
    expired_time = today_timestrap + ONE_DAY
    return expired_time
