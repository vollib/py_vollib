# -*- coding: utf-8 -*-

"""
vollib.lets_be_rational.core
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Core implied volatility calculations based on Peter Jaeckel's LetsBeRational.

:copyright: 2017 Gammon Capital LLC
:license: MIT, see LICENSE for more details.

======================================================================================
Copyright 2013-2014 Peter Jaeckel.

Permission to use, copy, modify, and distribute this software is freely granted,
provided that this notice is preserved.

WARRANTY DISCLAIMER
The Software is provided "as is" without warranty of any kind, either express or implied,
including without limitation any implied warranties of condition, uninterrupted use,
merchantability, fitness for a particular purpose, or non-infringement.
======================================================================================
"""

from math import fabs, sqrt, log, exp

from cody_special import norm_cdf, norm_pdf
from cody_special.erf_cody import erfcx_cody
from cody_special.constants import (
    DBL_MAX, DBL_MIN, DBL_EPSILON,
    ONE_OVER_SQRT_TWO, ONE_OVER_SQRT_TWO_PI,
    SQRT_TWO_PI, TWO_PI
)
from piecewise_rational import (
    rational_cubic_interpolation,
    convex_rational_cubic_control_parameter_to_fit_second_derivative_at_left_side,
    convex_rational_cubic_control_parameter_to_fit_second_derivative_at_right_side,
)
from cody_special.normaldistribution import inverse_norm_cdf

from vollib.lets_be_rational.exceptions import BelowIntrinsicException, AboveMaximumException
from vollib.lets_be_rational.constants import (
    SQRT_DBL_EPSILON, FOURTH_ROOT_DBL_EPSILON, SIXTEENTH_ROOT_DBL_EPSILON,
    SQRT_DBL_MIN, SQRT_DBL_MAX, DENORMALIZATION_CUTOFF,
    SQRT_THREE, SQRT_ONE_OVER_THREE, TWO_PI_OVER_SQRT_TWENTY_SEVEN,
    PI_OVER_SIX, SQRT_PI_OVER_TWO,
)


implied_volatility_maximum_iterations = 2
asymptotic_expansion_accuracy_threshold = -10
small_t_expansion_of_normalized_black_threshold = 2 * SIXTEENTH_ROOT_DBL_EPSILON


def _householder_factor(newton, halley, hh3):
    return (1 + 0.5 * halley * newton) / (1 + newton * (halley + hh3 * newton / 6))


def _compute_f_lower_map_and_first_two_derivatives(x, s):
    ax = fabs(x)
    z = SQRT_ONE_OVER_THREE * ax / s
    y = z * z
    s2 = s * s
    Phi = norm_cdf(-z)
    phi = norm_pdf(z)
    fpp = PI_OVER_SIX * y / (s2 * s) * Phi * (
        8 * SQRT_THREE * s * ax + (3 * s2 * (s2 - 8) - 8 * x * x) * Phi / phi) * exp(2 * y + 0.25 * s2)
    if _is_below_horizon(s):
        fp = 1
        f = 0
    else:
        Phi2 = Phi * Phi
        fp = TWO_PI * y * Phi2 * exp(y + 0.125 * s * s)
        if _is_below_horizon(x):
            f = 0
        else:
            f = TWO_PI_OVER_SQRT_TWENTY_SEVEN * ax * (Phi2 * Phi)
    return f, fp, fpp


def _compute_f_upper_map_and_first_two_derivatives(x, s):
    f = norm_cdf(-0.5 * s)
    if _is_below_horizon(x):
        fp = -0.5
        fpp = 0
    else:
        w = _square(x / s)
        fp = -0.5 * exp(0.5 * w)
        fpp = SQRT_PI_OVER_TWO * exp(w + 0.125 * s * s) * w / s

    return f, fp, fpp


def _square(x):
    return x * x


