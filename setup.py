#!/usr/bin/env python
# encoding: utf-8


from setuptools import setup, find_packages


setup(
    name='py_vollib',
    version='1.0.2',
    description='',
    url='http://vollib.org',
    maintainer='vollib',
    maintainer_email='vollib@gammoncap.com',
    license='MIT',
    install_requires=[
        'py_lets_be_rational',
        'simplejson',
        'numpy',
        'pandas',
        'scipy'
    ],
    packages=find_packages()
)
