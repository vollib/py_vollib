# -*- coding: utf-8 -*-

"""
py_vollib.helpers.distributions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A library for option pricing, implied volatility, and
greek calculation.  py_vollib is based on lets_be_rational,
a Python wrapper for LetsBeRational by Peter Jaeckel as
described below.

:copyright: © 2017 Gammon Capital LLC
:license: MIT, see LICENSE for more details.

About LetsBeRational:
~~~~~~~~~~~~~~~~~~~~~

The source code of LetsBeRational resides at www.jaeckel.org/LetsBeRational.7z .

======================================================================================
Copyright © 2013-2014 Peter Jäckel.

Permission to use, copy, modify, and distribute this software is freely granted,
provided that this notice is preserved.

WARRANTY DISCLAIMER
The Software is provided "as is" without warranty of any kind, either express or implied,
including without limitation any implied warranties of condition, uninterrupted use,
merchantability, fitness for a particular purpose, or non-infringement.
======================================================================================
"""


# -----------------------------------------------------------------------------
# IMPORTS

# Standard library imports
from __future__ import division
import math

# Related third party imports
import numpy

# Local application/library specific imports


def CND(x):
    y = numpy.abs(x)
    if y > 37.:
        CND = 0
    else:
        Exponential = numpy.exp(-y ** 2 / 2.)
        if y < 7.07106781186547:
            SumA = 3.52624965998911E-02 * y + 0.700383064443688
            SumA = SumA * y + 6.37396220353165
            SumA = SumA * y + 33.912866078383
            SumA = SumA * y + 112.079291497871
            SumA = SumA * y + 221.213596169931
            SumA = SumA * y + 220.206867912376
            SumB = 8.83883476483184E-02 * y + 1.75566716318264
            SumB = SumB * y + 16.064177579207
            SumB = SumB * y + 86.7807322029461
            SumB = SumB * y + 296.564248779674
            SumB = SumB * y + 637.333633378831
            SumB = SumB * y + 793.826512519948
            SumB = SumB * y + 440.413735824752
            CND = Exponential * SumA / SumB
        else:
            SumA = y + 0.65
            SumA = y + 4. / SumA
            SumA = y + 3. / SumA
            SumA = y + 2. / SumA
            SumA = y + 1. / SumA
            CND = Exponential / (SumA * 2.506628274631)

    CND = 1 - CND if x > 0 else CND

    return CND


def CBND(x, y, rho):
    '''
    '     A function for computing bivariate normal probabilities.
    '
    '       Alan Genz
    '       Department of Mathematics
    '       Washington State University
    '       Pullman, WA 99164-3113
    '       Email : alangenz@wsu.edu
    '
    '    This function is based on the method described by
    '        Drezner, Z and G.O. Wesolowsky, (1990),
    '        On the computation of the bivariate normal integral,
    '        Journal of Statist. Comput. Simul. 35, pp. 101-107,
    '    with major modifications for double precision, and for |R| close to 1.
    '   This code was originally transelated into VBA by Graeme West
    '''

    W  = numpy.zeros((11,4))
    XX = numpy.zeros((11,4))

    W[1][1] = 0.17132449237917
    XX[1][1] = -0.932469514203152

    W[2][1] = 0.360761573048138
    XX[2][1] = -0.661209386466265

    W[3][1] = 0.46791393457269
    XX[3][1] = -0.238619186083197

    W[1][2] = 4.71753363865118E-02
    XX[1][2] = -0.981560634246719

    W[2][2] = 0.106939325995318
    XX[2][2] = -0.904117256370475

    W[3][2] = 0.160078328543346
    XX[3][2] = -0.769902674194305

    W[4][2] = 0.203167426723066
    XX[4][2] = -0.587317954286617

    W[5][2] = 0.233492536538355
    XX[5][2] = -0.36783149899818

    W[6][2] = 0.249147045813403
    XX[6][2] = -0.125233408511469

    W[1][3] = 1.76140071391521E-02
    XX[1][3] = -0.993128599185095
    W[2][3] = 4.06014298003869E-02
    XX[2][3] = -0.963971927277914
    W[3][3] = 6.26720483341091E-02
    XX[3][3] = -0.912234428251326

    W[4][3] = 8.32767415767048E-02
    XX[4][3] = -0.839116971822219

    W[5][3] = 0.10193011981724
    XX[5][3] = -0.746331906460151

    W[6][3] = 0.118194531961518
    XX[6][3] = -0.636053680726515

    W[7][3] = 0.131688638449177
    XX[7][3] = -0.510867001950827

    W[8][3] = 0.142096109318382
    XX[8][3] = -0.37370608871542

    W[9][3] = 0.149172986472604
    XX[9][3] = -0.227785851141645

    W[10][3] = 0.152753387130726
    XX[10][3] = -7.65265211334973E-02

    if numpy.abs(rho) < 0.3:
        NG = 1
        LG = 3
    elif numpy.abs(rho) < 0.75:
        NG = 2
        LG = 6
    else:
        NG = 3
        LG = 10

    h = -x
    k = -y
    hk = h * k
    BVN = 0

    if numpy.abs(rho) < 0.925:
        if numpy.abs(rho) > 0:
            hs = (h * h + k * k) / 2.
            asr = math.asin(rho)
            for i in range(1,LG+1):
                for ISs in [-1,1]:
                    sn = math.sin(asr * (ISs * XX[i][NG] + 1) / 2)
                BVN = BVN + W[i][NG] * numpy.exp((sn * hk - hs) / (1 - sn * sn))
            BVN = BVN * asr / (4. * numpy.pi)
        BVN = BVN + CND(-h) * CND(-k)
    else:
        if rho < 0:
            k = -k
            hk = -hk

        if numpy.abs(rho) < 1.:
            Ass = (1. - rho) * (1. + rho)
            A = numpy.sqrt(Ass)
            bs = (h - k) ** 2
            c = (4. - hk) / 8.
            d = (12. - hk) / 16.
            asr = -(bs / Ass + hk) / 2.
            if asr > -100:
                BVN = A * numpy.exp(asr) * (1 - c * (bs - Ass) * (1 - d * bs / 5.) / 3. + c * d * Ass * Ass / 5.)
        if -hk < 100:
            b = numpy.sqrt(bs)
            BVN = BVN - numpy.exp(-hk / 2.) * numpy.sqrt(2. * numpy.pi) * CND(-b / A) * b * (1. - c * bs * (1. - d * bs / 5.) / 3.)

        A = A / 2
        for i in range(1,LG+1):
            for ISs in [-1,1]:
                xs = (A * (ISs * XX[i][NG] + 1)) ** 2
                rs = numpy.sqrt(1 - xs)
                asr = -(bs / xs + hk) / 2
                if asr > -100:
                    BVN = BVN + A * W(i, NG) * numpy.exp(asr) * (numpy.exp(-hk * (1 - rs) / (2 * (1 + rs))) / rs - (1 + c * xs * (1 + d * xs)))

        BVN = -BVN / (2. * numpy.pi)

        if rho > 0.:
            BVN = BVN + CND(-max(h, k))
        else:
            BVN = -BVN
            if k > h:
                BVN = BVN + CND(k) - CND(h)

    CBND = BVN

    return CBND


if __name__ == "__main__":
    from py_vollib.helpers.doctest_helper import run_doctest
    run_doctest()