def _inverse_f_lower_map(x, f):
    return 0 if _is_below_horizon(f) else fabs(
        x / (SQRT_THREE * inverse_norm_cdf(pow(f / (TWO_PI_OVER_SQRT_TWENTY_SEVEN * fabs(x)), 1. / 3.))))


def _inverse_f_upper_map(f):
    return -2. * inverse_norm_cdf(f)


def _is_below_horizon(x):
    """This weeds out denormalized (a.k.a. 'subnormal') numbers."""
    return fabs(x) < DENORMALIZATION_CUTOFF


def _normalized_black_call_using_norm_cdf(x, s):
    h = x / s
    t = 0.5 * s
    b_max = exp(0.5 * x)
    b = norm_cdf(h + t) * b_max - norm_cdf(h - t) / b_max
    return fabs(max(b, 0.0))


def _asymptotic_expansion_of_normalized_black_call(h, t):
    e = (t / h) * (t / h)
    r = ((h + t) * (h - t))
    q = (h / r) * (h / r)
    asymptotic_expansion_sum = (2.0+q*(-6.0E0-2.0*e+3.0*q*(1.0E1+e*(2.0E1+2.0*e)+5.0*q*(-1.4E1+e*(-7.0E1+e*(-4.2E1-2.0*e))+7.0*q*(1.8E1+e*(1.68E2+e*(2.52E2+e*(7.2E1+2.0*e)))+9.0*q*(-2.2E1+e*(-3.3E2+e*(-9.24E2+e*(-6.6E2+e*(-1.1E2-2.0*e))))+1.1E1*q*(2.6E1+e*(5.72E2+e*(2.574E3+e*(3.432E3+e*(1.43E3+e*(1.56E2+2.0*e)))))+1.3E1*q*(-3.0E1+e*(-9.1E2+e*(-6.006E3+e*(-1.287E4+e*(-1.001E4+e*(-2.73E3+e*(-2.1E2-2.0*e))))))+1.5E1*q*(3.4E1+e*(1.36E3+e*(1.2376E4+e*(3.8896E4+e*(4.862E4+e*(2.4752E4+e*(4.76E3+e*(2.72E2+2.0*e)))))))+1.7E1*q*(-3.8E1+e*(-1.938E3+e*(-2.3256E4+e*(-1.00776E5+e*(-1.84756E5+e*(-1.51164E5+e*(-5.4264E4+e*(-7.752E3+e*(-3.42E2-2.0*e))))))))+1.9E1*q*(4.2E1+e*(2.66E3+e*(4.0698E4+e*(2.3256E5+e*(5.8786E5+e*(7.05432E5+e*(4.0698E5+e*(1.08528E5+e*(1.197E4+e*(4.2E2+2.0*e)))))))))+2.1E1*q*(-4.6E1+e*(-3.542E3+e*(-6.7298E4+e*(-4.90314E5+e*(-1.63438E6+e*(-2.704156E6+e*(-2.288132E6+e*(-9.80628E5+e*(-2.01894E5+e*(-1.771E4+e*(-5.06E2-2.0*e))))))))))+2.3E1*q*(5.0E1+e*(4.6E3+e*(1.0626E5+e*(9.614E5+e*(4.08595E6+e*(8.9148E6+e*(1.04006E7+e*(6.53752E6+e*(2.16315E6+e*(3.542E5+e*(2.53E4+e*(6.0E2+2.0*e)))))))))))+2.5E1*q*(-5.4E1+e*(-5.85E3+e*(-1.6146E5+e*(-1.77606E6+e*(-9.37365E6+e*(-2.607579E7+e*(-4.01166E7+e*(-3.476772E7+e*(-1.687257E7+e*(-4.44015E6+e*(-5.9202E5+e*(-3.51E4+e*(-7.02E2-2.0*e))))))))))))+2.7E1*q*(5.8E1+e*(7.308E3+e*(2.3751E5+e*(3.12156E6+e*(2.003001E7+e*(6.919458E7+e*(1.3572783E8+e*(1.5511752E8+e*(1.0379187E8+e*(4.006002E7+e*(8.58429E6+e*(9.5004E5+e*(4.7502E4+e*(8.12E2+2.0*e)))))))))))))+2.9E1*q*(-6.2E1+e*(-8.99E3+e*(-3.39822E5+e*(-5.25915E6+e*(-4.032015E7+e*(-1.6934463E8+e*(-4.1250615E8+e*(-6.0108039E8+e*(-5.3036505E8+e*(-2.8224105E8+e*(-8.870433E7+e*(-1.577745E7+e*(-1.472562E6+e*(-6.293E4+e*(-9.3E2-2.0*e))))))))))))))+3.1E1*q*(6.6E1+e*(1.0912E4+e*(4.74672E5+e*(8.544096E6+e*(7.71342E7+e*(3.8707344E8+e*(1.14633288E9+e*(2.07431664E9+e*(2.33360622E9+e*(1.6376184E9+e*(7.0963464E8+e*(1.8512208E8+e*(2.7768312E7+e*(2.215136E6+e*(8.184E4+e*(1.056E3+2.0*e)))))))))))))))+3.3E1*(-7.0E1+e*(-1.309E4+e*(-6.49264E5+e*(-1.344904E7+e*(-1.4121492E8+e*(-8.344518E8+e*(-2.9526756E9+e*(-6.49588632E9+e*(-9.0751353E9+e*(-8.1198579E9+e*(-4.6399188E9+e*(-1.6689036E9+e*(-3.67158792E8+e*(-4.707164E7+e*(-3.24632E6+e*(-1.0472E5+e*(-1.19E3-2.0*e)))))))))))))))))*q)))))))))))))))))
    b = ONE_OVER_SQRT_TWO_PI * exp((-0.5 * (h * h + t * t))) * (t / r) * asymptotic_expansion_sum
    return fabs(max(b, 0.))


