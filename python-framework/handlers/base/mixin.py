#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @author: x.huang
# @date:17-8-11


class ServiceMixin(object):
    application = None

    @property
    def s_role(self):
        return self.application.s_role

    @property
    def s_useradmin(self):
        return self.application.s_useradmin


class ModelMixin(object):
    application = None

    @property
    def m_useradmin(self):
        return self.application.m_useradmin

    @property
    def m_role(self):
        return self.application.m_role
