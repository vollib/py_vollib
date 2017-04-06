# -*- coding: utf-8 -*-

"""
py_vollib.black_scholes.implied_volatility
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

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
from py_lets_be_rational import implied_volatility_from_a_transformed_rational_guess as iv
import numpy

# Local application/library specific imports
from py_vollib.black_scholes import black_scholes
from py_vollib.helpers import binary_flag
from py_vollib.helpers import forward_price
from py_vollib.helpers.constants import FLOAT_MAX, MINUS_FLOAT_MAX
from py_vollib.helpers.exceptions import PriceIsAboveMaximum, PriceIsBelowIntrinsic


# -----------------------------------------------------------------------------
# FUNCTIONS

def implied_volatility(price, S, K, t, r, flag):
    """Calculate the Black-Scholes implied volatility.

    :param price: the Black-Scholes option price
    :type price: float
    :param S: underlying asset price
    :type S: float
    :param K: strike price
    :type K: float
    :param t: time to expiration in years
    :type t: float
    :param r: risk-free interest rate
    :type r: float
    :param flag: 'c' or 'p' for call or put.
    :type flag: str 
    
    >>> S = 100
    >>> K = 100
    >>> sigma = .2
    >>> r = .01
    >>> flag = 'c'
    >>> t = .5

    >>> price = black_scholes(flag, S, K, t, r, sigma)
    >>> iv = implied_volatility(price, S, K, t, r, flag)

    >>> expected_price = 5.87602423383
    >>> expected_iv = 0.2
    
    >>> abs(expected_price - price) < 0.00001
    True
    >>> abs(expected_iv - iv) < 0.00001
    True
    """
    deflater = numpy.exp(-r * t)
    undiscounted_option_price = price / deflater
    F = forward_price(S, t, r)
    sigma_calc = iv(undiscounted_option_price, F, K, t, binary_flag[flag])
    if sigma_calc == FLOAT_MAX:
        raise PriceIsAboveMaximum()
    elif sigma_calc == MINUS_FLOAT_MAX:
        raise PriceIsBelowIntrinsic()
    return sigma_calc


if __name__ == "__main__":
    from py_vollib.helpers.doctest_helper import run_doctest
    run_doctest()
