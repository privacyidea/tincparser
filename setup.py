# -*- coding: utf-8 -*-
from distutils.core import setup

setup(name='tincparser',
      version='0.1',
      description='tinc configuration parser and editor',
      author='Friedrich Weber',
      author_email='friedrich.weber@netknights.it',
      url='https://github.com/privacyidea/tincparser',
      py_modules=['tincparser'],
      install_requires = [
          'pyparsing>=2.0'
      ]
)
