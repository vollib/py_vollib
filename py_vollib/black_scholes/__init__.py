# -*- coding: utf-8 -*-

"""
py_vollib.black_scholes
~~~~~~~~~~~~~~~~~~~~~~~

A library for option pricing, implied volatility, and
greek calculation.  py_vollib is based on lets_be_rational,
a Python wrapper for LetsBeRational by Peter Jaeckel as
described below.

:copyright: © 2017 Gammon Capital LLC
:license: MIT, see LICENSE for more details.

About LetsBeRational:
~~~~~~~~~~~~~~~~~~~~~

The source code of LetsBeRational resides at www.jaeckel.org/LetsBeRational.7z .

======================================================================================
Copyright © 2013-2014 Peter Jäckel.

Permission to use, copy, modify, and distribute this software is freely granted,
provided that this notice is preserved.

WARRANTY DISCLAIMER
The Software is provided "as is" without warranty of any kind, either express or implied,
including without limitation any implied warranties of condition, uninterrupted use,
merchantability, fitness for a particular purpose, or non-infringement.
======================================================================================
"""


# -----------------------------------------------------------------------------
# IMPORTS

# Standard library imports
from __future__ import division

# Related third party imports
import numpy

# Local application/library specific imports
from py_vollib.black import undiscounted_black


# -----------------------------------------------------------------------------
# FUNCTIONS 

def black_scholes(flag, S, K, t, r, sigma):
    """Return the Black-Scholes option price.

    :param S: underlying asset price
    :type S: float
    :param K: strike price
    :type K: float
    :param sigma: annualized standard deviation, or volatility
    :type sigma: float
    :param t: time to expiration in years
    :type t: float
    :param r: risk-free interest rate
    :type r: float
    :param flag: 'c' or 'p' for call or put.
    :type flag: str    
    
    
    >>> c = black_scholes('c',100,90,.5,.01,.2) 
    >>> abs(c - 12.111581435) < .000001
    True

    >>> p = black_scholes('p',100,90,.5,.01,.2) 
    >>> abs(p - 1.66270456231) < .000001
    True
    """   
    
    deflater = numpy.exp(-r * t)
    F = S / deflater
    return undiscounted_black(F, K, sigma, t, flag) * deflater


if __name__ == "__main__":
    from py_vollib.helpers.doctest_helper import run_doctest
    run_doctest()
