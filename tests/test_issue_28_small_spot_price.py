# tests/test_issue_28_small_spot_price.py
"""
Test for Issue #28: Numerical greeks return NaN/error for spot prices < 0.01
https://github.com/vollib/py_vollib/issues/28
"""
import pytest
from vollib.black_scholes.greeks.numerical import delta, gamma, vega, theta, rho


def test_numerical_greeks_with_small_spot_price():
    """Test that numerical greeks work correctly with very small spot prices."""
    # These parameters trigger the bug in the old code
    S = 0.005  # Spot price < 0.01
    K = 0.01
    t = 0.25
    r = 0.05
    sigma = 0.2
    flag = 'c'

    # These should NOT raise errors or return NaN
    delta_val = delta(flag, S, K, t, r, sigma)
    gamma_val = gamma(flag, S, K, t, r, sigma)
    vega_val = vega(flag, S, K, t, r, sigma)
    theta_val = theta(flag, S, K, t, r, sigma)
    rho_val = rho(flag, S, K, t, r, sigma)

    # All should be finite numbers
    assert not (delta_val != delta_val), "Delta is NaN"  # NaN check
    assert not (gamma_val != gamma_val), "Gamma is NaN"
    assert not (vega_val != vega_val), "Vega is NaN"
    assert not (theta_val != theta_val), "Theta is NaN"
    assert not (rho_val != rho_val), "Rho is NaN"

    # Sanity check: delta should be between 0 and 1 for calls
    assert 0 <= delta_val <= 1, f"Delta out of bounds: {delta_val}"


def test_numerical_greeks_extreme_small_spot():
    """Test with even smaller spot prices."""
    S = 0.0001
    K = 0.001
    t = 0.25
    r = 0.05
    sigma = 0.2

    # Should work for both calls and puts
    for flag in ['c', 'p']:
        delta_val = delta(flag, S, K, t, r, sigma)
        gamma_val = gamma(flag, S, K, t, r, sigma)

        assert not (delta_val != delta_val), f"{flag} Delta is NaN"
        assert not (gamma_val != gamma_val), f"{flag} Gamma is NaN"


def test_numerical_greeks_zero_spot_price():
    """Test edge case: S = 0 should handle gracefully."""
    S = 0.0
    K = 100
    t = 0.25
    r = 0.05
    sigma = 0.2

    # For S=0:
    # - Call option: worthless, delta ~ 0
    # - Put option: worth K*exp(-r*t), delta ~ -1

    # Should not crash or return NaN
    delta_call = delta('c', S, K, t, r, sigma)
    delta_put = delta('p', S, K, t, r, sigma)
    gamma_call = gamma('c', S, K, t, r, sigma)
    gamma_put = gamma('p', S, K, t, r, sigma)

    assert not (delta_call != delta_call), "Call Delta is NaN with S=0"
    assert not (delta_put != delta_put), "Put Delta is NaN with S=0"
    assert not (gamma_call != gamma_call), "Call Gamma is NaN with S=0"
    assert not (gamma_put != gamma_put), "Put Gamma is NaN with S=0"

    # Call with S=0 should have delta near 0
    assert abs(delta_call) < 0.01, f"Call delta should be ~0 when S=0, got {delta_call}"
    # Put with S=0 should have delta near -1
    assert abs(delta_put + 1) < 0.01, f"Put delta should be ~-1 when S=0, got {delta_put}"


def test_numerical_greeks_nearly_zero_spot():
    """Test with extremely small but non-zero spot prices."""
    test_cases = [
        (1e-6, 0.001),   # Very small
        (1e-9, 0.001),   # Extremely small
        (1e-12, 0.001),  # Nearly zero
    ]

    t = 0.25
    r = 0.05
    sigma = 0.2

    for S, K in test_cases:
        delta_call = delta('c', S, K, t, r, sigma)
        delta_put = delta('p', S, K, t, r, sigma)
        gamma_call = gamma('c', S, K, t, r, sigma)
        gamma_put = gamma('p', S, K, t, r, sigma)

        assert not (delta_call != delta_call), f"Call delta is NaN with S={S}"
        assert not (delta_put != delta_put), f"Put delta is NaN with S={S}"
        assert not (gamma_call != gamma_call), f"Call gamma is NaN with S={S}"
        assert not (gamma_put != gamma_put), f"Put gamma is NaN with S={S}"

        # Deep OTM call (S << K) should have delta ~ 0
        assert 0 <= delta_call <= 0.1, f"Call delta should be ~0 with S={S}, K={K}, got {delta_call}"
        # Deep ITM put (S << K) should have delta ~ -1
        assert -1.1 <= delta_put <= -0.9, f"Put delta should be ~-1 with S={S}, K={K}, got {delta_put}"
