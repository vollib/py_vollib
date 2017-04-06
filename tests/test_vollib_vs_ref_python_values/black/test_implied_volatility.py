# -----------------------------------------------------------------------------
# IMPORTS

# Standard library imports
import unittest

# Related third party imports

# Local application/library specific imports
from py_vollib.black import black as c_black
from py_vollib.black.implied_volatility import implied_volatility_of_discounted_option_price as c_implied_volatility
from py_vollib.ref_python.black import black as py_black
from py_vollib.ref_python.black.implied_volatility import implied_volatility as py_implied_volatility
from tests.test_utils import almost_equal


class TestImpliedVolatility(unittest.TestCase):

    def test_implied_volatility_put(self):
        F = 100
        K = 100
        sigma = .2
        t = .5
        r = .02
        flag = 'p'

        c_price = c_black(flag, F, K, t, r, sigma)
        py_price = py_black(flag, F, K, t, r, sigma)

        c_iv = c_implied_volatility(c_price, F, K, t, r, flag)
        py_iv = py_implied_volatility(py_price, F, K, t, r, flag)
        self.assertTrue(almost_equal(c_iv, py_iv))

    def test_implied_volatility_call(self):
        F = 100
        K = 100
        sigma = .2
        t = .5
        r = .02
        flag = 'c'

        c_price = c_black(flag, F, K, t, r, sigma)
        py_price = py_black(flag, F, K, t, r, sigma)

        c_iv = c_implied_volatility(c_price, F, K, t, r, flag)
        py_iv = py_implied_volatility(py_price, F, K, t, r, flag)
        self.assertTrue(almost_equal(c_iv, py_iv))


if __name__ == '__main__':
    unittest.main()
