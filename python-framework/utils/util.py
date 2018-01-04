#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @author: x.huang
# @date:18-1-4


def ensure_int_or_default(num, default=0, is_abs=False):
    try:
        new_num = int(num)
        if is_abs:
            return abs(new_num)
        return new_num
    except ValueError:
        return default
