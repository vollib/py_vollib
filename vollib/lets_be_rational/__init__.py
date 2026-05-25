"""Compatibility exports for LetsBeRational functionality.

The implementation lives in the external ``lets_be_rational`` package.
This module preserves the historical ``vollib.lets_be_rational`` namespace.
"""

from lets_be_rational import (
    black,
    implied_volatility_from_a_transformed_rational_guess,
    implied_volatility_from_a_transformed_rational_guess_with_limited_iterations,
    norm_cdf,
    normalised_black,
    normalised_black_call,
    normalised_implied_volatility_from_a_transformed_rational_guess,
    normalised_implied_volatility_from_a_transformed_rational_guess_with_limited_iterations,
    normalised_vega,
)
from lets_be_rational.exceptions import AboveMaximumException, BelowIntrinsicException

PriceIsBelowIntrinsic = BelowIntrinsicException
PriceIsAboveMaximum = AboveMaximumException

__all__ = [
    "AboveMaximumException",
    "BelowIntrinsicException",
    "PriceIsAboveMaximum",
    "PriceIsBelowIntrinsic",
    "black",
    "implied_volatility_from_a_transformed_rational_guess",
    "implied_volatility_from_a_transformed_rational_guess_with_limited_iterations",
    "norm_cdf",
    "normalised_black",
    "normalised_black_call",
    "normalised_implied_volatility_from_a_transformed_rational_guess",
    "normalised_implied_volatility_from_a_transformed_rational_guess_with_limited_iterations",
    "normalised_vega",
]
