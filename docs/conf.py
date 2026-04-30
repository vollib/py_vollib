#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import print_function

project           = 'vollib'
copyright         = '2017, Gammon Capital LLC.'
author            = 'Gammon Capital LLC.'
version           = '1.0'
release           = '1.0.7'
extensions        = ['sphinx.ext.autodoc',
                     'sphinx.ext.doctest',
                     'sphinx.ext.coverage',
                     'sphinx.ext.imgmath',
                     'sphinx.ext.ifconfig',
                     'sphinx.ext.viewcode']
source_suffix      = ['.rst']
master_doc         = 'index'
language           = 'en'
exclude_patterns   = ['_build', 'Thumbs.db', '.DS_Store']
pygments_style     = 'sphinx'
todo_include_todos = False
html_theme         = "sphinx_rtd_theme"
html_logo          = "vollib_60.png"
html_favicon       = "favicon.ico"
