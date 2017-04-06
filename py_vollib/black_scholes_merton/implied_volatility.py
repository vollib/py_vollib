# -*- coding: utf-8 -*-

"""
py_vollib.black_scholes_merton.implied_volatility
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Copyright © 2017 Gammon Capital LLC

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
from py_lets_be_rational import implied_volatility_from_a_transformed_rational_guess as iv
import numpy

# Local application/library specific imports
from py_vollib.black_scholes_merton import black_scholes_merton
from py_vollib.helpers import binary_flag
from py_vollib.helpers.exceptions import PriceIsAboveMaximum, PriceIsBelowIntrinsic
from py_vollib.helpers.constants import MINUS_FLOAT_MAX, FLOAT_MAX


# -----------------------------------------------------------------------------
# FUNCTIONS

def implied_volatility(price, S, K, t, r, q, flag):
    """Calculate the Black-Scholes-Merton implied volatility.

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
    :param flag: 'c' or 'p' for call or put.
    :type flag: str

    >>> S = 100
    >>> K = 100
    >>> sigma = .2
    >>> r = .01
    >>> flag = 'c'
    >>> t = .5
    >>> q = 0
    
    >>> price = black_scholes_merton(flag, S, K, t, r, sigma, q)
    >>> iv = implied_volatility(price, S, K, t, r, q, flag)

    >>> expected_price = 5.87602423383
    >>> expected_iv = 0.2
    
    >>> abs(expected_price - price) < 0.00001
    True
    >>> abs(expected_iv - iv) < 0.00001
    True
    """

    deflater = numpy.exp(-r * t)
    
    undiscounted_option_price = price / deflater
    
    F = S * numpy.exp((r-q)*t)
    
    sigma_calc = iv(undiscounted_option_price, F, K, t, binary_flag[flag])

    if sigma_calc == FLOAT_MAX:
        
        raise PriceIsAboveMaximum()
    
    elif sigma_calc == MINUS_FLOAT_MAX:
        
        raise PriceIsBelowIntrinsic() 
    
    return sigma_calc


if __name__ == "__main__":
    from py_vollib.helpers.doctest_helper import run_doctest
    run_doctest()
