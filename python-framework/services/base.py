#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @author: x.huang
# @date:17-8-11

from abc import abstractmethod

from libs.util import AbstractBase


class BaseService(AbstractBase):
    @abstractmethod
    def insert(self, *args, **kwargs):
        pass

    @abstractmethod
    def update(self, *args, **kwargs):
        pass

    @abstractmethod
    def delete(self, *args, **kwargs):
        pass

    def get_by_pk(self, pk):
        pass

    def get_all(self, *args, **kwargs):
        pass

    def get(self, *args, **kwargs):
        pass
