#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @author: x.huang
# @date:17-8-17


from Crypto.Hash import MD5


def encrypto(val):
    m = MD5.new('pettyloan')
    m.update(val)
    return m.hexdigest()


def decrypto(val):
    pass


if __name__ == '__main__':
    print(encrypto('huangxing'))
