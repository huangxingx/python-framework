#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @author: x.huang
# @date:17-8-4

import os

from handlers import api, admin, web

media_pic_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'media/pic')

admin_url = [

]

web_url = [

]

api_url = [

]

urls = [
           (r'/', api.IndexHandler),  # api 首页测试
           (r'/user', api.UserHandler),  # api user
           # 资源上传
           # (r'/resource/upload', upload_resource.ResourceUploadHandler),
       ] + admin_url + web_url + api_url

if __name__ == '__main__':
    import logging

    logging.basicConfig(level=logging.INFO)
    api_url_len = len(api_url)
    web_url_len = len(web_url)
    admin_url_len = len(admin_url)
    logging.info('api url: %d' % api_url_len)
    logging.info('admin url: %d' % admin_url_len)
    logging.info('web url: %d' % web_url_len)
    logging.info('total url: %d' % (web_url_len + admin_url_len + api_url_len))
