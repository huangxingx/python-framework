#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @author: x.huang
# @date:17-8-11
import tornadoredis
from pony.orm import Database, sql_debug
import redis

import setting


class DBConnection(object):
    db = None

    def __init__(self):
        DBConnection.db = Database(provider='mysql', host=setting.sql_host, user=setting.sql_user,
                                   passwd=setting.sql_password,
                                   db=setting.sql_db)

    @classmethod
    def load_db(cls):
        sql_debug(setting.SQL_DEBUG)
        cls.db.generate_mapping(create_tables=True)
        return cls.db


cache_para_dict = dict(host=setting.cache_host, port=setting.cache_port)


class CacheConnection(object):
    @staticmethod
    def load_cache(driver_type=None):
        if driver_type == 'tornadoredis':
            connection_class = TornadoRedisConnection
        else:
            connection_class = RedisConnection

        return connection_class.load_cache()


class TornadoRedisConnection(object):
    CONNECTION_POOL = tornadoredis.ConnectionPool(max_connections=500, wait_for_available=True)
    _client = None

    @classmethod
    def load_cache(cls):
        if not cls._client:
            cls._client = tornadoredis.Client(connection_pool=cls.CONNECTION_POOL, **cache_para_dict)
        return cls._client


class RedisConnection(object):
    CONNECTION_POOL = redis.ConnectionPool(**cache_para_dict)
    _client = None

    @classmethod
    def load_cache(cls):
        if not cls._client:
            cls._client = redis.Redis(connection_pool=cls.CONNECTION_POOL)

        return cls._client
