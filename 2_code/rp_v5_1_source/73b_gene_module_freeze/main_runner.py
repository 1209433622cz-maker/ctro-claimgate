"""Frozen main experiment runner with immutable, resumable 250-record chunks.

No main run is performed at import, QA, freeze or release. Explicit --all or
--scenario is required, and frozen dependencies must pass before observations.
"""
import argparse
import gzip
import hashlib
import json
import math
import sys
import time
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np

from model import METHODS, TARGETS, analyze, generate, stable_json

ROOT = Path('H:/SCI2/Centrosome')
ADMIN = ROOT/'0_admin/research_plan/rp_v5_1_main'
MAIN = ROOT/'3_results/74_gene_module_main'


def digest(b):
    return hashlib.sha256(b).hexdigest()


def file_sha(p):
    h = hashlib.sha256()
    with p.open('rb') as f:
        for b in iter(lambda: f.read(4*1024*1024), b''):
            h.update(b)
    return h.hexdigest()


def exclusive(p, b):
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open('xb') as f:
        f.write(b)
        f.flush()


class Moment:
    def __init__(self):
        self.n, self.mean, self.M2 = 0, 0., 0.

    def add(self, v):
        if not math.isfinite(v):
            raise ValueError('NONFINITE_SUMMARY_CONTRIBUTION')
        self.n += 1
        delta = v-self.mean
        self.mean += delta/self.n
        self.M2 += delta*(v-self.mean)

    def result(self):
        return dict(n=self.n, mean=self.mean if self.n else None,
                    mcse=math.sqrt(max(0., self.M2)/(self.n-1)/self.n) if self.n > 1 else None)


def wilson(k, n):
    if not n:
        return None
    z, p = 1.9599639845400536, k/n
    den = 1+z*z/n
    center = (p+z*z/(2*n))/den
    half = z*math.sqrt(p*(1-p)/n+z*z/(4*n*n))/den
    return [center-half, center+half]


def binary_result(moment):
    row = moment.result()
    n, p = row['n'], row['mean']
    row['mcse'] = math.sqrt(p*(1-p)/n) if n else None
    row['wilson95'] = wilson(round(p*n), n) if n else None
    row['applicability'] = 'APPLICABLE' if n else 'NOT_APPLICABLE_NO_ELIGIBLE_VALID_REPLICATES'
    return row


