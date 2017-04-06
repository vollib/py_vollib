# -*- coding: utf-8 -*-

"""
py_vollib.black_scholes_merton
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

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

# Related third party imports
import numpy

# Local application/library specific imports
from py_lets_be_rational import black
from py_vollib.helpers import binary_flag


# -----------------------------------------------------------------------------
# FUNCTIONS

def black_scholes_merton(flag, S, K, t, r, sigma, q):
    """Return the Black-Scholes-Merton option price.

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
    :param q: annualized continuous dividend rate
    :type q: float 

    From Espen Haug, The Complete Guide To Option Pricing Formulas
    Page 4

    >>> S=100
    >>> K=95
    >>> q=.05
    >>> t = 0.5
    >>> r = 0.1
    >>> sigma = 0.2

    >>> p_published_value = 2.4648
    >>> p_calc = black_scholes_merton('p', S, K, t, r, sigma, q)
    >>> abs(p_published_value - p_calc) < 0.0001
    True
    """
    
    F = S * numpy.exp((r-q)*t)
    deflater = numpy.exp(-r * t)
    return black(F, K, sigma, t, binary_flag[flag]) * deflater


if __name__ == "__main__":
    from py_vollib.helpers.doctest_helper import run_doctest
    run_doctest()
