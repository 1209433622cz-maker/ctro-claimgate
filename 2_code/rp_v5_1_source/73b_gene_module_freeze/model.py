"""RP V5.1 gene-to-module generator and explicit paired target-aware inference.

Continuous expression, not UMI counts. No study data are downloaded or edited.
"""
import hashlib
import json
import math
from pathlib import Path
from functools import lru_cache

import numpy as np

from numerics import bh_adjust, welch_one

VERSION = 'CTRO_GENE_MODULE_V1'
SIZES = [5, 11, 16, 17]
TARGETS = ['theta_D_full', 'theta_D_observed', 'theta_C_observed']
METHODS = ['CELL_NAIVE_WELCH', 'DONOR_MEAN_WELCH']
ZERO_TOL = 1e-12


def stable_json(obj):
    return json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(',', ':'),
                      allow_nan=False).encode('utf-8')


def rng_for(master, scenario_id, replicate, stream):
    digest = hashlib.sha256(scenario_id.encode('utf-8')).digest()
    words = [int.from_bytes(digest[i:i+4], 'little') for i in [0, 4, 8, 12]]
    seq = np.random.SeedSequence([int(master), *words, int(replicate), int(stream)])
    return np.random.Generator(np.random.PCG64(seq))


def noise(rng, shape, family):
    if family == 'gaussian':
        return rng.normal(size=shape)
    if family == 'unit_variance_laplace':
        return rng.laplace(scale=1/math.sqrt(2), size=shape)
    raise ValueError('UNKNOWN_NOISE')


def membership(scenario, rng):
    if scenario['module_sizes'] != SIZES:
        raise ValueError('CHANGED_MODULE_SIZES')
    full, observed = [], []
    offset = 0
    for k in SIZES:
        ids = np.arange(offset, offset+k)
        full.append(ids.tolist())
        if scenario['coverage'] == 'full':
            observed.append(ids.tolist())
        elif scenario['coverage'] == 'ceil_0.6K':
            observed.append(sorted(rng.choice(ids, math.ceil(.6*k), replace=False).tolist()))
        else:
            raise ValueError('UNKNOWN_COVERAGE')
        offset += k
    return full, observed