def _small_t_expansion_of_normalized_black_call(h, t):
    a = 1 + h * (0.5 * SQRT_TWO_PI) * erfcx_cody(-ONE_OVER_SQRT_TWO * h)
    w = t * t
    h2 = h * h
    expansion = 2*t*(a+w*((-1+3*a+a*h2)/6+w*((-7+15*a+h2*(-1+10*a+a*h2))/120+w*((-57+105*a+h2*(-18+105*a+h2*(-1+21*a+a*h2)))/5040+w*((-561+945*a+h2*(-285+1260*a+h2*(-33+378*a+h2*(-1+36*a+a*h2))))/362880+w*((-6555+10395*a+h2*(-4680+17325*a+h2*(-840+6930*a+h2*(-52+990*a+h2*(-1+55*a+a*h2)))))/39916800+((-89055+135135*a+h2*(-82845+270270*a+h2*(-20370+135135*a+h2*(-1926+25740*a+h2*(-75+2145*a+h2*(-1+78*a+a*h2))))))*w)/6227020800.0))))))
    b = ONE_OVER_SQRT_TWO_PI * exp((-0.5 * (h * h + t * t))) * expansion
    return fabs(max(b, 0.0))


def _normalised_black_call_using_erfcx(h, t):
    b = 0.5 * exp(-0.5 * (h * h + t * t)) * (erfcx_cody(-ONE_OVER_SQRT_TWO * (h + t)) - erfcx_cody(-ONE_OVER_SQRT_TWO * (h - t)))
    return fabs(max(b, 0.0))


