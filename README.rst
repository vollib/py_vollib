About ``py_vollib``
===================

``py_vollib`` is a python library for calculating option prices,
implied volatility and greeks. At its core is Peter Jäckel's 
source code for ``LetsBeRational``, an extremely fast and accurate algorithm
for obtaining Black's implied volatility from option prices.

Building on this solid foundation, ``py_vollib`` provides functions
to calculate option prices, implied volatility and greeks using 
Black, Black-Scholes, and Black-Scholes-Merton. ``py_vollib``
implements both analytical and numerical greeks for each of the three pricing formulae.

About the initial release
-------------------------

This is the initial release of ``py_vollib``.

About the reference implementation
----------------------------------

**py_vollib.ref_python is a pure python version of py_vollib without any dependence on LetsBeRational. It is provided purely as a reference implementation for sanity checking. It is not recommended for industrial use.**


Dependencies
------------

``py_vollib`` is Python 2.7/Python 3.6 compatible. It depends on the ``py_lets_be_rational`` package, pure python implementation of Peter Jäckel's original C source code.

To install via pip, type the following::

    >>> pip install py_vollib

Installing ``py_vollib`` via pip will automatically install the necessary dependencies,
except for pip, and Python.

Python, and pip must be installed prior to installing ``py_vollib``.


``py_lets_be_rational`` is quite stable compared to ``py_vollib``, which is likely to be updated frequently.

Troubleshooting
---------------

Problem: ``OSError: dlopen(libllvmlite.dylib, 6): image not found``
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

This is a MacOS specific error. Take a look at ``py_vollib``'s dependency graph from this point of view:

::

    py_vollib
        |_ py_lets_be_rational
            |_ numba
                |_ llvmlite
                    |_ LLVM


- ``numba`` version 0.31.0 (current version) doesn't specify ``llvmlite`` version in its dependencies.
- ``llvmlite`` 0.17.0 (current version) depends on LLVM 4.0.
- You can install LLVM version 4.0 using the ``brew install llvm`` command.
- You can install ``llvmlite`` version 0.17.0 using the
  ``LLVM_CONFIG=/usr/local/opt/llvm/bin/llvm-config pip install -U llvmlite`` command.
- Installing ``llvmlite`` version 0.17.0 seems to be not working:
  ``OSError: dlopen(libllvmlite.dylib, 6): image not found``
- ``llvmlite`` 0.16.0 depends on LLVM 3.9.
- You can install LLVM version 3.9 using the ``brew install llvm@3.9`` command.
- You can install ``llvmlite`` version 0.16.0 using the
  ``LLVM_CONFIG=/usr/local/opt/llvm@3.9/bin/llvm-config pip install -U llvmlite==0.16.0`` command.

Solution
++++++++

::

    brew install llvm@3.9
    LLVM_CONFIG=/usr/local/opt/llvm@3.9/bin/llvm-config pip install -U llvmlite==0.16.0
    pip install py_vollib


About "Let's be Rational":
--------------------------

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

Links:
------

  * `Let's Be Rational <http://www.pjaeckel.webspace.virginmedia.com/LetsBeRational.pdf>`_
  * `pip <https://pypi.python.org/pypi/pip>`_
  * `Licence <http://vollib.org/license>`_
  * `Vollib Home <http://vollib.org>`_

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

