import pandas as pd, numpy as np, statsmodels.formula.api as smf
from pathlib import Path
df = pd.read_csv(Path(__file__).parent / 'PS2_data.csv')

# Question 1
print("Question 1")
m1 = smf.ols('wage ~ education + ability', df).fit()
print(m1.summary())
print('b1 =', m1.params['education'], 'se =', m1.bse['education'])

# Question 2
print("Question 2")
df['lwage'] = np.log(df['wage'])
m2 = smf.ols('lwage ~ education + ability', df).fit()
print(m2.summary())

# Question 3
print("Question 3")
print('R2 =', m1.rsquared,'SSR =', m1.ssr, 'SER =', np.sqrt(m1.scale))

# Question 4
print("Question 4")
m4a = smf.ols('education ~ ability', df).fit()
df['res'] = m4a.resid
m4b = smf.ols('wage ~ res', df).fit()
print(m4b.summary())
print('coef res =', m4b.params['res'], ' vs b1 =', m1.params['education'])

# Question 5
print("Question 5")
m5 = smf.ols('wage ~ education', df).fit()
print(m5.summary())
b1t = m5.params['education']; print('b1~ =', b1t)

# Question 6
print("Question 6")
print('R2 short/long =', m5.rsquared, m1.rsquared)
print('SSE(ESS) short/long =', m5.ess, m1.ess, ' SST =', m1.centered_tss)

# Question 7
print("Question 7")
m7 = smf.ols('ability ~ education', df).fit()
d1 = m7.params['education']
b2 = m1.params['ability']; b1 = m1.params['education']
print('delta1 =', d1, ' b2 =', b2, ' b2*d1 =', b2*d1, ' b1~ - b1 =', b1t-b1)
print('corr(education, ability) =', df.education.corr(df.ability))

# Question 9 
print("Question 9")
from statsmodels.stats.diagnostic import het_breuschpagan
print('BP test (Q1 model):', het_breuschpagan(m1.resid, m1.model.exog))
import pandas as pd, numpy as np, statsmodels.formula.api as smf
import matplotlib.pyplot as plt
from pathlib import Path
 
try:
    base = Path(__file__).parent
except NameError:
    base = Path('.')
df = pd.read_csv(base / 'PS2_data.csv')
m1 = smf.ols('wage ~ education + ability', df).fit()
df['fitted'] = m1.fittedvalues
df['resid'] = m1.resid
 
fig, ax = plt.subplots(1, 3, figsize=(15, 4.2), sharey=True)
for a, x, lab in zip(ax, ['fitted', 'education', 'ability'],
                     ['Fitted wage', 'Education (years)', 'Ability']):
    a.scatter(df[x], df['resid'], s=14, alpha=0.7)
    a.axhline(0, color='red', lw=1)
    a.set_xlabel(lab); a.set_title(f'Residuals vs {lab.lower()}')
ax[0].set_ylabel('Residual')
plt.tight_layout()
plt.savefig(base / 'q9_residual_plots.png', dpi=150)
plt.show()