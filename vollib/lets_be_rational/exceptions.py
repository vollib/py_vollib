"""Compatibility exports for LetsBeRational exceptions."""

from py_lets_be_rational.exceptions import (
    AboveMaximumException,
    BelowIntrinsicException,
    VolatilityValueException,
)

PriceIsBelowIntrinsic = BelowIntrinsicException
PriceIsAboveMaximum = AboveMaximumException

__all__ = [
    "AboveMaximumException",
    "BelowIntrinsicException",
    "PriceIsAboveMaximum",
    "PriceIsBelowIntrinsic",
    "VolatilityValueException",
]
