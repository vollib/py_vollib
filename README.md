# vollib

`vollib` is a python library for calculating option prices, implied volatility and greeks. At its core is Peter Jaeckel's source code for `LetsBeRational`, an extremely fast and accurate algorithm for obtaining Black's implied volatility from option prices.

Building on this solid foundation, `vollib` provides functions to calculate option prices, implied volatility and greeks using Black, Black-Scholes, and Black-Scholes-Merton. `vollib` implements both analytical and numerical greeks for each of the three pricing formulae.

## Input domain

Strike prices (`K`) must be strictly positive for the Black, Black-Scholes, and Black-Scholes-Merton pricing functions. A zero strike call has a well-defined mathematical limit, but `vollib` does not special-case that boundary; it preserves the domain and behavior of the underlying LetsBeRational implementation. If an application wants to support `K = 0`, handle that boundary before calling `vollib`.

This domain requirement applies equally to calls and puts:

| Strike input | Calls | Puts |
| --- | --- | --- |
| `K = 0` | raises `ZeroDivisionError` | raises `ZeroDivisionError` |
| `K < 0` | raises `ValueError` | raises `ValueError` |

## Installation

`vollib` 1.0.8 supports Python 3.9 through 3.12.

```bash
pip install vollib
```

## Package history

The original `vollib 0.1.x` package was the Python 2.7/C-SWIG implementation. It remains available on PyPI for pinned legacy installs, but it is deprecated.

The `py_vollib 1.0.x` package name was introduced for the pure-Python implementation with Python 3 support. Starting with `vollib 1.0.7`, the canonical package name is again `vollib`.

## Migration from py_vollib

The canonical Python package is now `vollib`. Existing `py_vollib.*` imports remain available as a compatibility namespace for this transition release, but they are deprecated. New code should import from `vollib`:

```python
from vollib.black_scholes import black_scholes
```

Existing code like this will continue to work for now:

```python
from py_vollib.black_scholes import black_scholes
```

The temporary `vollib-test` package was a bridge while the official package release path was being repaired. It is superseded by the official `vollib` package.

## Implied volatility from option price

`vollib` can calculate implied volatility from a known option price. For example, using Black-Scholes:

```python
from vollib.black_scholes import black_scholes
from vollib.black_scholes.implied_volatility import implied_volatility

flag = "c"
S = 100
K = 100
t = 0.5
r = 0.01
sigma = 0.2

price = black_scholes(flag, S, K, t, r, sigma)
iv = implied_volatility(price, S, K, t, r, flag)
```

The same pattern is available for Black and Black-Scholes-Merton through their respective `implied_volatility` modules.

## Dependencies

- `cody-special` - High-precision error functions and normal distribution
- `piecewise-rational` - Shape-preserving piecewise rational cubic interpolation
- `lets_be_rational` - Pure Python implementation of Peter Jaeckel's LetsBeRational
- `numpy`
- `pandas`
- `scipy`
- `simplejson`

## About the reference Python implementation

`vollib` contains `vollib.ref_python`, a pure python version of the functions in `vollib.*`. It is provided purely as a reference implementation for sanity checking.

## About "Let's be Rational"

["Let's Be Rational"](http://www.pjaeckel.webspace.virginmedia.com/LetsBeRational.pdf) is a paper by [Peter Jaeckel](http://jaeckel.org) showing *"how Black's volatility can be implied from option prices with as little as two iterations to maximum attainable precision on standard (64 bit floating point) hardware for all possible inputs."*

The paper is accompanied by the full C source code, which resides at [www.jaeckel.org/LetsBeRational.7z](http://www.jaeckel.org/LetsBeRational.7z).

```
Copyright (c) 2013-2014 Peter Jaeckel.

Permission to use, copy, modify, and distribute this software is freely granted,
provided that this notice is preserved.

WARRANTY DISCLAIMER
The Software is provided "as is" without warranty of any kind, either express or implied,
including without limitation any implied warranties of condition, uninterrupted use,
merchantability, fitness for a particular purpose, or non-infringement.
```

## Links

- [Let's Be Rational](http://www.pjaeckel.webspace.virginmedia.com/LetsBeRational.pdf)
- [Licence](http://vollib.org/license)
- [Vollib Home](http://vollib.org)
- [GitHub](https://github.com/vollib/py_vollib)

## License

MIT
