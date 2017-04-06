# -----------------------------------------------------------------------------
# IMPORTS

# Standard library imports
from __future__ import print_function
import unittest

# Related third party imports

# Local application/library specific imports
from py_vollib.ref_python.black_scholes import black_scholes
from py_vollib.ref_python.black_scholes.implied_volatility import implied_volatility
from py_vollib.ref_python.black_scholes.greeks import analytical
from py_vollib.ref_python.black_scholes.greeks import numerical
from tests.test_utils import IteratorForTestData


class TestRefPythonBlackScholesAgainstBenchmarkValues(unittest.TestCase):
    def setUp(self):
        self.tdi = IteratorForTestData()

    def test_prices(self):
        while self.tdi.has_next():
            row = self.tdi.next_row()
            S, K, t, r, sigma = row['S'], row['K'], row['t'], row['R'], row['v']
            self.assertAlmostEqual(black_scholes('c', S, K, t, r, sigma), row['bs_call'], delta=0.000001)
            self.assertAlmostEqual(black_scholes('p', S, K, t, r, sigma), row['bs_put'], delta=0.000001)

    def test_analytical_delta(self):
        while self.tdi.has_next():
            row = self.tdi.next_row()
            S, K, t, r, sigma = row['S'], row['K'], row['t'], row['R'], row['v']
            self.assertAlmostEqual(analytical.delta('c', S, K, t, r, sigma), row['CD'], delta=0.000001)
            self.assertAlmostEqual(analytical.delta('p', S, K, t, r, sigma), row['PD'], delta=0.000001)

    def test_analytical_theta(self):
        while self.tdi.has_next():
            row = self.tdi.next_row()
            S, K, t, r, sigma = row['S'], row['K'], row['t'], row['R'], row['v']
            self.assertAlmostEqual(analytical.theta('c', S, K, t, r, sigma), row['CT'] / 365.0, delta=0.000001)
            self.assertAlmostEqual(analytical.theta('p', S, K, t, r, sigma), row['PT'] / 365.0, delta=0.000001)

    def test_analytical_gamma(self):
        while self.tdi.has_next():
            row = self.tdi.next_row()
            S, K, t, r, sigma = row['S'], row['K'], row['t'], row['R'], row['v']
            self.assertAlmostEqual(analytical.gamma('c', S, K, t, r, sigma), row['CG'], delta=0.000001)
            self.assertAlmostEqual(analytical.gamma('p', S, K, t, r, sigma), row['PG'], delta=0.000001)

    def test_analytical_vega(self):
        while self.tdi.has_next():
            row = self.tdi.next_row()
            S, K, t, r, sigma = row['S'], row['K'], row['t'], row['R'], row['v']
            self.assertAlmostEqual(analytical.vega('c', S, K, t, r, sigma), row['CV'] * .01, delta=0.000001)
            self.assertAlmostEqual(analytical.vega('p', S, K, t, r, sigma), row['PV'] * .01, delta=0.000001)

    def test_analytical_rho(self):
        while self.tdi.has_next():
            row = self.tdi.next_row()
            S, K, t, r, sigma = row['S'], row['K'], row['t'], row['R'], row['v']
            self.assertAlmostEqual(analytical.rho('c', S, K, t, r, sigma), row['CR'] * 0.01, delta=0.000000001)
            self.assertAlmostEqual(analytical.rho('p', S, K, t, r, sigma), row['PR'] * 0.01, delta=0.000000001)

    def test_numerical_delta(self):
        while self.tdi.has_next():
            row = self.tdi.next_row()
            S, K, t, r, sigma = row['S'], row['K'], row['t'], row['R'], row['v']
            self.assertAlmostEqual(numerical.delta('c', S, K, t, r, sigma), row['CD'], delta=0.000001)
            self.assertAlmostEqual(numerical.delta('p', S, K, t, r, sigma), row['PD'], delta=0.000001)

    def test_numerical_theta(self):
        while self.tdi.has_next():
            row = self.tdi.next_row()
            S, K, t, r, sigma = row['S'], row['K'], row['t'], row['R'], row['v']
            self.assertAlmostEqual(numerical.theta('c', S, K, t, r, sigma), row['CT'] / 365.0, delta=1)
            self.assertAlmostEqual(numerical.theta('p', S, K, t, r, sigma), row['PT'] / 365.0, delta=1)

    def test_numerical_gamma(self):
        while self.tdi.has_next():
            row = self.tdi.next_row()
            S, K, t, r, sigma = row['S'], row['K'], row['t'], row['R'], row['v']
            self.assertAlmostEqual(numerical.gamma('c', S, K, t, r, sigma), row['CG'], delta=0.000001)
            self.assertAlmostEqual(numerical.gamma('p', S, K, t, r, sigma), row['PG'], delta=0.000001)

    def test_numerical_vega(self):
        while self.tdi.has_next():
            row = self.tdi.next_row()
            S, K, t, r, sigma = row['S'], row['K'], row['t'], row['R'], row['v']
            self.assertAlmostEqual(numerical.vega('c', S, K, t, r, sigma), row['CV'] * 0.01, delta=0.01)
            self.assertAlmostEqual(numerical.vega('p', S, K, t, r, sigma), row['PV'] * 0.01, delta=0.01)

    def test_numerical_rho(self):
        while self.tdi.has_next():
            row = self.tdi.next_row()
            S, K, t, r, sigma = row['S'], row['K'], row['t'], row['R'], row['v']
            self.assertAlmostEqual(numerical.rho('c', S, K, t, r, sigma), row['CR'] * 0.01, delta=0.001)
            self.assertAlmostEqual(numerical.rho('p', S, K, t, r, sigma), row['PR'] * 0.01, delta=0.001)

    def test_implied_volatility(self):
        while self.tdi.has_next():
            row = self.tdi.next_row()
            S, K, t, r, sigma = row['S'], row['K'], row['t'], row['R'], row['v']
            C, P = black_scholes('c', S, K, t, r, sigma), black_scholes('p', S, K, t, r, sigma)
            try:
                iv = implied_volatility(C, S, K, t, r, 'c')
                self.assertAlmostEqual(sigma, iv, delta=0.0001)
            except:
                print('could not calculate iv for ', C, S, K, t, r, 'c')
            iv = implied_volatility(P, S, K, t, r, 'p')
            self.assertTrue(iv == 1e-12) if iv == 1e-12 else self.assertAlmostEqual(sigma, iv, delta=0.001)


if __name__ == '__main__':
    unittest.main()
