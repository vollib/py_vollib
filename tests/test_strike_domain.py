import pytest

from vollib.black import black
from vollib.black_scholes import black_scholes
from vollib.black_scholes_merton import black_scholes_merton


@pytest.mark.parametrize(
    ("pricing_function", "args"),
    [
        (black, ("c", 200, 0, 1, 0.02, 1.3)),
        (black, ("p", 200, 0, 1, 0.02, 1.3)),
        (black_scholes, ("c", 200, 0, 1, 0.02, 1.3)),
        (black_scholes, ("p", 200, 0, 1, 0.02, 1.3)),
        (black_scholes_merton, ("c", 200, 0, 1, 0.02, 1.3, 0.01)),
        (black_scholes_merton, ("p", 200, 0, 1, 0.02, 1.3, 0.01)),
    ],
)
def test_zero_strike_raises_consistently(pricing_function, args):
    with pytest.raises(ZeroDivisionError):
        pricing_function(*args)


@pytest.mark.parametrize(
    ("pricing_function", "args"),
    [
        (black, ("c", 200, -1, 1, 0.02, 1.3)),
        (black_scholes, ("c", 200, -1, 1, 0.02, 1.3)),
        (black_scholes_merton, ("c", 200, -1, 1, 0.02, 1.3, 0.01)),
    ],
)
def test_negative_strike_is_outside_supported_domain(pricing_function, args):
    with pytest.raises(ValueError):
        pricing_function(*args)
