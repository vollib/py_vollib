# -----------------------------------------------------------------------------
# IMPORTS

# Standard library imports
import unittest

# Related third party imports

# Local application/library specific imports
from py_vollib.black import black as c_black
from py_vollib.ref_python.black import black as py_black
from tests.test_utils import almost_equal


class TestPrice(unittest.TestCase):

    def test_black_put(self):
        F = 100
        K = 90
        sigma = .2
        r = .02
        t = .5
        flag = 'p'

        c_price = c_black(flag, F, K, t, r, sigma)
        py_price = py_black(flag, F, K, t, r, sigma)
        self.assertTrue(almost_equal(c_price, py_price))

    def test_black_call(self):
        F = 100
        K = 90
        sigma = .2
        r = .02
        t = .5
        flag = 'c'

        c_price = c_black(flag, F, K, t, r, sigma)
        py_price = py_black(flag, F, K, t, r, sigma)
        self.assertTrue(almost_equal(c_price, py_price))


if __name__ == '__main__':
    unittest.main()
