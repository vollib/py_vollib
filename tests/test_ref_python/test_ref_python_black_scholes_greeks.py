# -----------------------------------------------------------------------------
# IMPORTS

# Standard library imports
from __future__ import print_function
import unittest
from itertools import product

# Related third party imports
import numpy

# Local application/library specific imports
from py_vollib.ref_python.black_scholes.greeks.analytical import delta
from py_vollib.ref_python.black_scholes.greeks.analytical import gamma
from py_vollib.ref_python.black_scholes.greeks.analytical import theta
from py_vollib.ref_python.black_scholes.greeks.analytical import vega
from py_vollib.ref_python.black_scholes.greeks.analytical import rho
from py_vollib.ref_python.black_scholes.greeks.numerical import delta as ndelta
from py_vollib.ref_python.black_scholes.greeks.numerical import gamma as ngamma
from py_vollib.ref_python.black_scholes.greeks.numerical import theta as ntheta
from py_vollib.ref_python.black_scholes.greeks.numerical import vega as nvega
from py_vollib.ref_python.black_scholes.greeks.numerical import rho as nrho


class TestRefPythonBSGreeks(unittest.TestCase):
    def setUp(self):
        self.epsilon = 0.001
        self.flags = ['c', 'p']
        self.S = 100
        self.Ks = numpy.linspace(20, 200, 10)
        self.ts = numpy.linspace(0.01, 2, 10)
        self.rs = numpy.linspace(0, 0.2, 10)
        self.sigmas = numpy.linspace(0.1, 0.5, 10)
        self.arg_combinations = list(product(self.flags, [self.S], self.Ks, self.ts, self.rs, self.sigmas))

    def diff_mean(self, left, right):
        left_arr = numpy.array(left)
        right_arr = numpy.array(right)
        abs_diff = numpy.abs(left_arr - right_arr)
        return numpy.mean(abs_diff)

    def test_theta(self):
        thetas = [theta(flag, S, K, t, r, sigma) for flag, S, K, t, r, sigma in self.arg_combinations]
        nthetas = [ntheta(flag, S, K, t, r, sigma) for flag, S, K, t, r, sigma in self.arg_combinations]
        self.assertTrue(self.diff_mean(thetas, nthetas) < self.epsilon)

    def test_delta(self):
        deltas = [delta(flag, S, K, t, r, sigma) for flag, S, K, t, r, sigma in self.arg_combinations]
        ndeltas = [ndelta(flag, S, K, t, r, sigma) for flag, S, K, t, r, sigma in self.arg_combinations]
        self.assertTrue(self.diff_mean(deltas, ndeltas) < self.epsilon)

    def test_gamma(self):
        gammas = [gamma(flag, S, K, t, r, sigma) for flag, S, K, t, r, sigma in self.arg_combinations]
        ngammas = [ngamma(flag, S, K, t, r, sigma) for flag, S, K, t, r, sigma in self.arg_combinations]
        self.assertTrue(self.diff_mean(gammas, ngammas) < self.epsilon)

    def test_vega(self):
        vegas = [vega(flag, S, K, t, r, sigma) for flag, S, K, t, r, sigma in self.arg_combinations]
        nvegas = [nvega(flag, S, K, t, r, sigma) for flag, S, K, t, r, sigma in self.arg_combinations]
        self.assertTrue(self.diff_mean(vegas, nvegas) < self.epsilon)

    def test_rho(self):
        rhos = [rho(flag, S, K, t, r, sigma) for flag, S, K, t, r, sigma in self.arg_combinations]
        nrhos = [nrho(flag, S, K, t, r, sigma) for flag, S, K, t, r, sigma in self.arg_combinations]
        self.assertTrue(self.diff_mean(rhos, nrhos) < self.epsilon)


if __name__ == '__main__':
    unittest.main()
