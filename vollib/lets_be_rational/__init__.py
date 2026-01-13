"""
Internal lets_be_rational module for vollib.

Based on Peter Jäckel's LetsBeRational algorithm.
"""
from vollib.lets_be_rational.core import (
    implied_volatility_from_a_transformed_rational_guess,
    implied_volatility_from_a_transformed_rational_guess_with_limited_iterations,
    normalised_implied_volatility_from_a_transformed_rational_guess,
    normalised_implied_volatility_from_a_transformed_rational_guess_with_limited_iterations,
    normalised_black,
    normalised_black_call,
    black,
    normalised_vega,
)
from vollib.lets_be_rational.exceptions import (
    BelowIntrinsicException,
    AboveMaximumException,
    PriceIsBelowIntrinsic,
    PriceIsAboveMaximum,
)
from cody_special import norm_cdf
