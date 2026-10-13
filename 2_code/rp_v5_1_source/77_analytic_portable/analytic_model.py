"""Post-main deterministic derivations for the unchanged continuous generator.

No new Monte Carlo sample, corrected interval, patient analysis or source edits.
"""
import hashlib
import itertools
import json
import math
import sys
from collections import Counter
from fractions import Fraction as F
from pathlib import Path
import numpy as np

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'2_code/73b_gene_module_freeze'))
import model


def read(p):return json.loads(p.read_text(encoding='utf-8'))
def dump(p,v):
    p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(v,ensure_ascii=False,indent=2,allow_nan=False)+'\n',encoding='utf-8',newline='\n')


def coefficients(s):
    beta=[F(0)]*49;offset=0
    for j,k in enumerate([5,11,16,17]):
        if j==0:
            affected=k if s['signal_structure']=='uniform' else k//2
            for i in range(affected):beta[offset+i]=F(str(s['delta']))*k/affected
        if s['background_overlap']=='floor_0.25K':
            for i in range(k//4):beta[offset+i]+=F(str(s['background_effect']))
        offset+=k
    return beta


def membership_variance(beta,m):
    k=len(beta);mean=sum(beta,F(0))/k
    sample_var=sum(((x-mean)**2 for x in beta),F(0))/(k-1)
    return (1-F(m,k))*sample_var/m


def noise_variance(rho,gamma,m,counts):
    nu=gamma+(1-rho-gamma)/m;n=len(counts)//2
    return sum((rho+nu/count for count in counts),F(0))/(n*n)


def covariance_path(rho,gamma,m,counts):
    n=len(counts)//2;answer=0.
    for count in counts:
        # Direct cell-score covariance quadratic form; no call to donor_variance.
        cov=np.full((count,count),float(rho))+np.eye(count)*float(gamma+(1-rho-gamma)/m)
        weights=np.full(count,1/(n*count))
        answer+=float(weights@cov@weights)
    return answer


def c_composition(n,reverse=False):
    # Exact rational ratio for unscaled states -1/0/1; factorial route.
    sizes=[80,20,5] if reverse else [5,20,80];answer=F(0);mass=0
    for a in range(n+1):
        for b in range(n-a+1):
            c=n-a-b;mult=math.factorial(n)//(math.factorial(a)*math.factorial(b)*math.factorial(c))
            answer+=F(mult,3**n)*F(-a*sizes[0]+c*sizes[2],a*sizes[0]+b*sizes[1]+c*sizes[2])
            mass+=mult
    assert mass==3**n
    return answer


def c_convolution(n,reverse=False):
    # Independent algorithm: ordered-draw integer convolution of (N, N*z).
    sizes=[80,20,5] if reverse else [5,20,80]
    distribution=Counter({(0,0):1})
    for _ in range(n):
        next_distribution=Counter()
        for (den,num),mult in distribution.items():
            for size,z in zip(sizes,[-1,0,1]):next_distribution[(den+size,num+size*z)]+=mult
        distribution=next_distribution
    assert sum(distribution.values())==3**n
    answer=sum((F(mult,3**n)*F(num,den) for (den,num),mult in distribution.items()),F(0))
    return answer,len(distribution)


def main(destination=None):
    out=Path(destination) if destination else ROOT/'3_results/77_analytic_portable'
    cfg=read(ROOT/'0_admin/research_plan/rp_v5_1_main/FROZEN_MAIN_CONFIG.json')
    lookup={(r['scenario_id'],r['method'],r['module_id'],r['target']):r for r in read(ROOT/'3_results/74_execution_audit/ALL_MAIN_TARGET_SUMMARIES.json')}
    sparse=next(s for s in cfg['scenarios'] if s['scenario_id']=='A126')
    beta=coefficients(sparse)[:5];m=3;masks=[];dist=Counter()
    for ids in itertools.combinations(range(5),m):
        truth=sum((beta[i] for i in ids),F(0))/m;dist[truth]+=1
        masks.append(dict(members=list(ids),target_fraction=str(truth),target=float(truth)))
    mean=sum((truth*count for truth,count in dist.items()),F(0))/10
    variance=sum(((truth-mean)**2*count for truth,count in dist.items()),F(0))/10
    assert mean==F(2,5) and variance==membership_variance(beta,m)==F(1,25)
    mask_result=dict(coefficients=[str(x) for x in beta],masks=masks,
        target_distribution=[dict(target_fraction=str(k),probability_fraction=str(F(v,10))) for k,v in sorted(dist.items())],
        mean_fraction=str(mean),mean=float(mean),variance_fraction=str(variance),variance=float(variance),
        finite_population_formula='(1-m/K)*S_beta_squared/m; S_beta_squared has denominator K-1',
        equal_mask_probability=True,mask_shared_across_donors=True,not_cross_K_experiment=True)
    rows=[];max_matrix_error=0.;max_helper_error=0.;mse_diagnostics=[]
    for s in cfg['scenarios']:
        if s['block']=='C':continue
        n=s['n_per_group'];counts=([20]*n if s['layout']=='equal20' else [5,20,80]*(n//3)+[5,20,80][:n%3])*2
        betas=coefficients(s);offset=0
        for j,k in enumerate([5,11,16,17]):
            m=k if s['coverage']=='full' else math.ceil(.6*k)
            rho,gamma=F(str(s['rho'])),F(str(s['gamma']))
            v=noise_variance(rho,gamma,m,counts);mask_v=membership_variance(betas[offset:offset+k],m)
            cov=covariance_path(rho,gamma,m,counts)
            helper=sum(model.donor_variance(float(rho),float(gamma),m,c) for c in counts)/(n*n)
            max_matrix_error=max(max_matrix_error,abs(float(v)-cov));max_helper_error=max(max_helper_error,abs(float(v)-helper))
            assert abs(float(v)-cov)<1e-12 and abs(float(v)-helper)<1e-12
            full=sum(betas[offset:offset+k],F(0))/k
            row=dict(scenario_id=s['scenario_id'],module_id=f'M{j+1}',full_members=k,observed_members=m,
                theta_D_full=float(full),noise_variance_fraction=str(v),noise_variance=float(v),
                mask_target_variance_fraction=str(mask_v),mask_target_variance=float(mask_v),
                full_target_total_variance_fraction=str(v+mask_v),full_target_total_variance=float(v+mask_v),
                unconditional_full_target_bias=0.,covariance_matrix_value=cov,
                scope='A_B_FIXED_COUNTS_INDEPENDENT_DONOR_STATES_ONLY_NOT_C')
            rows.append(row)
            for target,theory in [('theta_D_full',v+mask_v),('theta_D_observed',v)]:
                obs=lookup[(s['scenario_id'],'DONOR_MEAN_WELCH',f'M{j+1}',target)]['mean_squared_error']
                z=(obs['mean']-float(theory))/obs['mcse']
                mse_diagnostics.append(dict(scenario_id=s['scenario_id'],module_id=f'M{j+1}',target=target,
                    theoretical_mse=float(theory),existing_empirical_mse=obs,mc_standardized_difference=z,
                    descriptive_not_joint_pass_threshold=True))
            offset+=k
    c_rows=[]
    for n in [4,12]:
        case=c_composition(n);control=c_composition(n,True)
        dc,states=c_convolution(n);dr,_=c_convolution(n,True)
        assert case==dc and control==dr and control==-case
        pop_case=F(75,105);pop_control=-pop_case
        shift=math.sqrt(.6)*float(case-control);population=math.sqrt(.6)*float(pop_case-pop_control)
        helper=2*math.sqrt(.4)*model.finite_c_ratio_expectation(n,True)
        assert abs(shift-helper)<1e-12
        c_rows.append(dict(n_per_group=n,ordered_draws_per_arm=3**n,convolution_states=states,
            case_exact_unscaled_ratio_fraction=str(case),control_exact_unscaled_ratio_fraction=str(control),
            finite_n_shift=shift,population_shift=population,finite_minus_population=shift-population,
            production_helper_shift=helper,independent_algorithms='FACTORIAL_COMPOSITIONS_AND_INTEGER_CONVOLUTION',
            not_replacement_primary_estimand=True))
    assert abs(c_rows[0]['population_shift']-model.population_cell_shift(next(s for s in cfg['scenarios'] if s['scenario_id']=='C002')))<1e-12
    status=dict(status='EXACT_POST_MAIN_MODEL_EXPLANATION_CHECKED_NOT_COVERAGE_PROOF',mask_count=10,
        a_b_variance_rows=len(rows),existing_mse_comparison_rows=len(mse_diagnostics),
        maximum_covariance_error=max_matrix_error,maximum_frozen_helper_error=max_helper_error,
        c_expectation_rows=2,new_main_instances=0,
        max_abs_mse_mc_standardized_difference=max(abs(r['mc_standardized_difference']) for r in mse_diagnostics),
        no_requirement_all_rows_inside_individual_95_intervals=True,
        primary_results_unchanged=True,welch_coverage_analytically_proven=False)
    dump(out/'EXACT_MEMBERSHIP_TARGET_DISTRIBUTION.json',mask_result)
    dump(out/'ALL_640_FIXED_COUNT_VARIANCE_DECOMPOSITIONS.json',rows)
    dump(out/'ALL_1280_EXISTING_MSE_CORRESPONDENCE_DIAGNOSTICS.json',mse_diagnostics)
    dump(out/'EXACT_C_POPULATION_AND_FINITE_N_EXPECTATIONS.json',c_rows)
    dump(out/'ANALYTIC_STATUS.json',status)
    print(json.dumps(status,indent=2));return status


if __name__=='__main__':main()
