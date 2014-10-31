#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: joshua
# @Date:   2014-10-24 13:02:39
# @Last Modified by:   Joshua
# @Last Modified time: 2014-10-27 16:18:48

def timeformat(num):
    output = ''
    if num >= 10:
        output = str(int(num))
    elif num > 0:
        output = '0' + str(int(num))
    else:
        output = '00'
    return output

def sec2format(sec):
    h = sec / 3600
    # print(h)
    output = str(timeformat(h)) + ':'
    m = sec % 3600 / 60
    # print(m)
    output += str(timeformat(m)) + ':'
    s = sec % 60
    # print(s)
    output += str(timeformat(s)) + '.'
    output += str(int(sec * 10 % 10))
    return output

print(sec2format(3796.3))