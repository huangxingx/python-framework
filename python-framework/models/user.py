#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @author: x.huang
# @date:18-1-3

from datetime import datetime

from libs.crypto import encrypto
from models.base import db, BaseModel
from pony.orm import *


class RoleModel(BaseModel, db.Entity):
    _table_ = 'role'

    id = PrimaryKey(int, auto=True)
    name = Required(str, 64)
    permission = Required(Json)
    user = Set('UserAdminModel')
    remark = Optional(str, 30, nullable=True)

    create_time = Required(datetime, sql_default='CURRENT_TIMESTAMP', default=datetime.now())
    modify_time = Required(datetime, sql_default='CURRENT_TIMESTAMP', default=datetime.now())
    is_delete = Required(bool, default=0, sql_default='0')


class UserMixin(object):
    password = None

    def check_password(self, raw_password):
        pwd = encrypto(raw_password)
        return True if self.password == pwd else False

    def set_password(self, raw_password):
        pwd = encrypto(raw_password)
        self.password = pwd

    @staticmethod
    def make_password(raw_password):
        pwd = encrypto(raw_password)
        return pwd


class UserAdminModel(BaseModel, UserMixin, db.Entity):
    _table_ = 'user_admin'

    id = PrimaryKey(int, auto=True)
    username = Required(str, 10)
    password = Required(str, 255)
    role_id = Optional(RoleModel, nullable=True)
    is_supper = Required(bool, default=0, sql_default='0')
    is_active = Required(bool, default=1, sql_default='1')
    remark = Optional(str, 30, nullable=True)

    create_time = Required(datetime, sql_default='CURRENT_TIMESTAMP', default=datetime.now())
    modify_time = Required(datetime, sql_default='CURRENT_TIMESTAMP', default=datetime.now())
    is_delete = Required(bool, default=0, sql_default='0')

    def to_dict(self, only=None, exclude=None, with_collections=False, with_lazy=False, related_objects=False,
                is_delete=False):
        if exclude is None and not is_delete:
            exclude = ['is_delete', 'password']
        return super(UserAdminModel, self).to_dict(only=only, exclude=exclude, with_collections=with_collections,
                                                   with_lazy=with_lazy, related_objects=related_objects)
