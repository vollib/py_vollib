# -*- coding: utf-8 -*-

"""
py_vollib.ref_python.black_scholes_merton.implied_volatility
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

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
from scipy.optimize import brentq

# Local application/library specific imports
from py_vollib.ref_python.black_scholes_merton import black_scholes_merton


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
    >>> q = .02

    >>> price = black_scholes_merton(flag, S, K, t, r, sigma, q)
    >>> implied_volatility(price, S, K, t, r, q, flag)
    0.20000000000000018

    >>> flac = 'p'
    >>> sigma = 0.3
    >>> price = black_scholes_merton(flag, S, K, t, r, sigma, q)
    >>> price
    8.138101080183894
    >>> implied_volatility(price, S, K, t, r, q, flag)
    0.30000000000000027
    """

    f = lambda sigma: price - black_scholes_merton(flag, S, K, t, r, sigma, q)

    return brentq(
        f,
        a=1e-12,
        b=100,
        xtol=1e-15,
        rtol=1e-15,
        maxiter=1000,
        full_output=False
    )


if __name__ == "__main__":
    from py_vollib.helpers.doctest_helper import run_doctest
    run_doctest()
