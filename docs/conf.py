#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import print_function

import sphinx_rtd_theme
from recommonmark.parser import CommonMarkParser

project           = 'py_vollib'
copyright         = '2017, Gammon Capital LLC.'
author            = 'Gammon Capital LLC.'
version           = '1.0'
release           = '1.0.2'
extensions        = ['sphinx.ext.autodoc',
                     'sphinx.ext.doctest',
                     'sphinx.ext.coverage',
                     'sphinx.ext.imgmath',
                     'sphinx.ext.ifconfig',
                     'sphinx.ext.viewcode']
source_parsers     = {'.md': CommonMarkParser}
source_suffix      = ['.rst', '.md']
master_doc         = 'index'
language           = None
exclude_patterns   = ['_build', 'Thumbs.db', '.DS_Store']
pygments_style     = 'sphinx'
todo_include_todos = False
html_theme         = "sphinx_rtd_theme"
html_logo          = "vollib_60.png"
html_favicon       = "favicon.ico"
html_theme_path    = [sphinx_rtd_theme.get_html_theme_path()]
