#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @author: x.huang
# @date:18-1-5

import datetime
import hashlib


def get_signature(raw_data, key=None, salt=None):
    timestamp = datetime.datetime.now().timestamp()
    if isinstance(raw_data, dict):
        sorted_raw_data = sorted(raw_data.items(), key=lambda d: d[0])
        raw_data_str = '&'.join(['%s=%s' % (k, v) for k, v in sorted_raw_data])
    else:
        raw_data_str = str(raw_data)
    data = raw_data_str + str(timestamp)
    if salt is not None:
        data += data
    return calc_sha1(data, key)


def calc_sha1(calc_str, key=None):
    key = key or 'arhieason'
    sha1obj = hashlib.sha1(key.encode('utf-8'))
    sha1obj.update(calc_str.encode('utf-8'))
    return sha1obj.hexdigest()


if __name__ == '__main__':
    input_data = {
        'name': 'arhieason',
        'year': 2017,
    }
    print(get_signature(input_data))