def _unchecked_normalised_implied_volatility_from_a_transformed_rational_guess_with_limited_iterations(beta, x, q, N):
    # Subtract intrinsic.
    if q * x > 0:
        beta = fabs(max(beta - _normalised_intrinsic(x, q), 0.))
        q = -q
    # Map puts to calls
    if q < 0:
        x = -x
        q = -q
    if beta <= 0:
        return 0
    if beta < DENORMALIZATION_CUTOFF:
        return 0
    b_max = exp(0.5 * x)
    if beta >= b_max:
        raise AboveMaximumException
    iterations = 0
    direction_reversal_count = 0
    f = -DBL_MAX
    s = -DBL_MAX
    ds = s
    ds_previous = 0
    s_left = DBL_MIN
    s_right = DBL_MAX
    s_c = sqrt(fabs(2 * x))
    b_c = normalised_black_call(x, s_c)
    v_c = normalised_vega(x, s_c)
    # Four branches.
    if beta < b_c:
        s_l = s_c - b_c / v_c
        b_l = normalised_black_call(x, s_l)
        if beta < b_l:
            f_lower_map_l, d_f_lower_map_l_d_beta, d2_f_lower_map_l_d_beta2 = _compute_f_lower_map_and_first_two_derivatives(x, s_l)
            r_ll = convex_rational_cubic_control_parameter_to_fit_second_derivative_at_right_side(0., b_l, 0., f_lower_map_l, 1., d_f_lower_map_l_d_beta, d2_f_lower_map_l_d_beta2, True)
            f = rational_cubic_interpolation(beta, 0., b_l, 0., f_lower_map_l, 1., d_f_lower_map_l_d_beta, r_ll)
            if not (f > 0):
                t = beta / b_l
                f = (f_lower_map_l * t + b_l * (1 - t)) * t

            s = _inverse_f_lower_map(x, f)
            s_right = s_l
            while (iterations < N and fabs(ds) > DBL_EPSILON * s):
                if ds * ds_previous < 0:
                    direction_reversal_count += 1
                if iterations > 0 and (3 == direction_reversal_count or not (s > s_left and s < s_right)):
                    s = 0.5 * (s_left + s_right)
                    if s_right - s_left <= DBL_EPSILON * s:
                        break
                    direction_reversal_count = 0
                    ds = 0
                ds_previous = ds
                b = normalised_black_call(x, s)
                bp = normalised_vega(x, s)
                if b > beta and s < s_right:
                    s_right = s
                elif b < beta and s > s_left:
                    s_left = s
                if b <= 0 or bp <= 0:
                    ds = 0.5 * (s_left + s_right) - s
                else:
                    ln_b = log(b)
                    ln_beta = log(beta)
                    bpob = bp / b
                    h = x / s
                    b_halley = h * h / s - s / 4
                    newton = (ln_beta - ln_b) * ln_b / ln_beta / bpob
                    halley = b_halley - bpob * (1 + 2 / ln_b)
                    b_hh3 = b_halley * b_halley - 3 * _square(h / s) - 0.25
                    hh3 = b_hh3 + 2 * _square(bpob) * (1 + 3 / ln_b * (1 + 1 / ln_b)) - 3 * b_halley * bpob * (1 + 2 / ln_b)
                    ds = newton * _householder_factor(newton, halley, hh3)
                ds = max(-0.5 * s, ds)
                s += ds
                iterations += 1
            return s
        else:
            v_l = normalised_vega(x, s_l)
            r_lm = convex_rational_cubic_control_parameter_to_fit_second_derivative_at_right_side(b_l, b_c, s_l, s_c, 1 / v_l, 1 / v_c, 0.0, False)
            s = rational_cubic_interpolation(beta, b_l, b_c, s_l, s_c, 1 / v_l, 1 / v_c, r_lm)
            s_left = s_l
            s_right = s_c
    else:
        s_h = s_c + (b_max - b_c) / v_c if v_c > DBL_MIN else s_c
        b_h = normalised_black_call(x, s_h)
        if beta <= b_h:
            v_h = normalised_vega(x, s_h)
            r_hm = convex_rational_cubic_control_parameter_to_fit_second_derivative_at_left_side(b_c, b_h, s_c, s_h, 1 / v_c, 1 / v_h, 0.0, False)
            s = rational_cubic_interpolation(beta, b_c, b_h, s_c, s_h, 1 / v_c, 1 / v_h, r_hm)
            s_left = s_c
            s_right = s_h
        else:
            f_upper_map_h, d_f_upper_map_h_d_beta, d2_f_upper_map_h_d_beta2 = _compute_f_upper_map_and_first_two_derivatives(x, s_h)
            if d2_f_upper_map_h_d_beta2 > -SQRT_DBL_MAX < SQRT_DBL_MAX:
                r_hh = convex_rational_cubic_control_parameter_to_fit_second_derivative_at_left_side(b_h, b_max, f_upper_map_h, 0., d_f_upper_map_h_d_beta, -0.5, d2_f_upper_map_h_d_beta2, True)
                f = rational_cubic_interpolation(beta, b_h, b_max, f_upper_map_h, 0., d_f_upper_map_h_d_beta, -0.5, r_hh)
            if f <= 0:
                h = b_max - b_h
                t = (beta - b_h) / h
                f = (f_upper_map_h * (1 - t) + 0.5 * h * t) * (1 - t)
            s = _inverse_f_upper_map(f)
            s_left = s_h
            if beta > 0.5 * b_max:
                while iterations < N and fabs(ds) > DBL_EPSILON * s:
                    if ds * ds_previous < 0:
                        direction_reversal_count += 1
                    if iterations > 0 and (3 == direction_reversal_count or not (s > s_left and s < s_right)):
                        s = 0.5 * (s_left + s_right)
                    if (s_right - s_left <= DBL_EPSILON * s):
                        break
                    direction_reversal_count = 0
                    ds = 0
                    ds_previous = ds
                    b = normalised_black_call(x, s)
                    bp = normalised_vega(x, s)
                    if b > beta and s < s_right:
                        s_right = s
                    elif b < beta and s > s_left:
                        s_left = s
                    if b >= b_max or bp <= DBL_MIN:
                        ds = 0.5 * (s_left + s_right) - s
                    else:
                        b_max_minus_b = b_max - b
                        g = log((b_max - beta) / b_max_minus_b)
                        gp = bp / b_max_minus_b
                        b_halley = _square(x / s) / s - s / 4
                        b_hh3 = b_halley * b_halley - 3 * _square(x / (s * s)) - 0.25
                        newton = -g / gp
                        halley = b_halley + gp
                        hh3 = b_hh3 + gp * (2 * gp + 3 * b_halley)
                        ds = newton * _householder_factor(newton, halley, hh3)
                    ds = max(-0.5 * s, ds)
                    s += ds
                    iterations += 1
                return s
    # Middle segments
    while iterations < N and fabs(ds) > DBL_EPSILON * s:
        if ds * ds_previous < 0:
            direction_reversal_count += 1
        if iterations > 0 and (3 == direction_reversal_count or not (s > s_left and s < s_right)):
            s = 0.5 * (s_left + s_right)
            if s_right - s_left <= DBL_EPSILON * s:
                break
            direction_reversal_count = 0
            ds = 0
        ds_previous = ds
        b = normalised_black_call(x, s)
        bp = normalised_vega(x, s)
        if b > beta and s < s_right:
            s_right = s
        elif b < beta and s > s_left:
            s_left = s
        newton = (beta - b) / bp
        halley = _square(x / s) / s - s / 4
        hh3 = halley * halley - 3 * _square(x / (s * s)) - 0.25
        ds = max(-0.5 * s, newton * _householder_factor(newton, halley, hh3))
        s += ds
        iterations += 1
    return s


