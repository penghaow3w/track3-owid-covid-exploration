from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import hashlib, json

ROOT=Path(__file__).resolve().parents[1]
raw=ROOT/'data/raw/compact_2026-10-04.csv'
before=hashlib.sha256(raw.read_bytes()).hexdigest()
out=ROOT/'data/processed/exploration_2026-10-04'; out.mkdir(parents=True,exist_ok=True)
fig=ROOT/'figures/exploration_2026-10-04'; fig.mkdir(parents=True,exist_ok=True)
d=pd.read_csv(raw,parse_dates=['date'],low_memory=False)
d=d[d.continent.notna()].copy()
d['week']=d.date.dt.to_period('W-SUN')
g=d.groupby(['country','week'],observed=True)
weekly=g.agg(continent=('continent','first'),population=('population','first'),population_density=('population_density','first'),median_age=('median_age','first'),life_expectancy=('life_expectancy','first'),gdp_per_capita=('gdp_per_capita','first'),total_vaccinations=('total_vaccinations','max'),new_cases=('new_cases','sum'),days=('date','nunique'),observed_new_cases=('new_cases','count')).reset_index()
weekly['expected_days']=weekly.week.map(lambda x:(x.end_time.date()-x.start_time.date()).days+1)
weekly['complete']=(weekly.days.eq(weekly.expected_days)&weekly.observed_new_cases.eq(weekly.expected_days))
weekly['new_cases']=weekly.new_cases.where(weekly.complete)
weekly['positive']=weekly.new_cases.gt(0)
def first_k(s,k):
    x=s.where(s.gt(0)).dropna()
    out=pd.Series(pd.NA,index=s.index,dtype='string')
    text=x.astype('int64').astype(str)
    eligible=text[text.str.len().ge(k)]
    out.loc[eligible.index]=eligible.str[:k]
    return out
weekly['first_digit']=first_k(weekly.new_cases,1)
weekly['first_2_digits']=first_k(weekly.new_cases,2)
weekly['first_3_digits']=first_k(weekly.new_cases,3)
weekly['year']=weekly.week.dt.year
weekly['week_start']=weekly.week.map(lambda x:x.start_time)
weekly['week_end']=weekly.week.map(lambda x:x.end_time.normalize())
weekly=weekly.drop(columns=['week'])
weekly.to_csv(out/'country_week_new_cases_exploration.csv',index=False)
def stat(c):
    s=weekly[c]
    return {'field':c,'rows':len(s),'nonmissing':int(s.notna().sum()),'missing_pct':round(s.isna().mean()*100,3)}
summary=pd.DataFrame([stat(c) for c in ['new_cases','first_digit','first_2_digits','first_3_digits']])
summary.to_csv(out/'digit_availability.csv',index=False)
desc=['population','population_density','median_age','life_expectancy','gdp_per_capita','total_vaccinations']
pd.DataFrame([stat(c) for c in desc]).to_csv(out/'descriptor_availability.csv',index=False)
for c,title in [('population_density','Population density'),('median_age','Median age'),('life_expectancy','Life expectancy'),('gdp_per_capita','GDP per capita'),('total_vaccinations','Cumulative vaccinations')]:
    vals=weekly.loc[weekly[c].gt(0),c].dropna()
    plt.figure(figsize=(8,4.5)); plt.hist(np.log10(vals),bins=30,color='#4472c4',edgecolor='white'); plt.title(title+' by country-week (log10 positive values)'); plt.xlabel('log10(value)'); plt.ylabel('weekly records'); plt.tight_layout(); plt.savefig(fig/(c+'_log10.png'),dpi=150); plt.close()
for c in ['first_digit','first_2_digits','first_3_digits']:
    vals=weekly.loc[weekly.positive,c].dropna().astype(str); counts=vals.value_counts().sort_index(); counts.to_csv(out/(c+'_counts.csv'),header=['count'])
    plt.figure(figsize=(10,4)); counts.plot.bar(color='#70ad47'); plt.title('Positive complete weekly new_cases: '+c); plt.xlabel(c); plt.ylabel('records'); plt.tight_layout(); plt.savefig(fig/(c+'_distribution.png'),dpi=150); plt.close()
assert hashlib.sha256(raw.read_bytes()).hexdigest()==before
info={'rows':len(weekly),'positive_complete_rows':int(weekly.positive.sum()),'countries':int(weekly.country.nunique()),'raw_unchanged':True,'main_target':'weekly new_cases','third_digit_is_secondary':True}
(out/'summary.json').write_text(json.dumps(info,indent=2),encoding='utf-8')
print(summary.to_string(index=False)); print(json.dumps(info,indent=2))
