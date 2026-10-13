"""Offline Tier-A checks in an extracted package, without original workspace access.

Copies of model/numerics/plotting code remain byte-identical to their originals.
Explicit adapters only alter roots, guard scope and exclusion of patient work.
"""
import hashlib
import json
import math
import os
import platform
import sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
OUTPUT=ROOT/'reproduction_output'
OUTPUT.mkdir(parents=True,exist_ok=True)
os.environ['MPLCONFIGDIR']=str(OUTPUT/'matplotlib_cache')
os.environ['OPENBLAS_NUM_THREADS']='1'
os.environ['OMP_NUM_THREADS']='1'
FORBIDDEN_ORIGINAL='h:/sci2/centrosome'


def filesystem_network_boundary(event,args):
    if event in ['socket.connect','socket.getaddrinfo']:
        raise RuntimeError('NETWORK_NOT_ALLOWED_IN_PORTABLE_CHECK')
    if event in ['open','os.listdir','os.scandir'] and args and isinstance(args[0],(str,bytes,os.PathLike)):
        target=os.path.abspath(os.fsdecode(args[0])).replace('\\','/').lower()
        if target==FORBIDDEN_ORIGINAL or target.startswith(FORBIDDEN_ORIGINAL+'/'):
            raise RuntimeError('ORIGINAL_WORKSPACE_ACCESS_FORBIDDEN: '+target)


sys.addaudithook(filesystem_network_boundary)
sys.path.insert(0,str(ROOT/'2_code/73b_gene_module_freeze'))
sys.path.insert(0,str(ROOT/'2_code/75_verified_figures'))
sys.path.insert(0,str(ROOT/'2_code/77_analytic_portable'))
import numpy as np
import main_runner
import model
from analytic_model import main as analytic_main