def normalised_implied_volatility_from_a_transformed_rational_guess_with_limited_iterations(beta, x, q, N):
    # Map in-the-money to out-of-the-money
    if q * x > 0:
        beta -= _normalised_intrinsic(x, q)
        q = -q

    if beta < 0:
        raise BelowIntrinsicException
    return _unchecked_normalised_implied_volatility_from_a_transformed_rational_guess_with_limited_iterations(beta, x, q, N)


def implied_volatility_from_a_transformed_rational_guess_with_limited_iterations(price, F, K, T, q, N):
    intrinsic = fabs(max(K - F if q < 0 else F - K, 0.0))
    if price < intrinsic:
        raise BelowIntrinsicException
    max_price = K if q < 0 else F
    if price >= max_price:
        raise AboveMaximumException
    x = log(F / K)
    # Map in-the-money to out-of-the-money
    if q * x > 0:
        price = fabs(max(price - intrinsic, 0.0))
        q = -q
    return _unchecked_normalised_implied_volatility_from_a_transformed_rational_guess_with_limited_iterations(
        price / (sqrt(F) * sqrt(K)), x, q, N) / sqrt(T)


def normalised_implied_volatility_from_a_transformed_rational_guess(beta, x, q):
    return normalised_implied_volatility_from_a_transformed_rational_guess_with_limited_iterations(
        beta, x, q, implied_volatility_maximum_iterations)


