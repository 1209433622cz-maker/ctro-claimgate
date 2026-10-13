"""Source-bound Stage75 figures; no simulation or frozen-source mutation.

All primary display coordinates are read from the original frozen rules.
Complete JSON supplements retain every scenario/method/module/target.
"""
import hashlib
import itertools
import json
import math
import sys
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
import numpy as np

ROOT = Path('H:/SCI2/Centrosome')
AUDIT = ROOT / '3_results/74_execution_audit'
OUT = ROOT / '3_results/75_verified_figures_and_manuscript'
sys.path.insert(0, str(ROOT / '2_code/73b_gene_module_freeze'))
from main_runner import frozen_config

COLORS = {'CELL_NAIVE_WELCH': '#D55E00', 'DONOR_MEAN_WELCH': '#0072B2'}
METHODS = list(COLORS)
SHORT = {METHODS[0]: 'Cell-level', METHODS[1]: 'Donor mean'}
MATCH = {METHODS[0]: 'theta_C_observed', METHODS[1]: 'theta_D_observed'}
TARGET_LABEL = {'theta_D_full': 'Full donor target', 'theta_D_observed': 'Observed donor target',
                'theta_C_observed': 'Population cell target'}
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':8.2,
    'axes.titlesize':9,'axes.labelsize':8.2,'xtick.labelsize':8,'ytick.labelsize':8,
    'legend.fontsize':8,'axes.spines.top':False,'axes.spines.right':False,
    'svg.fonttype':'none','svg.hashsalt':'CTRO_STAGE75_FIXED_DISPLAY_V1',
    'savefig.facecolor':'white','figure.facecolor':'white'})
WIDTH = 180 / 25.4
FIGURES = []
USED = {}


def sha(p):
    h=hashlib.sha256()
    with p.open('rb') as f:
        for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
    return h.hexdigest()


def rel(p): return p.relative_to(ROOT).as_posix()
def identity(p): return dict(path=rel(p),bytes=p.stat().st_size,sha256=sha(p))


def read(p):
    p=Path(p);USED[rel(p)]=identity(p)
    return json.loads(p.read_text(encoding='utf-8'))


def dump(p,v):
    p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(v,ensure_ascii=False,indent=2,allow_nan=False)+'\n',encoding='utf-8')


def label(s):
    noise='G' if s['noise']=='gaussian' else 'L'
    coverage='all' if s['coverage']=='full' else 'partial'
    if s['block']=='C':
        rule='info' if s['cell_number_rule']=='informative_reverse_mapping' else 'indep'
        return f"{s['scenario_id']} n{s['n_per_group']}/{rule}/{noise}"
    return f"{s['scenario_id']} n{s['n_per_group']}/r{s['rho']:g}/{coverage}/{noise}"


def style(ax,title,letter,ylabel=None):
    ax.set_title(title,loc='left',pad=10)
    ax.text(-.10,1.06,letter,transform=ax.transAxes,fontweight='bold',fontsize=11)
    if ylabel:ax.set_ylabel(ylabel)
    ax.grid(axis='y',color='#E6E6E6',linewidth=.55)
    ax.set_axisbelow(True)


def rate(ax,rows,metric,color,offset=0,marker='o',name=None,filled=True):
    summaries=[r[metric] for r in rows]
    means=np.array([r['mean'] for r in summaries],dtype=float)*100
    if metric=='fdr':
        e=np.array([1.96*r['mcse'] for r in summaries])*100
        low=np.maximum(0,means-e);high=np.minimum(100,means+e)
    else:
        low=np.array([r['wilson95'][0] for r in summaries])*100
        high=np.array([r['wilson95'][1] for r in summaries])*100
    ax.errorbar(np.arange(len(rows))+offset,means,yerr=[np.maximum(0,means-low),np.maximum(0,high-means)],
        fmt=marker,color=color,mfc=color if filled else 'white',ms=4.1,
        capsize=2,elinewidth=.8,label=name,zorder=3)
    ax.set_ylim(0,102)


def xticks(ax,scenes,every=1,ids_only=False):
    inds=np.arange(len(scenes))[::every]
    labels=[scenes[i]['scenario_id'] if ids_only else label(scenes[i]) for i in inds]
    ax.set_xticks(inds,labels,rotation=55,ha='right')
    ax.set_xlim(-.6,len(scenes)-.4)


