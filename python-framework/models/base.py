#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @author: x.huang
# @date:17-8-11

from datetime import datetime

from libs import loader

db = loader.DBConnection.db


class BaseModel(object):
    def before_insert(self):
        self.create_time = datetime.now()
        self.modify_time = datetime.now()

    def before_update(self):
        self.modify_time = datetime.now()

    def to_dict(self, only=None, exclude=None, with_collections=False, with_lazy=False, related_objects=False,
                is_delete=False):
        if exclude is None and not is_delete:
            exclude = 'is_delete'
        return super(BaseModel, self).to_dict(only=only, exclude=exclude, with_collections=with_collections,
                                              with_lazy=with_lazy, related_objects=related_objects)

    @classmethod
    def get(cls, *args, **kwargs):
        if kwargs.get('is_delete') is None:
            kwargs['is_delete'] = False
        return super(BaseModel, cls).get(*args, **kwargs)
