# -*- coding: utf-8 -*-

"""
py_vollib.ref_python.black.implied_volatility
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A library for option pricing, implied volatility, and
greek calculation.  py_vollib is based on lets_be_rational,
a Python wrapper for LetsBeRational by Peter Jaeckel as
described below.

:copyright: © 2017 Gammon Capital LLC
:license: MIT, see LICENSE for more details.

py_vollib.ref_python is a pure python version of py_vollib without any dependence on LetsBeRational. It is provided purely as a reference implementation for sanity checking. It is not recommended for industrial use.
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

"""


# -----------------------------------------------------------------------------
# IMPORTS

# Standard library imports

# Related third party imports
from scipy.optimize import brentq

# Local application/library specific imports
from py_vollib.ref_python.black import black


# -----------------------------------------------------------------------------
# FUNCTIONS - IMPLIED VOLATILITY

def implied_volatility(price, F, K, r, t, flag):
    """Returns the Black delta of an option.

    :param price:
    :type price: float
    :param F: underlying futures price
    :type F: float
    :param K: strike price
    :type K: float
    :param r: annual risk-free interest rate
    :type r: float
    :param t: time to expiration in years
    :type t: float
    :param flag: 'c' or 'p' for call or put.
    :type flag: str

    :returns:  float

    >>> F = 101.0
    >>> K = 102.0
    >>> t = .5
    >>> r = .01
    >>> flag = 'p'
    >>> sigma_in = 0.2

    >>> price = black(flag, F, K, t, r, sigma_in)
    >>> expected_price = 6.20451158097
    >>> abs(expected_price - price) < 0.00001
    True

    >>> sigma_out = implied_volatility(price, F, K, r, t, flag)
    >>> sigma_in == sigma_out or abs(sigma_in - sigma_out) < 0.00001
    True

    >>> F = 100
    >>> K = 100
    >>> sigma = .2
    >>> flag = 'c'
    >>> t = .5
    >>> r = .02

    >>> discounted_call_price = black(flag, F, K, t, r, sigma)
    >>> iv = implied_volatility(discounted_call_price, F, K, r, t, flag)

    >>> expected_discounted_call_price = 5.5811067246
    >>> expected_iv = 0.2
    >>> abs(expected_discounted_call_price - discounted_call_price) < 0.00001
    True
    >>> abs(expected_iv - iv) < 0.00001
    True
    """

    f = lambda sigma: price - black(flag, F, K, t, r, sigma)

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
