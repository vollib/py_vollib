# -----------------------------------------------------------------------------
# IMPORTS

# Standard library imports
import unittest

# Related third party imports

# Local application/library specific imports
from py_vollib.black_scholes import black_scholes as c_black_scholes
from py_vollib.ref_python.black_scholes import black_scholes as py_black_scholes
from tests.test_utils import almost_equal


class TestPrice(unittest.TestCase):

    def test_black_scholes_put(self):
        S = 100
        K = 90
        r = .01
        t = .5
        sigma = .2
        flag = 'p'

        c_price = c_black_scholes(flag, S, K, t, r, sigma)
        py_price = py_black_scholes(flag, S, K, t, r, sigma)
        self.assertTrue(almost_equal(c_price, py_price))

    def test_black_scholes_call(self):
        S = 100
        K = 90
        r = .01
        t = .5
        sigma = .2
        flag = 'c'

        c_price = c_black_scholes(flag, S, K, t, r, sigma)
        py_price = py_black_scholes(flag, S, K, t, r, sigma)
        self.assertTrue(almost_equal(c_price, py_price))


if __name__ == '__main__':
    unittest.main()
