# -*- coding: utf-8 -*-

"""
py_vollib.ref_python.black_scholes_merton
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

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
from scipy.stats import norm

# Local application/library specific imports


N = norm.cdf


# -----------------------------------------------------------------------------
# FUNCTIONS, FOR REFERENCE AND TESTING

def d1(S, K, t, r, sigma, q):
    """Calculate the d1 component of the Black-Scholes-Merton PDE.

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

    >>> d1_published_value = 0.6102
    >>> d1_calc = d1(S,K,t,r,sigma,q)
    >>> abs(d1_published_value - d1_calc) < 0.0001
    True
    """

    numerator = numpy.log(S / float(K)) + ((r - q) + sigma * sigma / 2.0) * t
    denominator = sigma * numpy.sqrt(t)
    return numerator / denominator


def d2(S, K, t, r, sigma, q):
    """Calculate the d2 component of the Black-Scholes-Merton PDE.

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

    >>> d2_published_value = 0.4688
    >>> d2_calc = d2(S,K,t,r,sigma,q)
    >>> abs(d2_published_value - d2_calc) < 0.0001
    True
    """

    return d1(S, K, t, r, sigma, q) - sigma * numpy.sqrt(t)


def bsm_call(S, K, t, r, sigma, q):
    """Return the Black-Scholes-Merton call price
    implemented in python (for reference).

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
    """

    D1 = d1(S, K, t, r, sigma, q)
    D2 = d2(S, K, t, r, sigma, q)

    return S * numpy.exp(-q * t) * N(D1) - K * numpy.exp(-r * t) * N(D2)


def bsm_put(S, K, t, r, sigma, q):
    """Return the Black-Scholes-Merton put price
    implemented in python (for reference).

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
    >>> p_calc = bsm_put(S, K, t, r, sigma, q)
    >>> abs(p_published_value - p_calc) < 0.0001
    True
    """

    D1 = d1(S, K, t, r, sigma, q)
    D2 = d2(S, K, t, r, sigma, q)
    return K * numpy.exp(-r * t) * N(-D2) - S * numpy.exp(-q * t) * N(-D1)


def black_scholes_merton(flag, S, K, t, r, sigma, q):
    """Return the Black-Scholes-Merton call price implemented in
    python (for reference).

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

    if flag == 'c':
        return bsm_call(S, K, t, r, sigma, q)
    else:
        return bsm_put(S, K, t, r, sigma, q)


if __name__ == "__main__":
    from py_vollib.helpers.doctest_helper import run_doctest
    run_doctest()