class Summary:
    """All labels explicit; FDP MCSE uses replicate variance, not binomial."""
    def __init__(self):
        self.generated = 0
        self.rows = defaultdict(lambda: dict(valid=0, failed=0, failures=Counter(),
            coverage=Moment(), error=Moment(), squared_error=Moment(), length=Moment(),
            reject=Moment(), null_reject=Moment(), alt_reject=Moment(), sign=Moment()))
        self.families = {m: dict(fdp=Moment(), failed=0, failures=Counter()) for m in METHODS}
        self.pairs = defaultdict(lambda: dict(coverage_difference=Moment(), ci_length_difference=Moment()))
        self.mask_counts = Counter()

    def add(self, r):
        self.generated += 1
        truth = r['metadata']['truth']
        for j, members in enumerate(r['metadata']['observed_members']):
            self.mask_counts[(j, tuple(members))] += 1
        for name, method in r['methods'].items():
            family = self.families[name]
            if method['family_status'] == 'OK':
                family['fdp'].add(method['fdp'])
            else:
                family['failed'] += 1
            for j, module in enumerate(method['modules']):
                for target in TARGETS:
                    row = self.rows[(name, j, target)]
                    if module['status'] != 'OK':
                        row['failed'] += 1
                        row['failures'][module['reason']] += 1
                        continue
                    row['valid'] += 1
                    row['coverage'].add(float(module['coverage'][target]))
                    row['error'].add(module['error'][target])
                    row['squared_error'].add(module['error'][target]**2)
                    row['length'].add(module['ci_high']-module['ci_low'])
                    row['reject'].add(float(module['reject_zero']))
                    matching = module['matching_target']
                    if module['matching_truth_is_null']:
                        row['null_reject'].add(float(module['reject_zero']))
                    else:
                        row['alt_reject'].add(float(module['reject_zero']))
                    if abs(truth[target][j]) > 1e-12:
                        row['sign'].add(float(module['estimate']*truth[target][j] > 0))
        for j in range(4):
            first, second = [r['methods'][m]['modules'][j] for m in METHODS]
            if first['status'] == second['status'] == 'OK':
                for target in TARGETS:
                    pair = self.pairs[(j, target)]
                    pair['coverage_difference'].add(float(first['coverage'][target])-float(second['coverage'][target]))
                    pair['ci_length_difference'].add((first['ci_high']-first['ci_low']) -
                                                    (second['ci_high']-second['ci_low']))

    def result(self, scenario_id):
        rows = []
        for (name, j, target), r in sorted(self.rows.items()):
            n = r['valid']
            squared = r['squared_error'].result()
            rmse = math.sqrt(max(0., squared['mean'])) if n else None
            squared_mcse = squared['mcse']
            rmse_mcse = squared_mcse/(2*rmse) if rmse and squared_mcse is not None else None
            cover = binary_result(r['coverage'])
            rows.append(dict(scenario_id=scenario_id, method=name, module_id=f'M{j+1}',
                target=target, n_generated=self.generated, n_valid=n, n_failed=r['failed'],
                failure_fraction=r['failed']/self.generated, failure_reasons=dict(r['failures']),
                coverage=cover, bias=r['error'].result(), rmse=rmse,
                rmse_mcse_delta_method=rmse_mcse, mean_squared_error=squared,
                ci_length=r['length'].result(), sign_correct=binary_result(r['sign']),
                rejection_matching_target=binary_result(r['reject']),
                type_I_error_matching_target=binary_result(r['null_reject']),
                power_matching_target=binary_result(r['alt_reject']),
                rejection_fields_repeated_across_target_rows_not_independent=True))
        families = []
        for name, r in self.families.items():
            families.append(dict(scenario_id=scenario_id, method=name, n_generated=self.generated,
                n_valid=r['fdp'].n, n_failed=r['failed'], fdr=r['fdp'].result(),
                conditional_on_successful_family=True, failure_fraction=r['failed']/self.generated,
                family='FOUR_MODULES_MATCHING_METHOD_OBSERVED_TARGET'))
        pairs = [dict(scenario_id=scenario_id, module_id=f'M{j+1}', target=t,
            difference_direction='CELL_NAIVE_MINUS_DONOR_MEAN',
            **{name: value.result() for name, value in rows.items()})
            for (j, t), rows in sorted(self.pairs.items())]
        masks = [dict(module_id=f'M{j+1}', observed_members=list(ids), replicates=count)
                 for (j, ids), count in sorted(self.mask_counts.items())]
        return dict(scenario_id=scenario_id, generated=self.generated, rows=rows,
                    families=families, paired_metrics=pairs, mask_distribution=masks,
                    conditional_mask_method_performance='DERIVABLE_FROM_FULL_RECORDS_NOT_ESTIMATED_FROM_SINGLETON_MASKS')


def validate_chunk(path, receipt, scenario, config):
    if not path.exists() or not receipt.exists():
        raise RuntimeError('ORPHAN_OR_INCOMPLETE_CHUNK_DO_NOT_OVERWRITE: '+str(path))
    meta = json.loads(receipt.read_text(encoding='utf-8'))
    expected_name = f"replicates_{meta['start']:05d}_{meta['end']:05d}.ndjson.gz"
    if path.name != expected_name or not (0 <= meta['start'] < meta['end'] <= config['replicates_per_scenario']):
        raise RuntimeError('CHUNK_RANGE_CONFLICT')
    if meta['sha256'] != file_sha(path) or meta['config_sha256'] != config['config_sha256']:
        raise RuntimeError('CHUNK_IDENTITY_CONFLICT: '+str(path))
    records = [json.loads(line) for line in gzip.decompress(path.read_bytes()).splitlines()]
    assert len(records) == meta['end']-meta['start']
    for i, r in enumerate(records, meta['start']):
        assert r['replicate'] == i and r['scenario_id'] == scenario['scenario_id']
        assert r['metadata']['master_seed'] == config['master_seed']
        assert len({m['input_sha256'] for m in r['methods'].values()}) == 1
    return records


