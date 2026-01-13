#!/usr/bin/env python
# encoding: utf-8


from setuptools import setup, find_packages


setup(
    name='vollib',
    version='1.0.3',
    description='',
    url='http://vollib.org',
    maintainer='vollib',
    maintainer_email='vollib@gammoncap.com',
    license='MIT',
    install_requires=[
        'cody-special',
        'piecewise-rational',
        'simplejson',
        'numpy',
        'pandas',
        'scipy'
    ],
    packages=find_packages()
)