def effect_vectors(s, full):
    direct, background = np.zeros(sum(SIZES)), np.zeros(sum(SIZES))
    if s['signal_structure'] == 'uniform':
        direct[full[0]] = s['delta']
    elif s['signal_structure'] == 'sparse_floor_half':
        members = full[0][:SIZES[0]//2]
        direct[members] = s['delta']*SIZES[0]/len(members)
    else:
        raise ValueError('UNKNOWN_SIGNAL_STRUCTURE')
    if s['background_overlap'] == 'floor_0.25K':
        for ids in full:
            background[ids[:len(ids)//4]] = s['background_effect']
    elif s['background_overlap'] != 'none':
        raise ValueError('UNKNOWN_BACKGROUND')
    return direct, background


def population_cell_shift(s):
    if s['cell_number_rule'] == 'informative_reverse_mapping':
        return 2*math.sqrt(s['rho'])*math.sqrt(1.5)*75/105
    return 0.


def donor_and_counts(s, u_rng, n_rng):
    n = s['n_per_group']
    if s['block'] == 'C':
        classes = u_rng.integers(0, 3, size=2*n)
        u = (classes-1)*math.sqrt(1.5)
        if s['cell_number_rule'] == 'informative_reverse_mapping':
            sizes = np.array([5, 20, 80])
            counts = np.r_[sizes[::-1][classes[:n]], sizes[classes[n:]]]
        elif s['cell_number_rule'] == 'independent_discrete':
            counts = n_rng.choice([5, 20, 80], size=2*n)
        else:
            raise ValueError('UNKNOWN_C_COUNT_RULE')
    else:
        u = noise(u_rng, 2*n, s['noise'])
        if s['layout'] == 'equal20':
            one = np.full(n, 20)
        elif s['layout'] == 'cycle5_20_80':
            one = np.resize(np.array([5, 20, 80]), n)
        else:
            raise ValueError('UNKNOWN_LAYOUT')
        counts = np.r_[one, one]
    return u, counts.astype(int)


def score_expression(x, observed):
    if any(not ids for ids in observed):
        raise ValueError('EMPTY_OBSERVED_MODULE')
    if any(len(ids) != len(set(ids)) for ids in observed):
        raise ValueError('DUPLICATE_OBSERVED_MEMBER')
    return np.column_stack([x[:, ids].mean(axis=1) for ids in observed])


def aggregate_donors(scores, counts):
    cuts = np.r_[0, np.cumsum(counts)]
    if int(cuts[-1]) != len(scores) or any(int(n) <= 0 for n in counts):
        raise ValueError('COUNT_SCORE_CONTRACT')
    return np.vstack([scores[a:b].mean(axis=0) for a, b in zip(cuts[:-1], cuts[1:])])


def generate(s, replicate, master):
    n, rho, gamma = s['n_per_group'], s['rho'], s['gamma']
    if n < 2 or rho < 0 or gamma < 0 or rho+gamma >= 1:
        raise ValueError('INVALID_MODEL_VARIANCE_OR_N')
    full, observed = membership(s, rng_for(master, s['scenario_id'], replicate, 0))
    direct, background = effect_vectors(s, full)
    beta = direct+background
    u, counts = donor_and_counts(s, rng_for(master, s['scenario_id'], replicate, 1),
                                rng_for(master, s['scenario_id'], replicate, 2))
    expr_rng = rng_for(master, s['scenario_id'], replicate, 3)
    x = np.empty((int(counts.sum()), sum(SIZES)), dtype=np.float64)
    cursor = 0
    for d, count in enumerate(counts):
        v = noise(expr_rng, (int(count), 1), s['noise'])
        e = noise(expr_rng, (int(count), sum(SIZES)), s['noise'])
        x[cursor:cursor+count] = ((d >= n)*beta + math.sqrt(rho)*u[d]
                               + math.sqrt(gamma)*v + math.sqrt(1-rho-gamma)*e)
        cursor += count
    scores = score_expression(x, observed)
    donor_scores = aggregate_donors(scores, counts)
    d_full = np.array([beta[ids].mean() for ids in full])
    d_obs = np.array([beta[ids].mean() for ids in observed])
    c_obs = d_obs+population_cell_shift(s)
    truth = dict(theta_D_full=d_full.tolist(), theta_D_observed=d_obs.tolist(),
                 theta_C_observed=c_obs.tolist(), target_drift=(d_obs-d_full).tolist(),
                 direct_full=[float(direct[ids].mean()) for ids in full],
                 background_full=[float(background[ids].mean()) for ids in full],
                 direct_observed=[float(direct[ids].mean()) for ids in observed],
                 background_observed=[float(background[ids].mean()) for ids in observed],
                 population_cell_weight_shift=population_cell_shift(s),
                 population_cell_target_not_finite_n_unbiasedness=True)
    truth['theta_C_finite_n_estimator_expectation'] = (d_obs +
        2*math.sqrt(rho)*finite_c_ratio_expectation(n, True)
        if s['cell_number_rule'] == 'informative_reverse_mapping' else d_obs).tolist()
    meta = dict(generator=VERSION, scenario_id=s['scenario_id'], replicate=replicate,
                master_seed=int(master), counts=counts.tolist(), donor_u=u.tolist(),
                condition=['CONTROL']*n+['CASE']*n,
                full_members=full, observed_members=observed, beta=beta.tolist(),
                beta_direct=direct.tolist(), beta_background=background.tolist(),
                observed_K=[len(ids) for ids in observed],
                coverage_fraction=[len(ids)/k for ids, k in zip(observed, SIZES)], truth=truth)
    meta['mask_id'] = hashlib.sha256(stable_json(observed)).hexdigest()
    h = hashlib.sha256(stable_json(meta))
    h.update(x.astype('<f8', copy=False).tobytes(order='C'))
    meta['input_sha256'] = h.hexdigest()
    return dict(meta=meta, expression=x, cell_scores=scores, donor_scores=donor_scores)


def analyze(instance, scenario):
    m = instance['meta']
    n = scenario['n_per_group']
    split = sum(m['counts'][:n])
    methods = {}
    for name, scores, pos, target_name in [
        ('CELL_NAIVE_WELCH', instance['cell_scores'], split, 'theta_C_observed'),
        ('DONOR_MEAN_WELCH', instance['donor_scores'], n, 'theta_D_observed')]:
        modules = [welch_one(scores[pos:, j], scores[:pos, j]) for j in range(4)]
        all_ok = all(r['status'] == 'OK' for r in modules)
        q = bh_adjust([r['p'] for r in modules]) if all_ok else [None]*4
        nulls = [abs(v) <= ZERO_TOL for v in m['truth'][target_name]]
        for j, r in enumerate(modules):
            r['module_id'] = f'M{j+1}'
            r['matching_target'] = target_name
            r['matching_truth_is_null'] = nulls[j]
            r['q'] = q[j]
            r['bh_rejected'] = q[j] <= .05 if all_ok else None
            if r['status'] == 'OK':
                r['reject_zero'] = r['p'] < .05
                r['coverage'] = {t: r['ci_low'] <= m['truth'][t][j] <= r['ci_high'] for t in TARGETS}
                r['error'] = {t: r['estimate']-m['truth'][t][j] for t in TARGETS}
            else:
                r['reject_zero'] = None
                r['coverage'] = {t: None for t in TARGETS}
                r['error'] = {t: None for t in TARGETS}
        if all_ok:
            r_count = sum(r['bh_rejected'] for r in modules)
            false_count = sum(r['bh_rejected'] and nulls[j] for j, r in enumerate(modules))
            fdp = false_count/max(r_count, 1)
        else:
            r_count, false_count, fdp = None, None, None
        methods[name] = dict(input_sha256=m['input_sha256'], matching_target=target_name,
            modules=modules, family_status='OK' if all_ok else 'FAILED',
            bh_discoveries=r_count, bh_false_discoveries=false_count, fdp=fdp)
    return dict(scenario_id=scenario['scenario_id'], block=scenario['block'],
                replicate=m['replicate'], generator=VERSION, metadata=m, methods=methods)


def donor_variance(rho, gamma, k, count):
    return rho+(gamma+(1-rho-gamma)/k)/count


@lru_cache(maxsize=16)
def finite_c_ratio_expectation(n, informative):
    """Exact multinomial composition sum for E(sum NU / sum N), case arm."""
    if not informative:
        return 0.
    ans = 0.
    u = np.array([-1., 0., 1.])*math.sqrt(1.5)
    counts = np.array([5., 20., 80.])
    for a in range(n+1):
        for b in range(n-a+1):
            c = n-a-b
            multiplicity = math.factorial(n)//(math.factorial(a)*math.factorial(b)*math.factorial(c))
            composition = np.array([a, b, c])
            ratio = float(np.sum(composition*counts*u)/np.sum(composition*counts))
            ans += multiplicity/(3**n)*ratio
    return ans