def panel(pid,selection,rows,metric,target,rule=None,note=''):
    return dict(panel_id=pid,selection=selection,frozen_rule_id=rule,
        scenario_ids=sorted({r.get('scenario_id') for r in rows if r.get('scenario_id')}),
        module_ids=sorted({r.get('module_id') for r in rows if r.get('module_id')}),
        target=target,metric=metric,rows=rows,note=note,
        uncertainty='WILSON95_MC' if metric in ['coverage','type_I_error_matching_target','power_matching_target','rejection_matching_target']
        else 'MEAN_PLUS_MINUS_1.96_MCSE' if metric in ['fdr','estimate_mean']
        else 'DESCRIPTIVE_OR_ANALYTIC_NO_INFERENTIAL_INTERVAL')


def save(fig,fid,bucket,panels,role):
    kind='Stage75_Verified_Main' if fid.startswith('Figure') else 'Stage75_Complete_Supplement'
    base=ROOT / '4_figures' / bucket / kind / fid
    base.parent.mkdir(parents=True,exist_ok=True)
    fig.savefig(base.with_suffix('.png'),dpi=300)
    fig.savefig(base.with_suffix('.svg'),metadata={'Date':None,'Creator':'CTRO source-bound plotting code'})
    fig.canvas.draw()
    renderer=fig.canvas.get_renderer();width,height=fig.canvas.get_width_height()
    outside=[]
    hidden_ticks=set()
    for ax in fig.axes:
        if not ax.axison:
            hidden_ticks.update(id(t) for t in ax.get_xticklabels()+ax.get_yticklabels())
            continue
        for locations,labels,limits in [(ax.get_xticks(),ax.get_xticklabels(),ax.get_xlim()),
                                       (ax.get_yticks(),ax.get_yticklabels(),ax.get_ylim())]:
            lo,hi=sorted(limits)
            hidden_ticks.update(id(t) for x,t in zip(locations,labels) if x<lo-1e-10 or x>hi+1e-10)
    for item in fig.findobj(matplotlib.text.Text):
        if not item.get_visible() or not item.get_text() or id(item) in hidden_ticks:continue
        b=item.get_window_extent(renderer)
        if b.x0 < -1 or b.y0 < -1 or b.x1 > width+1 or b.y1 > height+1:outside.append(item.get_text())
    source=base.with_suffix('.source.json')
    dump(source,dict(figure_id=fid,role=role,width_mm=180,
        source_files=list(USED.values()),panels=panels,
        code=identity(Path(__file__)),visual_qa='SEE_SEPARATE_FIGURE_VISUAL_QA_JSON',
        visual_qa_locator='3_results/75_verified_figures_and_manuscript/FIGURE_VISUAL_QA.json',
        out_of_canvas_text=outside,scope='AUTHOR_REVIEW_NOT_JOURNAL_COMPLIANCE'))
    FIGURES.append(dict(figure_id=fid,role=role,png=identity(base.with_suffix('.png')),
        svg=identity(base.with_suffix('.svg')),source=identity(source),
        panel_count=len(panels),out_of_canvas_text=outside))
    plt.close(fig)