def implied_volatility_from_a_transformed_rational_guess(price, F, K, T, q):
    return implied_volatility_from_a_transformed_rational_guess_with_limited_iterations(
        price, F, K, T, q, implied_volatility_maximum_iterations)


def normalised_vega(x, s):
    ax = fabs(x)
    if ax <= 0:
        return ONE_OVER_SQRT_TWO_PI * exp(-0.125 * s * s)
    else:
        return 0 if s <= 0 or s <= ax * SQRT_DBL_MIN else ONE_OVER_SQRT_TWO_PI * exp(-0.5 * (_square(x / s) + _square(0.5 * s)))


def _normalised_intrinsic(x, q):
    if q * x <= 0:
        return 0
    x2 = x * x
    if x2 < 98 * FOURTH_ROOT_DBL_EPSILON:
        return fabs(max((-1 if q < 0 else 1) * x * (1 + x2 * ((1.0 / 24.0) + x2 * ((1.0 / 1920.0) + x2 * ((1.0 / 322560.0) + (1.0 / 92897280.0) * x2)))), 0.0))
    b_max = exp(0.5 * x)
    one_over_b_max = 1 / b_max
    return fabs(max((-1 if q < 0 else 1) * (b_max - one_over_b_max), 0.))


def _normalised_intrinsic_call(x):
    return _normalised_intrinsic(x, 1)


def normalised_black_call(x, s):
    if x > 0:
        return _normalised_intrinsic_call(x) + normalised_black_call(-x, s)
    ax = fabs(x)
    if s <= ax * DENORMALIZATION_CUTOFF:
        return _normalised_intrinsic_call(x)
    if x < s * asymptotic_expansion_accuracy_threshold and 0.5 * s * s + x < s * (
        small_t_expansion_of_normalized_black_threshold + asymptotic_expansion_accuracy_threshold):
        return _asymptotic_expansion_of_normalized_black_call(x / s, 0.5 * s)
    if 0.5 * s < small_t_expansion_of_normalized_black_threshold:
        return _small_t_expansion_of_normalized_black_call(x / s, 0.5 * s)
    if x + 0.5 * s * s > s * 0.85:
        return _normalized_black_call_using_norm_cdf(x, s)
    return _normalised_black_call_using_erfcx(x / s, 0.5 * s)


def normalised_black(x, s, q):
    return normalised_black_call(-x if q < 0 else x, s)


def black(F, K, sigma, T, q):
    intrinsic = fabs(max((K - F if q < 0 else F - K), 0.0))
    # Map in-the-money to out-of-the-money
    if q * (F - K) > 0:
        return intrinsic + black(F, K, sigma, T, -q)
    return max(intrinsic, (sqrt(F) * sqrt(K)) * normalised_black(log(F / K), sigma * sqrt(T), q))
