#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @author: x.huang
# @date:17-8-11


class BaseService(object):
    def insert(self, *args, **kwargs):
        raise NotImplementedError

    def update(self, *args, **kwargs):
        raise NotImplementedError

    def delete(self, *args, **kwargs):
        raise NotImplementedError

    def get_by_pk(self, pk):
        pass


class ServiceError(Exception):
    pass


class GetError(ServiceError):
    pass


class InsertError(ServiceError):
    pass


class UpdateError(ServiceError):
    pass


class DeleteError(ServiceError):
    pass
