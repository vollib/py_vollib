# -----------------------------------------------------------------------------
# IMPORTS

# Standard library imports
import unittest

# Related third party imports

# Local application/library specific imports
from py_vollib.black_scholes import black_scholes as c_black_scholes
from py_vollib.black_scholes.implied_volatility import implied_volatility as c_implied_volatility
from py_vollib.ref_python.black_scholes import black_scholes as py_black_scholes
from py_vollib.ref_python.black_scholes.implied_volatility import implied_volatility as py_implied_volatility
from tests.test_utils import almost_equal


class TestImpliedVolatility(unittest.TestCase):

    def test_implied_volatility_put(self):
        S = 100
        K = 100
        sigma = .232323232
        t = .5
        r = .01
        flag = 'p'

        c_price = c_black_scholes(flag, S, K, t, r, sigma)
        py_price = py_black_scholes(flag, S, K, t, r, sigma)

        c_iv = c_implied_volatility(c_price, S, K, t, r, flag)
        py_iv = py_implied_volatility(py_price, S, K, t, r, flag)
        self.assertTrue(almost_equal(c_iv, py_iv))

    def test_implied_volatility_call(self):
        S = 100
        K = 100
        sigma = .232323232
        t = .5
        r = .01
        flag = 'c'

        c_price = c_black_scholes(flag, S, K, t, r, sigma)
        py_price = py_black_scholes(flag, S, K, t, r, sigma)

        c_iv = c_implied_volatility(c_price, S, K, t, r, flag)
        py_iv = py_implied_volatility(py_price, S, K, t, r, flag)
        self.assertTrue(almost_equal(c_iv, py_iv))


if __name__ == '__main__':
    unittest.main()
