# -*- coding: utf-8 -*-

"""
vollib.lets_be_rational.exceptions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Exception classes for implied volatility calculations.

Based on Peter Jaeckel's LetsBeRational.
"""

from vollib.lets_be_rational.constants import (
    VOLATILITY_VALUE_TO_SIGNAL_PRICE_IS_BELOW_INTRINSIC,
    VOLATILITY_VALUE_TO_SIGNAL_PRICE_IS_ABOVE_MAXIMUM,
)


class VolatilityValueException(Exception):
    def __init__(self, message="Volatility value out of range.", value=None):
        Exception.__init__(self, message)
        self.value = value


class BelowIntrinsicException(VolatilityValueException):
    def __init__(self):
        VolatilityValueException.__init__(
            self,
            "The volatility is below the intrinsic value.",
            VOLATILITY_VALUE_TO_SIGNAL_PRICE_IS_BELOW_INTRINSIC
        )


class AboveMaximumException(VolatilityValueException):
    def __init__(self):
        VolatilityValueException.__init__(
            self,
            "The volatility is above the maximum value.",
            VOLATILITY_VALUE_TO_SIGNAL_PRICE_IS_ABOVE_MAXIMUM
        )


# Aliases for backward compatibility
PriceIsBelowIntrinsic = BelowIntrinsicException
PriceIsAboveMaximum = AboveMaximumException
