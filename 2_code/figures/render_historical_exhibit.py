"""Render H1 from 14 frozen aggregate coordinates only; never refit a disease model.

Dependencies: Matplotlib and NumPy. Run into a new output directory. The source
tables are integrity-checked but expression matrices and human ratings are absent.
"""
import argparse, csv, hashlib
from pathlib import Path, PurePosixPath
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
ROOT=Path(__file__).resolve().parents[2]

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--output-dir',type=Path,required=True);args=parser.parse_args()
    out=args.output_dir.resolve()
    if out.exists() and any(out.iterdir()):raise SystemExit('Output must be new or empty; do not overwrite scientific masters')
    if out==ROOT or ROOT in out.parents:raise SystemExit('Choose an output outside this tracked repository')
    out.mkdir(parents=True,exist_ok=True)
    with (ROOT/'3_results/figure_sources/H1_Frozen_Source_Coordinates.tsv').open(encoding='utf-8',newline='') as f:source=list(csv.DictReader(f,delimiter='\t'))
    assert len(source)==14
    for r in source:
        rel=PurePosixPath(r['source_path']);assert not rel.is_absolute() and '..' not in rel.parts and ':' not in str(rel)
        assert hashlib.sha256((ROOT/rel).read_bytes()).hexdigest()==r['source_sha256']
    labels=['Bulk discovery\n81 donors','Bulk replication, unadjusted\n157 baseline donors','Bulk replication, adjusted\n157 baseline donors','Fibroblast pseudobulk\n22 donors']
    a=[(label,float(r['effect']),float(r['se'])) for label,r in zip(labels,[r for r in source if r['panel']=='A'])]
    bvals=[float(r['effect']) for r in source if r['panel']=='B']
    cr=[]
    for module in ['NPC_CORE_STRUCTURAL','IMPORTIN_KARYOPHERIN','EXPORTIN_MACHINERY','RAN_CYCLE']:
        rr=[r for r in source if r['panel']=='C' and r['outcome']==module];assert len(rr)==2
        cr.append(dict(unadjusted_beta=float(rr[0]['effect']),context_adjusted_beta=float(rr[1]['effect'])))
    plt.rcParams.update({'font.family':'DejaVu Sans','font.size':8,'svg.fonttype':'none','svg.hashsalt':'CTRO_STAGE67'})
    fig,grid=plt.subplots(3,2,figsize=(7.1,9.0),gridspec_kw={'width_ratios':[2.6,1.2],'height_ratios':[1.4,1,1.25]})
    axes=grid[:,0]
    for note in grid[:,1]:note.axis('off')
    ax=axes[0]
    for y,(label,b,se) in enumerate(a):ax.errorbar(b,y,xerr=1.96*se,fmt='o',color='#2166ac' if y<3 else '#b2182b',capsize=3)
    ax.set_yticks(range(4),[t[0] for t in a]);ax.invert_yaxis();ax.set_xlim(-1.55,1.6)
    ax.axvline(0,color='gray',ls=':',lw=1);ax.set_xlabel('Coefficient (within-cohort SD)')
    ax.set_title('A  SSc: scale and model dependence',loc='left',fontsize=9,fontweight='bold',pad=10)
    grid[0,1].text(0,.75,'No pooled effect.\n\nBars: display-only\nnormal approximation\nfrom frozen SEs.\n\nFibroblast localization\nnot established.',fontsize=8,va='top')
    ax=axes[1];ax.scatter(bvals,[0,1],s=65,c=['#2166ac','#b2182b']);ax.axvline(0,color='gray',ls=':')
    ax.set_yticks([0,1],['Discovery','Replication']);ax.invert_yaxis();ax.set_xlim(-2,1)
    for y,b in enumerate(bvals):ax.annotate(f'g = {b:.3f}',(b,y),xytext=(5,8),textcoords='offset points',fontsize=8)
    ax.set_ylim(1.3,-.3)
    ax.set_xlabel('Hedges g (IgAN minus control)');ax.set_title('B  IgAN: direction did not replicate',loc='left',fontsize=9,fontweight='bold',pad=10)
    grid[1,1].text(0,.9,'Discovery maxT FWER\nP = 0.00644\n\nReplication directional\nP = 0.82451\n\nNo frozen SE/CI:\nintervals not invented.',fontsize=8,va='top')
    ax=axes[2];labels=['NPC core','Import','Export','Ran'];y=np.arange(4)
    ax.scatter([r['unadjusted_beta'] for r in cr],y-.1,marker='s',s=45,color='#2166ac',label='Phase-adjusted\nprimary')
    ax.scatter([r['context_adjusted_beta'] for r in cr],y+.1,marker='o',s=45,color='#b2182b',label='Background-program\nadjusted')
    ax.set_yticks(y,labels);ax.invert_yaxis();ax.axvline(0,color='gray',ls=':');ax.set_xlim(-1.65,.5)
    ax.set_xlabel('Module coefficient (SD)');ax.set_title('C  Endometriosis: conditional effects',loc='left',fontsize=9,fontweight='bold',pad=10)
    ax.set_xticks([-1.5,-1,-.5,0,.5])
    grid[2,1].legend(*ax.get_legend_handles_labels(),loc='upper left',bbox_to_anchor=(-.13,1.04),frameon=False,fontsize=8)
    grid[2,1].text(0,.61,'Maximum VIF = 54.83.\n\nAttenuation does not\nprove causal confounding.\n\nSame cohort; not\nindependent replication.\n\nSource coefficients;\nno context SE/CI supplied.',fontsize=8,va='top')
    for ax in axes:ax.spines[['top','right']].set_visible(False)
    fig.suptitle('Selected historical development contrasts\nNot the R1 probability-sampled corpus',fontsize=10,y=.985)
    fig.subplots_adjust(left=.31,right=.98,bottom=.07,top=.92,wspace=.15,hspace=.72)
    for ext in ['png','svg']:fig.savefig(out/f'Historical_Exhibit_H1_Selected_Development_Boundaries.{ext}',dpi=300,metadata={'Date':None} if ext=='svg' else None)
    plt.close(fig)
    print('PASS_FROZEN_COORDINATE_DISPLAY_ONLY_NO_SCIENTIFIC_EXECUTION')
if __name__=='__main__':main()
