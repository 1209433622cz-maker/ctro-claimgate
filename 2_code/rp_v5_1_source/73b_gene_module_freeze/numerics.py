"""Float64 Student t tails/quantiles and Welch inference without SciPy.

Incomplete beta continued fraction: DLMF 8.17. Production quantiles use
bracketing/bisection. Independent density integration lives in qa_stage73b.py.
No normal approximation, rounded df lookup or silent convergence fallback.
"""
import math
import numpy as np

VERSION = 'CTRO_NUMERICS_V1'


def beta_fraction(a, b, x):
    qab, qap, qam = a + b, a + 1, a - 1
    c = 1.0
    d = 1.0 - qab * x / qap
    if abs(d) < 1e-300:
        d = 1e-300
    d = 1 / d
    h = d
    for m in range(1, 1001):
        aa = m * (b - m) * x / ((qam + 2*m) * (a + 2*m))
        d, c = 1 + aa*d, 1 + aa/c
        if abs(d) < 1e-300:
            d = 1e-300
        if abs(c) < 1e-300:
            c = 1e-300
        d = 1/d
        h *= d*c
        aa = -(a + m) * (qab + m) * x / ((a + 2*m) * (qap + 2*m))
        d, c = 1 + aa*d, 1 + aa/c
        if abs(d) < 1e-300:
            d = 1e-300
        if abs(c) < 1e-300:
            c = 1e-300
        d = 1/d
        change = d*c
        h *= change
        if abs(change - 1) <= 2e-14:
            return h
    raise ArithmeticError('BETA_FRACTION_NONCONVERGENCE')


def ibeta(a, b, x):
    if not (a > 0 and b > 0 and 0 <= x <= 1):
        raise ValueError('INVALID_BETA_ARGUMENT')
    if x == 0 or x == 1:
        return float(x)
    bt = math.exp(math.lgamma(a+b) - math.lgamma(a) - math.lgamma(b)
                  + a*math.log(x) + b*math.log1p(-x))
    if x < (a+1)/(a+b+2):
        ans = bt*beta_fraction(a, b, x)/a
    else:
        ans = 1 - bt*beta_fraction(b, a, 1-x)/b
    if not math.isfinite(ans) or ans < -1e-12 or ans > 1+1e-12:
        raise ArithmeticError('INVALID_BETA_RESULT')
    return min(1., max(0., ans))


def t_sf_positive(x, df):
    if not math.isfinite(df) or df <= 0 or x < 0 or not math.isfinite(x):
        raise ValueError('INVALID_T_ARGUMENT')
    if x == 0:
        return .5
    # Symmetry avoids loss of precision in the small tail.
    return .5 * ibeta(df/2, .5, df/(df+x*x))


def t_cdf(x, df):
    s = t_sf_positive(abs(x), df)
    return 1-s if x >= 0 else s


def t_quantile(p, df):
    if not (0 < p < 1) or not math.isfinite(df) or df <= 0:
        raise ValueError('INVALID_QUANTILE_ARGUMENT')
    if p == .5:
        return 0.
    tail = min(p, 1-p)
    lo, hi = 0., 1.
    for _ in range(100):
        if t_sf_positive(hi, df) <= tail:
            break
        hi *= 2
    else:
        raise ArithmeticError('QUANTILE_BRACKET_NONCONVERGENCE')
    for _ in range(100):
        mid = (lo+hi)/2
        if t_sf_positive(mid, df) > tail:
            lo = mid
        else:
            hi = mid
        if hi-lo <= 2e-11*max(1., abs(mid)):
            return (-1 if p < .5 else 1) * (lo+hi)/2
    raise ArithmeticError('QUANTILE_BISECTION_NONCONVERGENCE')


def bh_adjust(p):
    x = np.asarray(p, dtype=float)
    if not np.isfinite(x).all() or np.any((x < 0) | (x > 1)):
        raise ValueError('INVALID_BH_INPUT')
    order = np.argsort(x, kind='stable')
    raw = x[order]*len(x)/np.arange(1, len(x)+1)
    corrected = np.minimum.accumulate(raw[::-1])[::-1]
    ans = np.empty(len(x))
    ans[order] = np.minimum(corrected, 1.)
    return ans.tolist()


def welch_one(case, control):
    """Explicit status; a failed module never becomes a fabricated P-value."""
    try:
        a, b = np.asarray(case, dtype=float), np.asarray(control, dtype=float)
        if len(a) < 2 or len(b) < 2:
            raise ValueError('TOO_FEW_OBSERVATIONS')
        if not np.isfinite(a).all() or not np.isfinite(b).all():
            raise ValueError('NONFINITE_INPUT')
        estimate = float(a.mean() - b.mean())
        v1, v0 = float(a.var(ddof=1)/len(a)), float(b.var(ddof=1)/len(b))
        vv = v1+v0
        if vv <= 0 or not math.isfinite(vv):
            raise ValueError('ZERO_OR_INVALID_VARIANCE')
        se = math.sqrt(vv)
        df = vv*vv/(v1*v1/(len(a)-1) + v0*v0/(len(b)-1))
        if df <= 0 or not math.isfinite(df):
            raise ValueError('INVALID_WELCH_DF')
        p = 2*t_sf_positive(abs(estimate/se), df)
        critical = t_quantile(.975, df)
        low, high = estimate-critical*se, estimate+critical*se
        if not all(math.isfinite(x) for x in [low, high, p]):
            raise ArithmeticError('NONFINITE_INFERENCE')
        return dict(status='OK', estimate=estimate, se=se, df=df, p=p,
                    ci_low=low, ci_high=high, n_case=len(a), n_control=len(b))
    except (ArithmeticError, ValueError, OverflowError) as e:
        return dict(status='FAILED', reason=str(e), estimate=None, se=None, df=None,
                    p=None, ci_low=None, ci_high=None, n_case=len(case), n_control=len(control))
