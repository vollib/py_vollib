About ``py_vollib``
===================

``py_vollib`` is a python library for calculating option prices, implied volatility and greeks.  At its core is
Peter Jäckel's source code for ``LetsBeRational``, an extremely fast and accurate algorithm for obtaining Black's
implied volatility from option prices.

Building on this solid foundation, ``py_vollib`` provides functions to calculate option prices, implied volatility and
greeks using Black, Black-Scholes, and Black-Scholes-Merton. ``py_vollib`` implements both analytical and numerical
greeks for each of the three pricing formulae.

Comparison with `vollib`
------------------------

+-------------------------------------------------+-------------------------+----------------------------+
| Feature                                         |      ``py_vollib``      |        ``vollib``          |
+=================================================+=========================+============================+
| Python Version Compatibility                    |       2.7 and 3.x       |          2.7 only          |
+-------------------------------------------------+-------------------------+----------------------------+
| Source Language                                 |          Python         | C with Python SWIG Wrapper |
+-------------------------------------------------+-------------------------+----------------------------+
| Optional Dependencies                           |          Numba          |            None            |
+-------------------------------------------------+-------------------------+----------------------------+
| Core Dependency (automatically installed by pip)| ``py_lets_be_rational`` |   ``lets_be_rational``     |
+-------------------------------------------------+-------------------------+----------------------------+

Execution Speed
---------------
Except for the source languages of ``py_lets_be_rational`` and ``lets_be_rational``, ``py_vollib``  and ``vollib``  are
almost identical. Each is orders of magnitude faster than traditional implied volatility calculation libraries, thanks
to the algorithms developed by Peter Jäckel.  However, ``py_vollib``, without Numba installed, is about an order of
magnitude slower than ``vollib``.  Numba helps to mitigate this speed gap considerably.

Numba Dependency
----------------

Numba is an optional dependency of ``py_vollib`` .  Because Numba installation can be tricky and OS-dependent, we
decided to leave it up to each user to decide how and whether to install Numba.  If Numba is present, execution speed
will be faster. If not, the code will still run -- just slower.

Installing Numba
----------------

``py_lets_be_rational`` optionally depends on ``numba`` which in turn depends on ``llvm-lite``. ``llvm-lite`` wants LLVM 3.9
being installed. On Mac OSX, use the latest version of HomeBrew to install ``numba``'s dependencies as shown below::

    brew install llvm@3.9
    LLVM_CONFIG=/usr/local/opt/llvm@3.9/bin/llvm-config pip install llvmlite==0.16.0
    pip install numba==0.31.0

For other operating systems, please refer to the ``llvm-lite`` and ``numba`` documentation.

About the reference Python implementation
-----------------------------------------

``py_vollib`` contains ``py_vollib.ref_python``, a pure python version of the functions in ``py_vollib.*``, except
without any dependency on ``lets_be_rational`` or ``py_lets_be_rational``.  It is provided purely as a reference
implementation for sanity checking. It is not recommended for serious use.


Dependencies
------------

``py_vollib`` is Python 2.7/Python 3.6 compatible.  Its core dependency is ``py_lets_be_rational`` package, pure
python implementation of Peter Jäckel's original C source code.

To install via pip, type the following::

    pip install py_vollib

Installing ``py_vollib`` via pip will automatically install the necessary dependencies,
except for pip, and Python.

Python, and pip must be installed prior to installing ``py_vollib``.


About "Let's be Rational"
-------------------------

`"Let's Be Rational" <http://www.pjaeckel.webspace.virginmedia.com/LetsBeRational.pdf>`_ is a paper by `Peter Jäckel <http://jaeckel.org>`_ showing *"how Black's volatility can be implied from option prices with as little as two iterations to maximum attainable precision on standard (64 bit floating point) hardware for all possible inputs."*

The paper is accompanied by the full C source code, which resides at `www.jaeckel.org/LetsBeRational.7z <www.jaeckel.org/LetsBeRational.7z>`_.

::

    Copyright © 2013-2014 Peter Jäckel.

    Permission to use, copy, modify, and distribute this software is freely granted,
    provided that this notice is preserved.

    WARRANTY DISCLAIMER
    The Software is provided "as is" without warranty of any kind, either express or implied,
    including without limitation any implied warranties of condition, uninterrupted use,
    merchantability, fitness for a particular purpose, or non-infringement.

Links
-----

  * `Let's Be Rational <http://www.pjaeckel.webspace.virginmedia.com/LetsBeRational.pdf>`_
  * `pip <https://pypi.python.org/pypi/pip>`_
  * `Licence <http://vollib.org/license>`_
  * `Vollib Home <http://vollib.org>`_
  * `py_lets_be_rational <http://github.com/vollib/py_lets_be_rational>`_
  * `lets_be_rational <http://github.com/vollib/lets_be_rational>`_
  * `vollib <http://github.com/vollib/vollib>`_

Development
-----------

Fork the GitHub repository. This will make it available under your username e.g. ``https://github.com/YOUR-USERNAME/py_vollib``.
Clone that repo on your computer, change the code as you wish. Commit and push it, and create a pull request. That's all.

Generate documentation
++++++++++++++++++++++

::

    cd docs
    sphinx-apidoc -f -o apidoc ../py_vollib
    make html

