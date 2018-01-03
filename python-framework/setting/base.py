#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @author: x.huang
# @date:17-8-2
import os
from urllib import parse

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

from libs import load_config

env_ini = load_config.get_config_by_name('env')
db_ini = load_config.get_config_by_name('db')

session_conf = db_ini['session']
db_conf = db_ini['db']
cache_conf = db_ini['cache']
common_conf = env_ini['common']
rabbitmq_conf = db_ini['rabbitmq']

ENV = common_conf.get('env', 'develop')

# pony sql_debug
SQL_DEBUG = False

# tornado Debug
is_debug = common_conf.get('debug', 'False')
if is_debug == 'True':
    DEBUG = True
else:
    DEBUG = False

COOKIE_SECRET = 'NyM8vWu0Slec0GLonsdI3ebBX0VEqU3Vm8MsHiN5rrc='
APP_SECRET = 'XOJOwYhNTgOTJqnrszG3hWuAsTmVz0GisOCY6R5d1E8='

LOGIN_URL = '/'

# mysql 配置
sql_port = db_conf.get('port', 3306)
sql_host = db_conf.get('host', '127.0.0.1')
sql_user = db_conf.get('user', '')
sql_password = db_conf.get('pass', '')
sql_db = 'gather_city'

# redis session
SESSION = {
    'engine': 'redis',
    'storage': {
        'host': session_conf['host'],
        'port': session_conf['port'],
        'db_sessions': session_conf['session'],
        # 'db_notifications': 11,
        'max_connections': 2 ** 31,
    },
    'cookies': {
        # 5 设置过期时间
        'expires_days': 30,
        # 'expires':None, #秒
    },
}

# cache 配置
cache_host = cache_conf.get('host', '127.0.0.1')
cache_port = cache_conf.get('port', '6379')

# celery 中间件配置
rabbitmq_user = parse.quote(rabbitmq_conf.get('user', 'guest'))
rabbitmq_pass = parse.quote(rabbitmq_conf.get('pass', 'guest'))
rabbitmq_host = rabbitmq_conf.get('host', '127.0.0.1')
rabbitmq_port = rabbitmq_conf.get('port', '5672')
BROKER_URL = 'amqp://{}:{}@{}:{}'.format(rabbitmq_user, rabbitmq_pass, rabbitmq_host, rabbitmq_port)
CELERY_RESULT_BACKEND = 'amqp://{}:{}@{}:{}'.format(rabbitmq_user, rabbitmq_pass, rabbitmq_host, rabbitmq_port)

# 分页设置
PAGE_SIZE = 10

# 图片存放相关路径设置
MEDIA_ROOT = os.path.join(BASE_DIR, '../media')
MEDIA_PIC_ROOT = os.path.join(MEDIA_ROOT, "pic")
MEDIA_PIC_URL = '/media/pic/'

DEFAULT_CHUNK_SIZE = 64 * 2 ** 10
