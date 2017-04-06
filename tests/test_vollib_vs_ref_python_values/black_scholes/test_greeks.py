# -----------------------------------------------------------------------------
# IMPORTS

# Standard library imports
import unittest

# Related third party imports

# Local application/library specific imports
from py_vollib.black_scholes.greeks import analytical as c_analytical
from py_vollib.black_scholes.greeks import numerical as c_numerical
from py_vollib.ref_python.black_scholes.greeks import analytical as py_analytical
from py_vollib.ref_python.black_scholes.greeks import numerical as py_numerical
from tests.test_utils import almost_equal


class TestGreeks(unittest.TestCase):
    def test_analytical_delta(self):
        S = 49
        K = 50
        sigma = .2
        r = .05
        t = 0.3846

        flag = 'p'
        c_put = c_analytical.delta(flag, S, K, t, r, sigma)
        py_put = py_analytical.delta(flag, S, K, t, r, sigma)
        self.assertTrue(almost_equal(c_put, py_put))

        flag = 'c'
        c_call = c_analytical.delta(flag, S, K, t, r, sigma)
        py_call = py_analytical.delta(flag, S, K, t, r, sigma)
        self.assertTrue(almost_equal(c_call, py_call))

    def test_analytical_gamma(self):
        S = 49
        K = 50
        sigma = .2
        r = .05
        t = 0.3846

        flag = 'p'
        c_put = c_analytical.gamma(flag, S, K, t, r, sigma)
        py_put = py_analytical.gamma(flag, S, K, t, r, sigma)
        self.assertTrue(almost_equal(c_put, py_put))

        flag = 'c'
        c_call = c_analytical.gamma(flag, S, K, t, r, sigma)
        py_call = py_analytical.gamma(flag, S, K, t, r, sigma)
        self.assertTrue(almost_equal(c_call, py_call))

    def test_analytical_rho(self):
        S = 49
        K = 50
        sigma = .2
        r = .05
        t = 0.3846

        flag = 'p'
        c_put = c_analytical.rho(flag, S, K, t, r, sigma)
        py_put = py_analytical.rho(flag, S, K, t, r, sigma)
        self.assertTrue(almost_equal(c_put, py_put))

        flag = 'c'
        c_call = c_analytical.rho(flag, S, K, t, r, sigma)
        py_call = py_analytical.rho(flag, S, K, t, r, sigma)
        self.assertTrue(almost_equal(c_call, py_call))

    def test_analytical_theta(self):
        S = 49
        K = 50
        sigma = .2
        r = .05
        t = 0.3846

        flag = 'p'
        c_put = c_analytical.theta(flag, S, K, t, r, sigma)
        py_put = py_analytical.theta(flag, S, K, t, r, sigma)
        self.assertTrue(almost_equal(c_put, py_put))

        flag = 'c'
        c_call = c_analytical.theta(flag, S, K, t, r, sigma)
        py_call = py_analytical.theta(flag, S, K, t, r, sigma)
        self.assertTrue(almost_equal(c_call, py_call))

    def test_analytical_vega(self):
        S = 49
        K = 50
        sigma = .2
        r = .05
        t = 0.3846

        flag = 'p'
        c_put = c_analytical.vega(flag, S, K, t, r, sigma)
        py_put = py_analytical.vega(flag, S, K, t, r, sigma)
        self.assertTrue(almost_equal(c_put, py_put))

        flag = 'c'
        c_call = c_analytical.vega(flag, S, K, t, r, sigma)
        py_call = py_analytical.vega(flag, S, K, t, r, sigma)
        self.assertTrue(almost_equal(c_call, py_call))

    def test_numerical_delta(self):
        S = 49
        K = 50
        sigma = .2
        r = .05
        t = 0.3846

        flag = 'p'
        c_put = c_numerical.delta(flag, S, K, t, r, sigma)
        py_put = py_numerical.delta(flag, S, K, t, r, sigma)
        self.assertTrue(almost_equal(c_put, py_put))

        flag = 'c'
        c_call = c_numerical.delta(flag, S, K, t, r, sigma)
        py_call = py_numerical.delta(flag, S, K, t, r, sigma)
        self.assertTrue(almost_equal(c_call, py_call))

    def test_numerical_gamma(self):
        S = 49
        K = 50
        sigma = .2
        r = .05
        t = 0.3846

        flag = 'p'
        c_put = c_numerical.gamma(flag, S, K, t, r, sigma)
        py_put = py_numerical.gamma(flag, S, K, t, r, sigma)
        self.assertTrue(almost_equal(c_put, py_put))

        flag = 'c'
        c_call = c_numerical.gamma(flag, S, K, t, r, sigma)
        py_call = py_numerical.gamma(flag, S, K, t, r, sigma)
        self.assertTrue(almost_equal(c_call, py_call))

    def test_numerical_rho(self):
        S = 49
        K = 50
        sigma = .2
        r = .05
        t = 0.3846

        flag = 'p'
        c_put = c_numerical.rho(flag, S, K, t, r, sigma)
        py_put = py_numerical.rho(flag, S, K, t, r, sigma)
        self.assertTrue(almost_equal(c_put, py_put))

        flag = 'c'
        c_call = c_numerical.rho(flag, S, K, t, r, sigma)
        py_call = py_numerical.rho(flag, S, K, t, r, sigma)
        self.assertTrue(almost_equal(c_call, py_call))

    def test_numerical_theta(self):
        S = 49
        K = 50
        sigma = .2
        r = .05
        t = 0.3846

        flag = 'p'
        c_put = c_numerical.theta(flag, S, K, t, r, sigma)
        py_put = py_numerical.theta(flag, S, K, t, r, sigma)
        self.assertTrue(almost_equal(c_put, py_put))

        flag = 'c'
        c_call = c_numerical.theta(flag, S, K, t, r, sigma)
        py_call = py_numerical.theta(flag, S, K, t, r, sigma)
        self.assertTrue(almost_equal(c_call, py_call))

    def test_numerical_vega(self):
        S = 49
        K = 50
        sigma = .2
        r = .05
        t = 0.3846

        flag = 'p'
        c_put = c_numerical.vega(flag, S, K, t, r, sigma)
        py_put = py_numerical.vega(flag, S, K, t, r, sigma)
        self.assertTrue(almost_equal(c_put, py_put))

        flag = 'c'
        c_call = c_numerical.vega(flag, S, K, t, r, sigma)
        py_call = py_numerical.vega(flag, S, K, t, r, sigma)
        self.assertTrue(almost_equal(c_call, py_call))


if __name__ == '__main__':
    unittest.main()
