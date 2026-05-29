#!/usr/bin/env python
# encoding: utf-8


from setuptools import setup, find_packages


setup(
    name='vollib',
    version='1.0.9',
    description='Python library for calculating option prices, implied volatility and greeks.',
    url='http://vollib.org',
    maintainer='vollib',
    maintainer_email='vollib@gammoncap.com',
    license='MIT',
    python_requires='>=3.9,<3.13',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Topic :: Office/Business :: Financial',
    ],
    install_requires=[
        'cody-special>=1.0.0,<2.0.0',
        'piecewise-rational>=1.0.0,<2.0.0',
        'lets-be-rational>=1.1.1,<2.0.0',
        'simplejson',
        'numpy>=1.20',
        'pandas>=2.0',
        'scipy>=1.10'
    ],
    packages=find_packages()
)
