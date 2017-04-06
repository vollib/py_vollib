# -*- coding: utf-8 -*-

"""
py_vollib.black.implied_volatility
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

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
import py_lets_be_rational as lets_be_rational
import numpy

# Local application/library specific imports
from py_vollib.black import black
from py_vollib.black import undiscounted_black
from py_vollib.black import normalised_black
from py_vollib.helpers import binary_flag
from py_vollib.helpers.exceptions import PriceIsAboveMaximum, PriceIsBelowIntrinsic
from py_vollib.helpers.constants import MINUS_FLOAT_MAX, FLOAT_MAX


# -----------------------------------------------------------------------------
# FUNCTIONS - IMPLIED VOLATILITY

def implied_volatility_of_discounted_option_price(discounted_option_price, F, K, r, t, flag):
    """Calculate the implied volatility of the Black option price

    :param discounted_option_price: discounted Black price of a futures option
    :type discounted_option_price: float
    :param F: underlying futures price
    :type F: float
    :param K: strike price
    :type K: float
    :param r: the risk-free interest rate
    :type r: float 
    :param t: time to expiration in years
    :type t: float
    :param flag: 'p' or 'c' for put or call
    :type flag: str

    >>> F = 100
    >>> K = 100
    >>> sigma = .2
    >>> flag = 'c'
    >>> t = .5
    >>> r = .02

    >>> discounted_call_price = black(flag, F, K, t, r, sigma)
    >>> iv = implied_volatility_of_discounted_option_price(
    ... discounted_call_price, F, K, r, t, flag)

    >>> expected_price = 5.5811067246
    >>> expected_iv = 0.2
    
    >>> abs(expected_price - discounted_call_price) < 0.00001
    True
    >>> abs(expected_iv - iv) < 0.00001
    True
    """
    
    deflater = numpy.exp(-r * t)
    undiscounted_option_price = discounted_option_price / deflater
    sigma_calc = lets_be_rational.implied_volatility_from_a_transformed_rational_guess(
        undiscounted_option_price,
        F,
        K,
        t,
        binary_flag[flag]
    )
    if sigma_calc == FLOAT_MAX:
        raise PriceIsAboveMaximum()
    elif sigma_calc == MINUS_FLOAT_MAX:
        raise PriceIsBelowIntrinsic() 
    return sigma_calc


implied_volatility = implied_volatility_of_discounted_option_price


# -----------------------------------------------------------------------------
# FUNCTIONS - IMPLIED VOLATILITY, FOR TEST & REFERENCE

def normalised_implied_volatility(beta, x, flag):
    """Calculate the normalised Black implied volatility,
    a time invariant transformation
    of Black implied volatility.

    Keyword arguments:
    
    :param x: ln(F/K) where K is the strike price, and F is the futures price
    :type x: float
    :param beta: the normalized Black price
    :type beta: float
    :param flag: 'p' or 'c' for put or call 
    :type flag: str
    
    >>> beta_call = normalised_black(0.0, 0.2, 'c')
    >>> beta_put = normalised_black(0.1,0.23232323888,'p')
    >>> normalized_b76_iv_call = normalised_implied_volatility(beta_call, 0.0, 'c')
    >>> normalized_b76_iv_put = normalised_implied_volatility(beta_put, 0.1, 'p')
    
    >>> expected_price = 0.0796556745541
    >>> expected_iv = 0.2
    
    >>> abs(expected_price - beta_call) < 0.00001
    True
    >>> abs(expected_iv - normalized_b76_iv_call) < 0.00001
    True
    
    >>> expected_price = 0.0509710222785
    >>> expected_iv = 0.23232323888
    
    >>> abs(expected_price - beta_put) < 0.00001
    True
    >>> abs(expected_iv - normalized_b76_iv_put) < 0.00001
    True
    """    

    q = binary_flag[flag]
    return lets_be_rational.normalised_implied_volatility_from_a_transformed_rational_guess(
        beta, x, q)


def normalised_implied_volatility_limited_iterations(beta, x, flag, N):
    """Calculate the normalised Black implied volatility,
    with limited iterations.

    :param x: ln(F/K) where K is the strike price, and F is the futures price
    :type x: float
    :param beta: the normalized Black price
    :type beta: float
    :param flag: 'p' or 'c' for put or call 
    :type flag: str  

    >>> beta_call = normalised_black(0.0, 0.2, 'c')
    >>> beta_put = normalised_black(0.1,0.23232323888,'p')
    >>> normalized_b76_iv_call = normalised_implied_volatility_limited_iterations(beta_call, 0.0, 'c',1)
    >>> normalized_b76_iv_put = normalised_implied_volatility_limited_iterations(beta_put, 0.1, 'p',1)
    
    >>> expected_price = 0.0796556745541
    >>> expected_iv = 0.2
    
    >>> abs(expected_price - beta_call) < 0.00001
    True
    >>> abs(expected_iv - normalized_b76_iv_call) < 0.00001
    True
    
    >>> expected_price = 0.0509710222785
    >>> expected_iv = 0.23232323888
    
    >>> abs(expected_price - beta_put) < 0.00001
    True
    >>> abs(expected_iv - normalized_b76_iv_put) < 0.00001
    True
    """    

    q = binary_flag[flag]
    return lets_be_rational.normalised_implied_volatility_from_a_transformed_rational_guess_with_limited_iterations(
        beta, x, q, N)


def implied_volatility_of_undiscounted_option_price(
        undiscounted_option_price,
        F,
        K,
        t,
        flag
    ):
    """Calculate the implied volatility of the undiscounted Black option price

    :param undiscounted_option_price: undiscounted Black price of a futures option
    :type undiscounted_option_price: float
    :param F: underlying futures price
    :type F: float
    :param K: strike price
    :type K: float
    :param t: time to expiration in years
    :type t: float  

    >>> F = 100
    >>> K = 100
    >>> sigma = .2
    >>> flag = 'c'
    >>> t = .5

    >>> undiscounted_call_price = undiscounted_black(F, K, sigma, t, flag)
    >>> iv = implied_volatility_of_undiscounted_option_price(
    ... undiscounted_call_price, F, K, t, flag)

    >>> expected_price = 5.6371977797
    >>> expected_iv = 0.2
    
    >>> abs(expected_price - undiscounted_call_price) < 0.00001
    True
    >>> abs(expected_iv - iv) < 0.00001
    True
    """

    return lets_be_rational.implied_volatility_from_a_transformed_rational_guess(
        undiscounted_option_price, 
        F,
        K, 
        t, 
        binary_flag[flag]
    )


def implied_volatility_of_undiscounted_option_price_limited_iterations(
    undiscounted_option_price, F, K, t, flag, N):
    """Calculate implied volatility of the undiscounted Black 
    option price with limited iterations.

    :param undiscounted_option_price: undiscounted Black price of a futures option
    :type undiscounted_option_price: float
    :param F: underlying futures price
    :type F: float
    :param K: strike price
    :type K: float
    :param t: time to expiration in years
    :type t: float 

    >>> F = 100
    >>> K = 100
    >>> sigma = .232323232
    >>> flag = 'c'
    >>> t = .5

    >>> price = undiscounted_black(F, K, sigma, t, flag)
    >>> iv = implied_volatility_of_undiscounted_option_price_limited_iterations(
    ... price, F, K, t, flag, 1)

    >>> expected_price = 6.54635543387
    >>> expected_iv = 0.232323232
    
    >>> abs(expected_price - price) < 0.00001
    True
    >>> abs(expected_iv - iv) < 0.00001
    True
    """  

    return lets_be_rational.implied_volatility_from_a_transformed_rational_guess_with_limited_iterations(
        undiscounted_option_price, 
        F,
        K, 
        t, 
        binary_flag[flag],
        N
    )


if __name__ == "__main__":
    from py_vollib.helpers.doctest_helper import run_doctest
    run_doctest()