def run_scenario(s, config, destination):
    folder = destination/s['scenario_id']
    folder.mkdir(parents=True, exist_ok=True)
    summary = Summary()
    for start in range(0, config['replicates_per_scenario'], config['chunk_replicates']):
        end = min(start+config['chunk_replicates'], config['replicates_per_scenario'])
        file = folder/f'replicates_{start:05d}_{end:05d}.ndjson.gz'
        receipt = file.with_suffix(file.suffix+'.receipt.json')
        if file.exists() or receipt.exists():
            records = validate_chunk(file, receipt, s, config)
        else:
            tick = time.perf_counter()
            records = []
            for i in range(start, end):
                one_tick = time.perf_counter()
                instance = generate(s, i, config['master_seed'])
                row = analyze(instance, s)
                row['runtime_seconds_generation_and_inference'] = time.perf_counter()-one_tick
                row['frozen_config_sha256'] = config['config_sha256']
                records.append(row)
            blob = gzip.compress(b'\n'.join(stable_json(r) for r in records)+b'\n', compresslevel=6, mtime=0)
            exclusive(file, blob)
            exclusive(receipt, stable_json(dict(scenario_id=s['scenario_id'], start=start, end=end,
                sha256=digest(blob), bytes=len(blob), config_sha256=config['config_sha256'],
                elapsed_seconds=time.perf_counter()-tick)))
            records = validate_chunk(file, receipt, s, config)
        for record in records:
            summary.add(record)
        print(json.dumps(dict(scenario_id=s['scenario_id'], completed_replicates=end,
                              target=config['replicates_per_scenario'])), flush=True)
    result = summary.result(s['scenario_id'])
    assert result['generated'] == config['replicates_per_scenario']
    result['config_sha256'] = config['config_sha256']
    body = stable_json(result)+b'\n'
    final = folder/'SCENARIO_SUMMARY.json'
    if final.exists():
        if final.read_bytes() != body:
            raise RuntimeError('SUMMARY_CONFLICT_DO_NOT_OVERWRITE')
    else:
        exclusive(final, body)
    return result


def frozen_config():
    path = ADMIN/'FROZEN_MAIN_CONFIG.json'
    freeze = json.loads((ADMIN/'MAIN_PRE_OUTCOME_FREEZE.json').read_text(encoding='utf-8'))
    for r in freeze['sources']:
        p = ROOT/r['path']
        if not p.is_file() or p.stat().st_size != r['bytes'] or file_sha(p) != r['sha256']:
            raise RuntimeError('FROZEN_SOURCE_CHANGED: '+r['path'])
    config = json.loads(path.read_text(encoding='utf-8'))
    if sys.version != config['environment']['python'] or np.__version__ != config['environment']['numpy']:
        raise RuntimeError('RUNTIME_CHANGED_REQUIRES_DOCUMENTED_REVIEW')
    config['config_sha256'] = file_sha(path)
    return config


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    choice = parser.add_mutually_exclusive_group(required=True)
    choice.add_argument('--all', action='store_true')
    choice.add_argument('--scenario')
    args = parser.parse_args()
    config = frozen_config()
    available = config['scenarios']
    if args.scenario:
        available = [s for s in available if s['scenario_id'] == args.scenario]
        if not available:
            raise ValueError('UNKNOWN_FROZEN_SCENARIO')
    for s in available:
        run_scenario(s, config, MAIN)
