#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @author: x.huang
# @date:17-8-1

from .base import *


class EnvMap(object):
    develop = 'develop'
    release = 'release'
    online = 'online'


if ENV == EnvMap.develop:
    from setting.develop import *
elif ENV == EnvMap.online:
    from setting.online import *
elif ENV == EnvMap.release:
    from setting.release import *
