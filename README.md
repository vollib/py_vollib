# vollib

`vollib` is a python library for calculating option prices, implied volatility and greeks. At its core is Peter Jaeckel's source code for `LetsBeRational`, an extremely fast and accurate algorithm for obtaining Black's implied volatility from option prices.

Building on this solid foundation, `vollib` provides functions to calculate option prices, implied volatility and greeks using Black, Black-Scholes, and Black-Scholes-Merton. `vollib` implements both analytical and numerical greeks for each of the three pricing formulae.

## Installation

```bash
pip install vollib-test
```

## Dependencies

- `cody-special` - High-precision error functions and normal distribution
- `piecewise-rational` - Shape-preserving piecewise rational cubic interpolation
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
- [GitHub](https://github.com/vollib/vollib)

## License

MIT
