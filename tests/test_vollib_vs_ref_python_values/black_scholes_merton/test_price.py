# -----------------------------------------------------------------------------
# IMPORTS

# Standard library imports
import unittest

# Related third party imports

# Local application/library specific imports
from py_vollib.black_scholes_merton import black_scholes_merton as c_black_scholes_merton
from py_vollib.ref_python.black_scholes_merton import black_scholes_merton as py_black_scholes_merton
from tests.test_utils import almost_equal


class TestPrice(unittest.TestCase):

    def test_black_put(self):
        S = 100
        K = 95
        r = .01
        q = .05
        t = .5
        sigma = .2
        flag = 'p'

        c_price = c_black_scholes_merton(flag, S, K, t, r, sigma, q)
        py_price = py_black_scholes_merton(flag, S, K, t, r, sigma, q)
        self.assertTrue(almost_equal(c_price, py_price))

    def test_black_call(self):
        S = 100
        K = 95
        r = .01
        q = .05
        t = .5
        sigma = .2
        flag = 'c'

        c_price = c_black_scholes_merton(flag, S, K, t, r, sigma, q)
        py_price = py_black_scholes_merton(flag, S, K, t, r, sigma, q)
        self.assertTrue(almost_equal(c_price, py_price))


if __name__ == '__main__':
    unittest.main()