def main():
    cfg=frozen_config()
    freeze=read(ROOT/'0_admin/research_plan/rp_v5_1_main/MAIN_PRE_OUTCOME_FREEZE.json')
    read(ROOT/'0_admin/research_plan/rp_v5_1_main/FROZEN_MAIN_CONFIG.json')
    valid=read(AUDIT/'FINAL_FULL_READBACK_VALIDATION.json')
    assert valid['status']=='PASS_FULL_READBACK' and valid['unique_instances']==960000
    assert valid['validated_scenarios']==192 and valid['failed_modules']==0
    rows=read(AUDIT/'ALL_MAIN_TARGET_SUMMARIES.json')
    families=read(AUDIT/'ALL_MAIN_FDR_SUMMARIES.json')
    paired=read(AUDIT/'ALL_MAIN_PAIRED_SUMMARIES.json')
    chunks=read(AUDIT/'FINAL_MAIN_CHUNK_MANIFEST.json')
    summary_manifest=read(AUDIT/'FINAL_MAIN_SUMMARY_MANIFEST.json')
    assert (len(rows),len(families),len(paired),len(chunks))==(4608,384,2304,3840)
    for r in summary_manifest:
        p=ROOT/r['path'];assert p.stat().st_size==r['bytes'] and sha(p)==r['sha256']
    lookup={(r['scenario_id'],r['method'],r['module_id'],r['target']):r for r in rows}
    flookup={(r['scenario_id'],r['method']):r for r in families}
    scenes=cfg['scenarios'];by={s['scenario_id']:s for s in scenes}
    rules={r['id']:r for r in cfg['figure_selection_rules']}
    for rule in rules.values():
        expected=[s['scenario_id'] for s in scenes if all(s[k]==v for k,v in rule['where'].items())]
        assert expected==rule['scenario_ids'],rule['id']
    def take(ids,method,target,module='M1'):return [lookup[(sid,method,module,target)] for sid in ids]
    pbc_path=ROOT/'3_results/72_solo_local_execution/PBC_MODULE_RECONSTRUCTION_AND_SENSITIVITY.json'
    pbc=read(pbc_path);old=read(ROOT/'3_results/72_solo_local_execution/PRE_OUTCOME_FREEZE.json')
    for r in old['sources']:
        p=ROOT/r['path'];assert p.stat().st_size==r['bytes'] and sha(p)==r['sha256']
    scores=np.array(pbc['score_matrix']);counts=np.array(pbc['cell_counts'])
    assert scores.shape==(8,4) and counts.sum()==1041 and pbc['permutation_allocations']==70
    assert pbc['max_absolute_reconstruction_error']<=1e-6
    for j,m in enumerate(pbc['modules']):
        equal=scores[4:,j].mean()-scores[:4,j].mean()
        weighted=np.average(scores[4:,j],weights=counts[4:])-np.average(scores[:4,j],weights=counts[:4])
        assert abs(equal-m['equal_donor_difference'])<1e-12
        assert abs(weighted-m['cell_count_weighted_donor_score_difference'])<1e-12
        drops=[r['difference'] for r in pbc['gene_dropout'] if r['module']==m['module']]
        assert len(drops)==m['genes'] and [min(drops),max(drops)]==m['leave_one_gene_range']
        assert m['maxT_p']==1
    dump(OUT/'STAGE75_INPUT_IDENTITY.json',dict(config_sha256=cfg['config_sha256'],
        input_files=list(USED.values()),main_summaries_checked=192,
        stage72_frozen_sources_checked=len(old['sources']),
        pbc_n_per_group=4,pbc_cells=1041,new_simulation_instances=0,
        science_scope='CONTINUOUS_VIRTUAL_MODULE_SIMULATION_PLUS_PREVIOUSLY_OBSERVED_DERIVED_PBC'))
    # Full machine-readable tables; no scenario/method/module/target omitted.
    dump(OUT/'supplement/ALL_4608_TARGET_ROWS.json',rows)
    dump(OUT/'supplement/ALL_384_FDR_ROWS.json',families)
    dump(OUT/'supplement/ALL_2304_PAIRED_ROWS.json',paired)
    dump(OUT/'supplement/ALL_192_SCENARIOS_AND_MASK_LOCATORS.json',dict(scenarios=scenes,
        summary_locators=summary_manifest,raw_chunk_manifest=identity(AUDIT/'FINAL_MAIN_CHUNK_MANIFEST.json'),
        masks='Complete empirical mask counts retained in each SCENARIO_SUMMARY.json; not independent experiments'))
    # Figure1 is a computation/estimand schematic, never a causal pathway.
    fig,ax=plt.subplots(figsize=(WIDTH,4.8));ax.axis('off')
    boxes=[(.02,.72,.45,.23,'a  Known-truth continuous simulation',
        '49 virtual genes; K = 5 / 11 / 16 / 17\nDonor, cell and gene factors\nDirect signal: M1 only (K = 5)'),
        (.53,.72,.45,.23,'b  Three distinct estimands',
        'Full donor target: all members\nObserved donor target: random subset\nPopulation cell target: cell-number weights'),
        (.02,.38,.45,.25,'c  Frozen main experiment',
        'A: calibration / coverage (128 scenarios)\nB: background attribution (32)\nC: informative cell numbers (32)\n192 × 5,000 paired instances'),
        (.53,.38,.45,.25,'d  Paired methods and evaluation',
        'Cell-level vs equal-donor Welch\nFull-target 95% CI coverage\nMatching-target Type I / power / BH FDR\nMonte Carlo uncertainty; all scenarios'),
        (.02,.04,.96,.24,'e  Separate, previously observed PBC illustration',
        '4 controls + 4 PBC donors; derived logCPM-based scores\nWeighting and fixed-scale member deletion; all four maxT P = 1\nNo new count reanalysis, disease truth or independent external validation')]
    for x,y,w,h,title,body in boxes:
        ax.add_patch(FancyBboxPatch((x,y),w,h,boxstyle='round,pad=0.007',
            fc='#F7F7F7',ec='#A6A6A6',lw=.7,transform=ax.transAxes))
        ax.text(x+.015,y+h-.035,title,transform=ax.transAxes,va='top',fontsize=9,fontweight='bold')
        ax.text(x+.015,y+h-.085,body,transform=ax.transAxes,va='top',fontsize=8.5,linespacing=1.5)
    fig.subplots_adjust(left=.02,right=.98,bottom=.02,top=.98)
    save(fig,'Figure1','Fig1',[panel('a-e','FROZEN_DESIGN_AND_PRIOR_CASE',[],
        'analytic_design','THREE_EXPLICIT_TARGETS',note='Boxes denote computation dependencies, not causal arrows')],'STUDY_DESIGN')
    # Figure2: exactly the eight pre-outcome null coordinates.
    rule=rules['FIG2_PRIMARY_NULL'];ids=rule['scenario_ids'];ss=[by[s] for s in ids]
    fig,axes=plt.subplots(3,1,figsize=(WIDTH,8.5));panels=[]
    for ax,metric,title,letter in zip(axes,['coverage','type_I_error_matching_target','fdr'],
        ['Full donor-target coverage','Matching-target Type I error','Four-module BH false discovery rate'],'abc'):
        selected=[]
        for i,m in enumerate(METHODS):
            rr=take(ids,m,'theta_D_full') if metric!='fdr' else [flookup[(s,m)] for s in ids]
            rate(ax,rr,metric,COLORS[m],(-.12,.12)[i],('s','o')[i],SHORT[m]);selected+=rr
        ax.axhline(95 if metric=='coverage' else 5,color='#666666',ls='--',lw=.8)
        style(ax,title,letter,'Percent')
        ax.set_xticks(np.arange(8),[f"n{s['n_per_group']} | r{s['rho']:g}\n{'all' if s['coverage']=='full' else 'partial'} ({s['scenario_id']})" for s in ss])
        ax.set_xlim(-.6,7.6);ax.legend(loc='center left',bbox_to_anchor=(.02,.65))
        panels.append(panel(letter,rule,selected,metric,'theta_D_full' if metric=='coverage' else 'MATCHING_METHOD_TARGET',rule['id']))
    fig.subplots_adjust(left=.12,right=.96,top=.95,bottom=.18,hspace=.88)
    save(fig,'Figure2','Fig2',panels,'STATISTICAL_EVIDENCE_NULL_CALIBRATION')
    # Figure3 uses both unchanged, explicitly frozen rule sets.
    rule=rules['FIG3_PRIMARY_TARGET_DRIFT'];ids=rule['scenario_ids'];ss=[by[s] for s in ids]
    crule=rules['FIG3_INFORMATIVE_CELL_TARGETS'];cids=crule['scenario_ids'];cs=[by[s] for s in cids]
    fig,axes=plt.subplots(3,2,figsize=(WIDTH,10.5));axes=axes.ravel();panels=[]
    for ax,method,letter in zip(axes[:2],METHODS[::-1],'ab'):
        full=take(ids,method,'theta_D_full');obs=take(ids,method,'theta_D_observed')
        rate(ax,full,'coverage',COLORS[method],-.10,'o','Full donor target')
        rate(ax,obs,'coverage',COLORS[method],.10,'^','Observed donor target',False)
        ax.axhline(95,color='#666666',ls='--',lw=.8)
        style(ax,f'{SHORT[method]} interval coverage',letter,'Percent');xticks(ax,ss,ids_only=True)
        ax.legend(loc='lower left' if method==METHODS[1] else 'upper left')
        panels.append(panel(letter,rule,full+obs,'coverage',['theta_D_full','theta_D_observed'],rule['id']))
    distribution=[];values=[-.4,-1/15,0.,4/15]
    for sid in ids:
        summary=read(ROOT/cfg['main_result_directory']/sid/'SCENARIO_SUMMARY.json')
        counts_by={round(x,10):0 for x in values}
        for row in summary['mask_distribution']:
            if row['module_id']!='M1':continue
            members=row['observed_members'];observed=sum(1. if g<2 else 0. for g in members)/len(members)
            drift=round(observed-.4,10);assert drift in counts_by
            counts_by[drift]+=row['replicates']
        assert sum(counts_by.values())==5000
        distribution.append(dict(scenario_id=sid,module_id='M1',n=5000,
            target='theta_D_observed_minus_theta_D_full',distribution=counts_by))
    bottom=np.zeros(8)
    for value,color in zip(values,['#542788','#998EC3','#DDDDDD','#5AB4AC']):
        ys=np.array([r['distribution'][round(value,10)] for r in distribution])/50
        axes[2].bar(np.arange(8),ys,bottom=bottom,color=color,label=f'{value:+.3f}',width=.65);bottom+=ys
    axes[2].set_ylim(0,102);style(axes[2],'Member-mask target drift','c','Replicates (%)');xticks(axes[2],ss,ids_only=True)
    axes[2].legend(ncol=2,loc='upper center',bbox_to_anchor=(.5,-.24),
        title='Observed − full target',fontsize=8,title_fontsize=8,columnspacing=.8,handlelength=1)
    panels.append(panel('c',rule,distribution,'truth_drift_distribution','theta_D_observed_minus_theta_D_full',rule['id']))
    selected=[]
    for i,m in enumerate(METHODS):
        rr=take(ids,m,MATCH[m]);rate(axes[3],rr,'power_matching_target',COLORS[m],(-.12,.12)[i],('s','o')[i],SHORT[m]);selected+=rr
    style(axes[3],'Matching-target power','d','Percent');xticks(axes[3],ss,ids_only=True)
    axes[3].legend(loc='center left',bbox_to_anchor=(.02,.56))
    panels.append(panel('d',rule,selected,'power_matching_target','MATCHING_METHOD_TARGET',rule['id'],
        'Conditional non-null denominators differ for partial masks; inspect source rows'))
    selected=[]
    for method,target,offset,marker,name,filled in [
        (METHODS[0],'theta_D_full',-.18,'s','Cell: full donor',True),
        (METHODS[0],'theta_C_observed',0,'^','Cell: population cell',False),
        (METHODS[1],'theta_D_full',.18,'o','Donor: full donor',True)]:
        rr=take(cids,method,target);rate(axes[4],rr,'coverage',COLORS[method],offset,marker,name,filled);selected+=rr
    axes[4].axhline(95,color='#666666',ls='--',lw=.8)
    style(axes[4],'Informative weights: interval coverage','e','Percent');xticks(axes[4],cs,ids_only=True)
    axes[4].legend(loc='center left',bbox_to_anchor=(.02,.76),fontsize=8)
    panels.append(panel('e',crule,selected,'coverage',['theta_D_full','theta_C_observed'],crule['id']))
    means=[];finite=[];population=[]
    shift=2*math.sqrt(.4)*math.sqrt(1.5)*75/105
    for s in cs:
        row=lookup[(s['scenario_id'],METHODS[0],'M1','theta_D_full')]
        info=s['cell_number_rule']=='informative_reverse_mapping'
        pop=shift if info else 0.;f=({4:.8475456224598155,12:1.043678318810064}[s['n_per_group']] if info else 0.)
        means.append(dict(scenario_id=s['scenario_id'],module_id='M1',method=METHODS[0],
            estimate_mean=row['bias'],theta_D_full=0.,population_cell_target=pop,finite_n_expectation=f))
        finite.append(f);population.append(pop)
    ax=axes[5];ax.errorbar(np.arange(8),[r['estimate_mean']['mean'] for r in means],
        yerr=[1.96*r['estimate_mean']['mcse'] for r in means],fmt='s',color=COLORS[METHODS[0]],
        capsize=2,ms=4,label='Cell mean ± 1.96 MCSE')
    ax.plot(np.arange(8),population,'kx',ms=6,label='Population cell target')
    ax.plot(np.arange(8),finite,'+',color='#882255',ms=7,label='Finite-n expectation')
    ax.axhline(0,color='#777777',ls='--',lw=.8,label='Full donor target = 0')
    style(ax,'Population and finite-n targets','f','Continuous score difference');xticks(ax,cs,ids_only=True)
    ax.set_ylim(-.10,1.35);ax.legend(loc='center left',bbox_to_anchor=(.02,.42),fontsize=8)
    panels.append(panel('f',crule,means,'estimate_mean',
        ['theta_D_full','theta_C_observed','theta_C_finite_n_estimator_expectation'],crule['id']))
    fig.subplots_adjust(left=.12,right=.98,top=.95,bottom=.11,hspace=.88,wspace=.50)
    save(fig,'Figure3','Fig3',panels,'STATISTICAL_EVIDENCE_TARGET_SEPARATION')
    # Previously observed PBC illustration, no new patient or gene selection.
    fig,axes=plt.subplots(3,1,figsize=(WIDTH,8.6));modules=pbc['modules'];names=['Anterograde IFT','Retrograde IFT','Basal body / distal appendage','Transition zone']
    weights=np.r_[counts[:4]/counts[:4].sum(),counts[4:]/counts[4:].sum()]
    axes[0].bar(np.arange(8),weights*100,color=['#777777']*4+['#009E73']*4,width=.65)
    axes[0].axhline(25,color='#666666',ls='--',lw=.8)
    for j,w in enumerate(weights):axes[0].text(j,w*100+1,str(counts[j]),ha='center',fontsize=8)
    axes[0].set_xticks(np.arange(8),['Control A','Control B','Control C','Control D','PBC A','PBC B','PBC C','PBC D'],rotation=30,ha='right')
    axes[0].set_ylim(0,60);style(axes[0],'Cell-count weights of existing donor scores','a','Within-group weight (%)')
    # Display aliases are not the original IDs; map is explicit in source.
    alias=[dict(display_alias=a,original_donor=d,cells=int(n),within_group_weight=float(w))
        for a,d,n,w in zip(['Control A','Control B','Control C','Control D','PBC A','PBC B','PBC C','PBC D'],pbc['donors'],counts,weights)]
    for k,key,col,marker,name in [(0,'equal_donor_difference','#0072B2','o','Equal donor'),
                                 (1,'cell_count_weighted_donor_score_difference','#CC79A7','s','Cell-count weighted donor score')]:
        axes[1].scatter([m[key] for m in modules],np.arange(4)+(-.10,.10)[k],c=col,marker=marker,label=name,zorder=3,s=23)
    axes[1].axvline(0,color='#777777',ls='--',lw=.8);axes[1].set_yticks(np.arange(4),names)
    axes[1].invert_yaxis();axes[1].legend(loc='upper center',bbox_to_anchor=(.5,-.37),fontsize=8)
    style(axes[1],'Weighting changes two module directions','b');axes[1].set_xlabel('PBC − control (fixed gene-z module score)')
    for j,m in enumerate(modules):
        axes[2].plot(m['leave_one_gene_range'],[j,j],color='#0072B2',lw=2)
        axes[2].scatter(m['equal_donor_difference'],j,c='#0072B2',s=22,zorder=3)
    axes[2].axvline(0,color='#777777',ls='--',lw=.8)
    axes[2].set_yticks(np.arange(4),[f'{n} (K={m["genes"]}, flips={m["leave_one_gene_sign_reversals"]})' for n,m in zip(names,modules)])
    axes[2].invert_yaxis();axes[2].set_xlabel('PBC − control: full point and member-deletion range')
    style(axes[2],'Leave-one-member-out ranges are not confidence intervals','c')
    fig.subplots_adjust(left=.40,right=.98,top=.96,bottom=.10,hspace=.87)
    save(fig,'Figure4','Fig4',[panel('a','ALL_EIGHT_FROZEN_PRIMARY_DONORS',alias,'descriptive_weights','GROUP_NORMALIZED_DONOR_WEIGHTS'),
        panel('b','ALL_FOUR_FROZEN_MODULES',modules,'descriptive_difference','PBC_MINUS_CONTROL'),
        panel('c','ALL_49_FIXED_SCALE_MEMBER_DELETIONS',pbc['gene_dropout'],'descriptive_range','PBC_MINUS_CONTROL',
              note='All four old maxT P=1; line is min/max of correlated deletions, not CI')],'PREVIOUSLY_OBSERVED_DERIVED_CASE')
    # Complete supplements use original catalog ordering, not outcome ranking.
    for block,fid,bucket in [('A','Supplement_S1','Fig2'),('C','Supplement_S3','Fig3')]:
        ss=[s for s in scenes if s['block']==block];ids=[s['scenario_id'] for s in ss]
        fig,axes=plt.subplots(2,1,figsize=(WIDTH,6.4));panels=[]
        for ax,m,letter in zip(axes,METHODS,'ab'):
            full=take(ids,m,'theta_D_full');matching=take(ids,m,MATCH[m])
            rate(ax,full,'coverage',COLORS[m],-.05,'o','Full donor target')
            rate(ax,matching,'coverage',COLORS[m],.05,'^','Matching observed target',False)
            ax.axhline(95,color='#777777',ls='--',lw=.8)
            style(ax,f'All {block} scenarios: {SHORT[m]}','ab'[METHODS.index(m)],'Coverage (%)')
            xticks(ax,ss,16 if block=='A' else 4,ids_only=True)
            if block=='A':ax.legend(loc='lower left')
            else:ax.legend(loc='center left',bbox_to_anchor=(.02,.73))
            panels.append(panel(letter,{'block':block,'ordering':'FROZEN_CATALOG'},full+matching,'coverage',
                ['theta_D_full',MATCH[m]],'ALL_OTHER_SCENARIOS_COMPLETE_SUPPLEMENT'))
        fig.subplots_adjust(left=.12,right=.98,top=.94,bottom=.16,hspace=.85)
        save(fig,fid,bucket,panels,'COMPLETE_FIXED_DESIGN_SUPPLEMENT')
    ss=[s for s in scenes if s['block']=='B'];ids=[s['scenario_id'] for s in ss]
    fig,axes=plt.subplots(2,2,figsize=(WIDTH,7.3));panels=[]
    for ax,module,letter in zip(axes.ravel(),['M1','M2','M3','M4'],'abcd'):
        selected=[]
        for i,m in enumerate(METHODS):
            rr=take(ids,m,'theta_D_observed',module);rate(ax,rr,'rejection_matching_target',COLORS[m],(-.12,.12)[i],('s','o')[i],SHORT[m]);selected+=rr
        style(ax,f'{module}: background expression detection',letter,'Raw rejection (%)');xticks(ax,ss,8)
        ax.legend(loc='center left',bbox_to_anchor=(.02,.42),fontsize=8)
        panels.append(panel(letter,rules['BACKGROUND_ATTRIBUTION_SUPPLEMENT'],selected,'rejection_matching_target',
            'theta_D_observed','BACKGROUND_ATTRIBUTION_SUPPLEMENT',
            note='Not Type I when effective expression contrast is nonzero; no direct core signal'))
    fig.subplots_adjust(left=.12,right=.98,top=.94,bottom=.18,hspace=.76,wspace=.45)
    save(fig,'Supplement_S2','Fig3',panels,'BACKGROUND_ATTRIBUTION_NOT_MECHANISM')
    ss=[s for s in scenes if s['block']=='A' and s['delta']==0];ids=[s['scenario_id'] for s in ss]
    fig,axes=plt.subplots(2,2,figsize=(WIDTH,7.3));panels=[]
    for ax,module,letter in zip(axes.ravel(),['M1','M2','M3','M4'],'abcd'):
        selected=[]
        for i,m in enumerate(METHODS):
            rr=take(ids,m,MATCH[m],module);rate(ax,rr,'type_I_error_matching_target',COLORS[m],(-.1,.1)[i],('s','o')[i],SHORT[m]);selected+=rr
        ax.axhline(5,color='#777777',ls='--',lw=.8);style(ax,f'{module}: all 64 A null labels',letter,'Type I error (%)');xticks(ax,ss,16)
        ax.legend(loc='center left',bbox_to_anchor=(.02,.42),fontsize=8)
        panels.append(panel(letter,{'block':'A','delta':0,'module_id':module},selected,
            'type_I_error_matching_target','MATCHING_METHOD_TARGET','ALL_OTHER_SCENARIOS_COMPLETE_SUPPLEMENT'))
    fig.subplots_adjust(left=.12,right=.98,top=.94,bottom=.18,hspace=.76,wspace=.45)
    save(fig,'Supplement_S4','Fig2',panels,'ALL_MODULE_NULL_CALIBRATION_NOT_K_SIGNAL_COMPARISON')
    ss=[s for s in scenes if s['block']=='A' and s['delta']==.4 and s['signal_structure']=='sparse_floor_half' and s['coverage']=='ceil_0.6K']
    ids=[s['scenario_id'] for s in ss];fig,axes=plt.subplots(2,1,figsize=(WIDTH,7));panels=[]
    full=take(ids,METHODS[1],'theta_D_full');obs=take(ids,METHODS[1],'theta_D_observed')
    rate(axes[0],full,'coverage',COLORS[METHODS[1]],-.10,'o','Partial score: full target')
    rate(axes[0],obs,'coverage',COLORS[METHODS[1]],.10,'^','Partial score: observed target',False)
    counterparts=[]
    for s in ss:
        match=[t for t in scenes if all(t[k]==v for k,v in s.items() if k not in ['scenario_id','coverage']) and t['coverage']=='full']
        assert len(match)==1;counterparts.append(match[0]['scenario_id'])
    complete=take(counterparts,METHODS[1],'theta_D_full')
    rate(axes[1],complete,'coverage',COLORS[METHODS[1]],0,'o','Full score: full target')
    for ax,letter,title in zip(axes,'ab',['All sparse partial scenarios (K=5)','Corresponding full-member scenarios']):
        ax.axhline(95,color='#777777',ls='--',lw=.8);style(ax,title,letter,'Coverage (%)');xticks(ax,ss);ax.legend(loc='lower left')
    panels=[panel('a',{'block':'A','delta':.4,'signal_structure':'sparse_floor_half','coverage':'ceil_0.6K'},full+obs,
        'coverage',['theta_D_full','theta_D_observed'],'ALL_OTHER_SCENARIOS_COMPLETE_SUPPLEMENT'),
        panel('b',{'paired_full_counterparts_of':ids},complete,'coverage','theta_D_full',
        'ALL_OTHER_SCENARIOS_COMPLETE_SUPPLEMENT',note='x labels identify partial counterpart; row contains actual full scenario ID')]
    fig.subplots_adjust(left=.12,right=.98,top=.94,bottom=.19,hspace=.90)
    save(fig,'Supplement_S5','Fig3',panels,'COMPLETE_SPARSE_MASK_SENSITIVITY_NOT_PRIMARY_RESELECTION')
    dump(OUT/'FIGURE_REGISTER.json',dict(figures=FIGURES,main_count=4,supplement_count=5,
        frozen_rule_identity=cfg['config_sha256'],new_simulation_instances=0,
        all_scenarios_retained=True,submission_ready=False,
        plotting_environment=dict(python=sys.version,numpy=np.__version__,matplotlib=matplotlib.__version__,
                                  font='DejaVu Sans',backend='Agg',width_mm=180,png_dpi=300)))
    dump(OUT/'PRIMARY_PANEL_SELECTION_REGISTER.json',dict(rules=list(rules.values()),
        immutable_config=identity(ROOT/'0_admin/research_plan/rp_v5_1_main/FROZEN_MAIN_CONFIG.json'),
        figure3_primary_rules_kept_together=True,
        source_inputs=list(USED.values()),outcome_ranked_main_selection=False))
    print(json.dumps(dict(main_figures=4,supplement_figures=5,
        out_of_canvas_text={r['figure_id']:r['out_of_canvas_text'] for r in FIGURES},
        target_rows=len(rows),fdr_rows=len(families),paired_rows=len(paired)),indent=2))


if __name__=='__main__':main()
