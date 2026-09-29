"""Triode characteristic slopes with private input data."""
from pathlib import Path
import argparse,json
import numpy as np
import pandas as pd
ROOT=Path(__file__).resolve().parents[1]

def fit_slope(voltage,current,lower,upper):
    """Original unweighted straight-line fit, with inclusive voltage limits."""
    x=np.asarray(voltage,dtype=float);y=np.asarray(current,dtype=float)
    mask=(x>=lower)&(x<=upper)
    if mask.sum()<2 or len(np.unique(x[mask]))<2:
        raise ValueError('Each fit window must contain at least two distinct voltages.')
    slope,intercept=np.polyfit(x[mask],y[mask],1)
    return float(slope),float(intercept),int(mask.sum())

def summarize(slopes):
    """Arithmetic mean and sample SD across curves, as in the original code."""
    values=np.asarray(slopes,dtype=float)
    return float(np.mean(values)),float(np.std(values,ddof=1)) if len(values)>1 else np.nan

def run(root=ROOT):
    root=Path(root);folder=root/'private_data'
    paths=[folder/n for n in ['measurements.csv','fit_windows.csv','settings.json']]
    if not all(p.is_file() for p in paths):
        print('Private data are not included. Complete the templates under private_data/; see docs/input_format.md.')
        return None
    measurements=pd.read_csv(paths[0],dtype={'group_id':str,'curve_id':str,'kind':str})
    windows=pd.read_csv(paths[1],dtype={'group_id':str,'kind':str})
    cfg=json.loads(paths[2].read_text());unit=cfg.get('current_unit')
    if unit not in ['A','mA','uA','monitor_unit']:
        raise ValueError('Set current_unit to A, mA, uA or monitor_unit. Calibrate inputs locally.')
    if measurements.empty or windows.empty:raise ValueError('Templates contain headers only. Supply local measurements and fit windows.')
    mcols=['group_id','curve_id','kind','fixed_voltage_V','swept_voltage_V','current']
    wcols=['group_id','kind','lower_voltage_V','upper_voltage_V']
    if not set(mcols)<=set(measurements) or not set(wcols)<=set(windows):raise ValueError('Input columns do not match templates.')
    if measurements[mcols].isna().any().any() or windows[wcols].isna().any().any():raise ValueError('Required values must not be missing.')
    if not measurements.kind.isin(['gm','ga']).all() or not windows.kind.isin(['gm','ga']).all():raise ValueError('kind must be gm or ga.')
    for df,cols in [(measurements,mcols[3:]),(windows,wcols[2:])]:
        if not np.isfinite(df[cols].to_numpy(dtype=float)).all():raise ValueError('Numeric values must be finite.')
    if windows.duplicated(['group_id','kind']).any():raise ValueError('Only one fit window per group and kind; use separate group labels for alternative windows.')
    if (windows.lower_voltage_V>=windows.upper_voltage_V).any():raise ValueError('Window lower limit must be less than upper limit.')
    records=[]
    for (group,kind,curve),d in measurements.groupby(['group_id','kind','curve_id'],sort=True):
        if d.fixed_voltage_V.nunique()!=1:raise ValueError('Each curve must have one fixed electrode voltage.')
        if d.swept_voltage_V.duplicated().any():raise ValueError('Use separate curve IDs for repeat scans; swept voltages must be unique per curve.')
        w=windows[(windows.group_id==group)&(windows.kind==kind)]
        if len(w)!=1:raise ValueError('Missing fit window for a group and kind.')
        w=w.iloc[0];slope,b,n=fit_slope(d.swept_voltage_V,d.current,w.lower_voltage_V,w.upper_voltage_V)
        records.append(dict(group_id=group,kind=kind,curve_id=curve,fixed_voltage_V=float(d.fixed_voltage_V.iloc[0]),
                            slope=slope,intercept=b,n_fit=n,lower_voltage_V=w.lower_voltage_V,upper_voltage_V=w.upper_voltage_V,
                            slope_unit=unit+'/V'))
    curves=pd.DataFrame(records);rows=[]
    for group,d in curves.groupby('group_id'):
        row={'group_id':group,'conductance_unit':unit+'/V'}
        for kind in ['gm','ga']:
            values=d.loc[d.kind==kind,'slope'].to_numpy()
            if not len(values):raise ValueError('Each group needs both gm and ga curves.')
            mean,sd=summarize(values);row[kind+'_mean']=mean;row[kind+'_sample_sd']=sd;row[kind+'_count']=len(values)
        gm,ga=row['gm_mean'],row['ga_mean'];sgm,sga=row['gm_sample_sd'],row['ga_sample_sd']
        if ga==0:
            row.update(mu=np.nan,mu_propagated_sd=np.nan,status='zero_ga_unresolved')
        else:
            mu=gm/ga
            # Equivalent derivative form of original ratio-error formula; defined at gm=0.
            err=np.sqrt((sgm/ga)**2+(gm*sga/(ga*ga))**2)
            row.update(mu=mu,mu_propagated_sd=err,status='summary_only' if np.isfinite(err) else 'insufficient_curves_for_sample_sd')
        rows.append(row)
    summary=pd.DataFrame(rows);out=root/'private_outputs';out.mkdir(exist_ok=True)
    curves.to_csv(out/'curve_slopes.csv',index=False);summary.to_csv(out/'group_summary.csv',index=False)
    print('Analysis completed. Tables are saved locally in private_outputs/. Spread is sample SD across curves, not a full uncertainty budget.')
    return curves,summary

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--root',type=Path,default=ROOT)
    try:run(parser.parse_args().root)
    except (ValueError,KeyError) as error:parser.exit(1,str(error)+'\n')
