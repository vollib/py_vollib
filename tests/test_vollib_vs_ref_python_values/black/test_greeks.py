# -----------------------------------------------------------------------------
# IMPORTS

# Standard library imports
import unittest

# Related third party imports

# Local application/library specific imports
from py_vollib.black.greeks import analytical as c_analytical
from py_vollib.black.greeks import numerical as c_numerical
from py_vollib.ref_python.black.greeks import analytical as py_analytical
from py_vollib.ref_python.black.greeks import numerical as py_numerical
from tests.test_utils import almost_equal


class TestGreeks(unittest.TestCase):

    def test_analytical_delta(self):
        F = 100
        K = 90
        sigma = .2
        r = .02
        t = .5

        flag = 'p'
        c_put = c_analytical.delta(flag, F, K, t, r, sigma)
        py_put = py_analytical.delta(flag, F, K, t, r, sigma)
        self.assertTrue(almost_equal(c_put, py_put))

        flag = 'c'
        c_call = c_analytical.delta(flag, F, K, t, r, sigma)
        py_call = py_analytical.delta(flag, F, K, t, r, sigma)
        self.assertTrue(almost_equal(c_call, py_call))

    def test_analytical_gamma(self):
        F = 100
        K = 90
        sigma = .2
        r = .02
        t = .5

        flag = 'p'
        c_put = c_analytical.gamma(flag, F, K, t, r, sigma)
        py_put = py_analytical.gamma(flag, F, K, t, r, sigma)
        self.assertTrue(almost_equal(c_put, py_put))

        flag = 'c'
        c_call = c_analytical.gamma(flag, F, K, t, r, sigma)
        py_call = py_analytical.gamma(flag, F, K, t, r, sigma)
        self.assertTrue(almost_equal(c_call, py_call))

    def test_analytical_rho(self):
        F = 100
        K = 90
        sigma = .2
        r = .02
        t = .5

        flag = 'p'
        c_put = c_analytical.rho(flag, F, K, t, r, sigma)
        py_put = py_analytical.rho(flag, F, K, t, r, sigma)
        self.assertTrue(almost_equal(c_put, py_put))

        flag = 'c'
        c_call = c_analytical.rho(flag, F, K, t, r, sigma)
        py_call = py_analytical.rho(flag, F, K, t, r, sigma)
        self.assertTrue(almost_equal(c_call, py_call))

    def test_analytical_theta(self):
        F = 100
        K = 90
        sigma = .2
        r = .02
        t = .5

        flag = 'p'
        c_put = c_analytical.theta(flag, F, K, t, r, sigma)
        py_put = py_analytical.theta(flag, F, K, t, r, sigma)
        self.assertTrue(almost_equal(c_put, py_put))

        flag = 'c'
        c_call = c_analytical.theta(flag, F, K, t, r, sigma)
        py_call = py_analytical.theta(flag, F, K, t, r, sigma)
        self.assertTrue(almost_equal(c_call, py_call))

    def test_analytical_vega(self):
        F = 100
        K = 90
        sigma = .2
        r = .02
        t = .5

        flag = 'p'
        c_put = c_analytical.vega(flag, F, K, t, r, sigma)
        py_put = py_analytical.vega(flag, F, K, t, r, sigma)
        self.assertTrue(almost_equal(c_put, py_put))

        flag = 'c'
        c_call = c_analytical.vega(flag, F, K, t, r, sigma)
        py_call = py_analytical.vega(flag, F, K, t, r, sigma)
        self.assertTrue(almost_equal(c_call, py_call))

    def test_numerical_delta(self):
        F = 100
        K = 90
        sigma = .2
        r = .02
        t = .5

        flag = 'p'
        c_put = c_numerical.delta(flag, F, K, t, r, sigma)
        py_put = py_numerical.delta(flag, F, K, t, r, sigma)
        self.assertTrue(almost_equal(c_put, py_put))

        flag = 'c'
        c_call = c_numerical.delta(flag, F, K, t, r, sigma)
        py_call = py_numerical.delta(flag, F, K, t, r, sigma)
        self.assertTrue(almost_equal(c_call, py_call))

    def test_numerical_gamma(self):
        F = 100
        K = 90
        sigma = .2
        r = .02
        t = .5

        flag = 'p'
        c_put = c_numerical.gamma(flag, F, K, t, r, sigma)
        py_put = py_numerical.gamma(flag, F, K, t, r, sigma)
        self.assertTrue(almost_equal(c_put, py_put))

        flag = 'c'
        c_call = c_numerical.gamma(flag, F, K, t, r, sigma)
        py_call = py_numerical.gamma(flag, F, K, t, r, sigma)
        self.assertTrue(almost_equal(c_call, py_call))

    def test_numerical_rho(self):
        F = 100
        K = 90
        sigma = .2
        r = .02
        t = .5

        flag = 'p'
        c_put = c_numerical.rho(flag, F, K, t, r, sigma)
        py_put = py_numerical.rho(flag, F, K, t, r, sigma)
        self.assertTrue(almost_equal(c_put, py_put))

        flag = 'c'
        c_call = c_numerical.rho(flag, F, K, t, r, sigma)
        py_call = py_numerical.rho(flag, F, K, t, r, sigma)
        self.assertTrue(almost_equal(c_call, py_call))

    def test_numerical_theta(self):
        F = 100
        K = 90
        sigma = .2
        r = .02
        t = .5

        flag = 'p'
        c_put = c_numerical.theta(flag, F, K, t, r, sigma)
        py_put = py_numerical.theta(flag, F, K, t, r, sigma)
        self.assertTrue(almost_equal(c_put, py_put))

        flag = 'c'
        c_call = c_numerical.theta(flag, F, K, t, r, sigma)
        py_call = py_numerical.theta(flag, F, K, t, r, sigma)
        self.assertTrue(almost_equal(c_call, py_call))

    def test_numerical_vega(self):
        F = 100
        K = 90
        sigma = .2
        r = .02
        t = .5

        flag = 'p'
        c_put = c_numerical.vega(flag, F, K, t, r, sigma)
        py_put = py_numerical.vega(flag, F, K, t, r, sigma)
        self.assertTrue(almost_equal(c_put, py_put))

        flag = 'c'
        c_call = c_numerical.vega(flag, F, K, t, r, sigma)
        py_call = py_numerical.vega(flag, F, K, t, r, sigma)
        self.assertTrue(almost_equal(c_call, py_call))


if __name__ == '__main__':
    unittest.main()
