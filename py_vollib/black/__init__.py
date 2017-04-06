# -*- coding: utf-8 -*-

"""
py_vollib.black
~~~~~~~~~~~~~~~

Copyright © 2017

A library for option pricing, implied volatility, and
greek calculation.  py_vollib is based on lets_be_rational,
a Python wrapper for LetsBeRational by Peter Jaeckel as
described below.

:copyright: © 2017 Gammon Capital LLC
:license: MIT, see LICENSE for more details.

About LetsBeRational:
~~~~~~~~~~~~~~~~~~~~~~~

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
from math import log, sqrt

# Related third party imports
import py_lets_be_rational as lets_be_rational
import numpy
from numpy import log, sqrt

# Local application/library specific imports
from py_vollib.helpers import binary_flag


# -----------------------------------------------------------------------------
# FUNCTIONS - OPTION PRICING

def black(flag, F, K, t, r, sigma):
    
    """Calculate the (discounted) Black option price.

    :param F: underlying futures price
    :type F: float
    :param K: strike price
    :type K: float
    :param sigma: annualized standard deviation, or volatility
    :type sigma: float
    :param t: time to expiration in years
    :type t: float  
        
    >>> F = 100
    >>> K = 100
    >>> sigma = .2
    >>> flag = 'c'
    >>> r = .02
    >>> t = .5
    >>> black(flag, F, K, t, r, sigma)
    5.5811067246048118

    """
    
    deflater = numpy.exp(-r * t)
    return undiscounted_black(F, K, sigma, t, flag) * deflater

# -----------------------------------------------------------------------------
# FUNCTIONS - FOR REFERENCE AND TESTING

def undiscounted_black(F, K, sigma, t, flag):

    """Calculate the **undiscounted** Black option price.

    :param F: underlying futures price
    :type F: float
    :param K: strike price
    :type K: float
    :param sigma: annualized standard deviation, or volatility
    :type sigma: float
    :param t: time to expiration in years
    :type t: float   

    >>> F = 100
    >>> K = 100
    >>> sigma = .2
    >>> flag = 'c'
    >>> t = .5
    >>> undiscounted_black(F, K, sigma, t, flag)
    5.637197779701664
    
    """

    q = binary_flag[flag]
    F = float(F)
    K = float(K)
    sigma = float(sigma)
    t = float(t)
    
    return lets_be_rational.black(F, K, sigma, t, q)


def normalised_black(x, s, flag):

    """Calculate the normalised Black value,
    a "time value put-call invariant" transformation
    of the Black pricing formula.  In other words, 
    the amount of time value, or "extrinsic" value 
    of a put and call at the same log-moneyness will
    be always be identical.

    :param x: ln(F/K) where K is the strike price, and F is the futures price
    :type x: float
    :param s: volatility times the square root of time to expiration
    :type s: float
    :param flag: 'p' or 'c' for put or call 
    :type flag: str   
    
    
    >>> def normalised_intrinsic(F, K, flag): 
    ...     if flag=='c':
    ...         return max(F-K,0)/(F*K)**0.5
    ...     else:
    ...         return max(K-F,0)/(F*K)**0.5    
    
    >>> F = 100.
    >>> K = 95.
    >>> x = log(F/K)
    >>> t = 0.5
    >>> v = 0.3
    >>> s = v * sqrt(t)    
    
    >>> normalised_black(x,s,'p')
    0.061296663817558904
    
    >>> normalised_black(x,s,'c')
    0.11259558142181655
    
    '''
    Here the put is OTM, so has only time value.
    The call is ITM, having both intrinsic and time value.
    Since the time value must be equal for both, 
    the call normalised price minus its normalised 
    intrinsic must equal the put normalised price.
    
    
    >>> (normalised_black(x,s,'p') - (
    ... normalised_black(x,s,'c') - normalised_intrinsic(F,K,'c')))<1e-12 
    True
    
    
    """
    
    q = binary_flag[flag]
    
    return lets_be_rational.normalised_black(x, s, q)


if __name__ == "__main__":
    from py_vollib.helpers.doctest_helper import run_doctest
    run_doctest()


