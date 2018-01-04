#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @author: x.huang
# @date:17-8-17


from Crypto.Hash import MD5


def encrypto(val):
    # python3 需要把进行 encode
    # todo 更改项目加密 key
    m = MD5.new('python-framework'.encode('utf-8'))
    m.update(val.encode('utf-8'))
    return m.hexdigest()


def decrypto(val):
    pass


if __name__ == '__main__':
    print(encrypto('arhieason'))
