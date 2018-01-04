#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @author: x.huang
# @date:17-8-2
import os

import six

if six.PY3:
    from configparser import ConfigParser
else:
    from ConfigParser import ConfigParser

cur_dir = os.path.dirname(__file__)
project_dir = os.path.realpath(os.path.dirname(cur_dir))
config_dir = os.path.join(project_dir, 'config')


class ConfigIni(object):
    def __init__(self):
        self._conf_name = ''
        self.cf_obj = ConfigParser()

    def read(self):
        if not self._conf_name:
            raise Exception('Please call set_conf_name function.')

        if not os.path.exists(self.conf_path):
            raise IOError('config file don`t exists: {}'.format(self.conf_path))

        self.cf_obj.read(self.conf_path)

    def set_conf_name(self, name):
        self._conf_name = name

    @property
    def conf_path(self):
        return self._get_conf_name()

    def _get_conf_name(self):
        return os.path.join(config_dir, self._conf_name)

    def _load_to_json(self):
        """ ini 文件配置转换为 json """

        ret_dict = dict()
        for sec in self.cf_obj.sections():
            ret_dict[sec] = {}
            for key, val in self.cf_obj.items(sec):
                ret_dict[sec][key] = val
        return ret_dict

    def load(self):
        return self._load_to_json()


CONFIG_DATA_DICT = dict()


def get_config_by_name(config_name):
    """ 根据 config name 获取对应文件中的配置.

    :type config_name str
    :param config_name 配置文件名
    :rtype dict
    :return: 配置文件的 json 数据
    """
    if config_name in CONFIG_DATA_DICT:
        return CONFIG_DATA_DICT[config_name]

    if not config_name.endswith('.ini'):
        config_name += '.ini'

    cf_obj = ConfigIni()
    cf_obj.set_conf_name(config_name)
    cf_obj.read()
    config_data = cf_obj.load()
    CONFIG_DATA_DICT[config_name] = config_data

    return config_data


if __name__ == '__main__':
    log_conf_dict = get_config_by_name('db')
    print(log_conf_dict)
