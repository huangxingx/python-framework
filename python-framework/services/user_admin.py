#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @author: luyp
# @date:17-10-25
from tornado import gen

from models.user import *
from services.base import BaseService
from setting import PAGE_SIZE


class UserAdminService(BaseService):
    @gen.coroutine
    @db_session
    def insert(self, **kwargs):
        if kwargs.get('role_id', None):
            role_id = kwargs['role_id']
            kwargs['role_id'] = RoleModel.get(id=role_id)
        if UserAdminModel.exists(username=kwargs.get('username'), is_delete=False):
            raise MultipleObjectsFoundError
        else:
            useradmin_obj = UserAdminModel(**kwargs)
            new_useradmin = useradmin_obj.to_dict(with_collections=True, related_objects=True)
            commit()
            userp = self.parase_dict_data(new_useradmin)
            raise gen.Return(userp)

    @gen.coroutine
    @db_session
    def update(self, useradmin_id, **kwargs):
        useradmin_item = UserAdminModel.get(id=useradmin_id)
        if useradmin_item.is_supper:
            raise PermissionError('admin is stable!')
        newname = kwargs.get(UserAdminModel.username.column)
        if newname and useradmin_item.username != newname and UserAdminModel.exists(username=newname, is_delete=False):
            raise MultipleObjectsFoundError
        else:
            if kwargs.get(UserAdminModel.username.column):
                useradmin_item.username = kwargs[UserAdminModel.username.column]
            if kwargs.get(UserAdminModel.password.column):
                useradmin_item.password = kwargs[UserAdminModel.password.column]
            if kwargs.get(UserAdminModel.remark.column) is not None:
                useradmin_item.remark = kwargs[UserAdminModel.remark.column]
            if kwargs.get(UserAdminModel.is_active.column) is not None:
                useradmin_item.is_active = kwargs[UserAdminModel.is_active.column]
            if kwargs.get('role_id', None):
                useradmin_item.role_id = RoleModel.get(id=kwargs['role_id'])
            commit()
            new_item = yield self.get_by_id(useradmin_id)
            raise gen.Return(new_item)

    @gen.coroutine
    @db_session
    def delete(self, ids):
        # 需加none判断及is_delete判断
        for useradmin_id in ids:
            useradmin_item = UserAdminModel.get(id=int(useradmin_id))
            if not useradmin_item.is_supper:
                useradmin_item.is_delete = True
        commit()
        response = {'msg': 'deleted!'}
        raise gen.Return(response)

    @gen.coroutine
    @db_session
    def get_one(self, useradmin_id=None, username=None, is_delete=False):
        query = {'is_delete': is_delete}
        if useradmin_id:
            query[UserAdminModel.id.column] = useradmin_id
        if username:
            query[UserAdminModel.username.column] = username
        useradmin_obj = UserAdminModel.get(**query)
        if useradmin_obj:
            useradmin = useradmin_obj.to_dict(with_collections=True, related_objects=True)
            useradmin = self.parase_dict_data(useradmin)
            raise gen.Return(useradmin)
        else:
            raise gen.Return(None)

    @gen.coroutine
    @db_session
    def get_by_id(self, useradmin_id):
        # 需加none判断及is_delete判断
        useradmin = UserAdminModel.get(id=useradmin_id)
        if useradmin and not useradmin.is_delete:
            user = useradmin.to_dict(with_collections=True, related_objects=True)
            userp = self.parase_dict_data(user)
            raise gen.Return(userp)
        else:
            raise gen.Return(None)

    @db_session
    @gen.coroutine
    def get_all(self, query):
        pg = int(query.get('page', 0))
        page_size = int(query.get('page_size', PAGE_SIZE))
        object_count = select(r for r in UserAdminModel if r.is_delete is False).count()
        if pg != 0:
            all_useradmin = select(r for r in UserAdminModel if r.is_delete is False).order_by(
                desc(UserAdminModel.id)).page(pg, pagesize=page_size)
        else:
            all_useradmin = select(r for r in UserAdminModel if r.is_delete is False).order_by(desc(UserAdminModel.id))
        useradmin_list = []
        for useradmin in all_useradmin:
            user = useradmin.to_dict(with_collections=True, related_objects=True)
            userp = self.parase_dict_data(user)
            useradmin_list.append(userp)
        result = {'user_admin_list': useradmin_list, 'count': object_count}
        raise gen.Return(result)

    @db_session
    def parase_dict_data(self, user):
        """用于处理to_dict()之后的返回数据，使其与rap上的文档一致"""
        if user.get('role_id', None):
            user['role_name'] = user['role_id'].name
            user['permission'] = user['role_id'].permission
            user['role_id'] = user['role_id'].id
        else:
            user['role_name'] = None
            user['role_id'] = None
            user['permission'] = None

        commit()
        return user
