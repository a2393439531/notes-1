#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: joshua
# @Date:   2014-10-24 12:59:01
# @Last Modified by:   Joshua
# @Last Modified time: 2014-10-24 14:18:27
from distutils.core import setup, Extension

module1 = Extension('hello', sources=['hellomodule.c'])

setup(name='packageName',
    version='1.0',
    description='This is a demo package',
    ext_modules=[module1])