def read(p):return json.loads(p.read_text(encoding='utf-8'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def dump(p,v):
    p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(v,ensure_ascii=False,indent=2,allow_nan=False)+'\n',encoding='utf-8',newline='\n')


def same(got,expected,tolerance=1e-10):
    if isinstance(expected,dict):
        assert set(got)==set(expected)
        for k,v in expected.items():same(got[k],v,tolerance)
    elif isinstance(expected,list):
        assert len(got)==len(expected)
        for g,e in zip(got,expected):same(g,e,tolerance)
    elif isinstance(expected,(str,bool,int)) or expected is None:assert got==expected
    else:assert math.isfinite(got) and abs(got-expected)<=tolerance*max(1,abs(expected)),(got,expected)


def package_config():
    cfg=read(ROOT/'0_admin/research_plan/rp_v5_1_main/FROZEN_MAIN_CONFIG.json')
    assert sys.version==cfg['environment']['python'] and np.__version__==cfg['environment']['numpy']
    cfg['config_sha256']=sha(ROOT/'0_admin/research_plan/rp_v5_1_main/FROZEN_MAIN_CONFIG.json')
    return cfg


def verify_payload(row):
    p=ROOT/row['path']
    assert p.stat().st_size==row['bytes'] and sha(p)==row['sha256'],row['path']


def negative_boundary_checks(row):
    checks=0
    for path in ['H:/SCI2/Centrosome/0_admin/ACTIVE_EXECUTION_CONTEXT.md',
                 'H:/SCI2/./Centrosome/0_admin/ACTIVE_EXECUTION_CONTEXT.md',
                 'H:/SCI2/Centrosome/../Centrosome/0_admin/ACTIVE_EXECUTION_CONTEXT.md']:
        try:sys.audit('open',path,'r',0)
        except RuntimeError as e:
            assert 'ORIGINAL_WORKSPACE_ACCESS_FORBIDDEN' in str(e);checks+=1
        else:raise AssertionError('WORKSPACE_BOUNDARY_NOT_ENFORCED')
    for event in ['socket.connect','socket.getaddrinfo']:
        try:sys.audit(event,None)
        except RuntimeError as e:
            assert 'NETWORK_NOT_ALLOWED' in str(e);checks+=1
        else:raise AssertionError('NETWORK_BOUNDARY_NOT_ENFORCED')
    for key,value in [('bytes',row['bytes']+1),('sha256','0'*64)]:
        bad=dict(row);bad[key]=value
        try:verify_payload(bad)
        except AssertionError:checks+=1
        else:raise AssertionError('SOURCE_MISMATCH_NOT_REJECTED')
    assert checks==7
    return checks


def synthetic_figures():
    import build_figures as bf
    bf.ROOT=ROOT;bf.AUDIT=ROOT/'3_results/74_execution_audit';bf.OUT=OUTPUT/'figure_metadata'
    bf.FIGURES=[];bf.USED={};bf.frozen_config=package_config
    source=Path(bf.__file__).read_text(encoding='utf-8')
    changes=[]
    for start,end,label in [
        ("    pbc_path=ROOT/'3_results/72_solo_local_execution/PBC_MODULE_RECONSTRUCTION_AND_SENSITIVITY.json'",'    # Full machine-readable tables;','OMIT_PATIENT_SETUP'),
        ('    # Figure1 is a computation/estimand schematic, never a causal pathway.','    # Figure2: exactly the eight pre-outcome null coordinates.','OMIT_OVERVIEW_WITH_PATIENT_ILLUSTRATION'),
        ('    # Previously observed PBC illustration, no new patient or gene selection.','    # Complete supplements use original catalog ordering, not outcome ranking.','OMIT_PATIENT_FIGURE4')]:
        assert source.count(start)==source.count(end)==1
        begin=source.index(start);finish=source.index(end,begin)
        removed=source[begin:finish];changes.append(dict(action=label,removed_text_sha256=hashlib.sha256(removed.encode()).hexdigest()))
        source=source[:begin]+source[finish:]
    # Actual display instructions for the seven synthetic figures are unchanged.
    source=source.replace('main_count=4,supplement_count=5','main_count=2,supplement_count=5')
    source=source.replace('dict(main_figures=4,supplement_figures=5','dict(main_figures=2,supplement_figures=5')
    start=source.index('def main():');end=source.index("if __name__=='__main__':main()",start)
    exec(compile(source[start:end],str(Path(bf.__file__))+'#synthetic_adapter','exec'),bf.__dict__)
    # main writes only under this extracted ROOT; no original guard or PBC input.
    bf.main()
    expected=read(ROOT/'CANONICAL_SYNTHETIC_FIGURE_BINDINGS.json')
    got={r['figure_id']:r for r in bf.FIGURES};matched=[]
    for row in expected:
        r=got[row['figure_id']]
        for key in ['png','svg']:assert r[key]['sha256']==row[key+'_sha256'],row['figure_id']+' '+key
        panels=read(ROOT/r['source']['path'])['panels'];same(panels,row['panels'],0.)
        matched.append(row['figure_id'])
    assert len(matched)==7
    dump(OUTPUT/'FIGURE_PORTABILITY_CHECK.json',dict(figures=matched,png_svg_byte_matches=14,panel_rows_unchanged=True,
        source_json_provenance_expected_to_differ=True,original_plotting_code_sha256=sha(Path(bf.__file__)),
        explicit_adapter_cuts=changes,old_workspace_or_patient_data_not_read=True))
    return len(matched)


def main():
    manifest=read(ROOT/'PORTABLE_PAYLOAD_MANIFEST.json')
    for r in manifest['payloads']:
        verify_payload(r)
    negative_checks=negative_boundary_checks(manifest['payloads'][0])
    cfg=package_config();by={s['scenario_id']:s for s in cfg['scenarios']}
    main_runner.ROOT=ROOT;main_runner.ADMIN=ROOT/'0_admin/research_plan/rp_v5_1_main'
    main_runner.MAIN=ROOT/'3_results/74_gene_module_main';main_runner.frozen_config=package_config
    references=read(ROOT/'REPLAY_REFERENCE_576_EXISTING_RECORDS.json')
    comparisons=0
    for reference in references:
        s=by[reference['scenario_id']]
        instance=model.generate(s,reference['replicate'],cfg['master_seed'])
        assert instance['meta']['input_sha256']==reference['metadata']['input_sha256']
        r=model.analyze(instance,s)
        same(r['metadata'],reference['metadata']);same(r['methods'],reference['methods'])
        comparisons+=1
    all_targets=[];all_fdr=[];all_pairs=[]
    for sid in by:
        summary=read(ROOT/f'3_results/74_gene_module_main/{sid}/SCENARIO_SUMMARY.json')
        assert summary['generated']==5000 and summary['config_sha256']==cfg['config_sha256']
        # The published aggregate export adds scenario_parameters. Reconstruct
        # that known annotation explicitly from the frozen catalog; do not drop
        # unknown fields or relax schema equality to conceal a mismatch.
        for rows in [summary['rows'],summary['families'],summary['paired_metrics']]:
            for row in rows:row['scenario_parameters']=by[sid]
        all_targets.extend(summary['rows']);all_fdr.extend(summary['families']);all_pairs.extend(summary['paired_metrics'])
    for values,name in [(all_targets,'ALL_MAIN_TARGET_SUMMARIES.json'),(all_fdr,'ALL_MAIN_FDR_SUMMARIES.json'),(all_pairs,'ALL_MAIN_PAIRED_SUMMARIES.json')]:
        master=read(ROOT/'3_results/74_execution_audit'/name)
        if name=='ALL_MAIN_TARGET_SUMMARIES.json':key=lambda r:(r['scenario_id'],r['method'],r['module_id'],r['target'])
        elif name=='ALL_MAIN_FDR_SUMMARIES.json':key=lambda r:(r['scenario_id'],r['method'])
        else:key=lambda r:(r['scenario_id'],r['module_id'],r['target'])
        same(sorted(values,key=key),sorted(master,key=key))
    analytical=analytic_main(OUTPUT/'analytical')
    figures=synthetic_figures()
    result=dict(status='PASS_PINNED_RUNTIME_OFFLINE_CLEAN_DIRECTORY_TIER_A',
        root=str(ROOT),python=sys.version,numpy=np.__version__,platform=platform.platform(),
        package_payloads_matched=len(manifest['payloads']),explicit_negative_boundary_tests=negative_checks,
        fixed_id_existing_replays=comparisons,
        new_scientific_instances=0,scenario_summary_records_read=192,
        target_rows=4608,fdr_rows=384,paired_rows=2304,reconstructed_synthetic_figures=figures,
        analytic_status=analytical,original_workspace_access_forbidden_by_audit_hook=True,
        network_access_forbidden_by_audit_hook=True,patient_input_files_included=False,
        all_960000_raw_records_rerun=False,cross_os_portability_tested=False,
        original_generator_independently_reimplemented=False,submission_ready=False)
    dump(OUTPUT/'PORTABLE_REPRODUCTION_RECEIPT.json',result)
    print(json.dumps(result,indent=2))


if __name__=='__main__':main()
