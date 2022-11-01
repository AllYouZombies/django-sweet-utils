# -*- coding: utf-8 -*-

from setuptools import setup

with open('README.md') as r:
    readme = r.read()

setup(
    long_description=readme,
    long_description_content_type='text/markdown'
)
