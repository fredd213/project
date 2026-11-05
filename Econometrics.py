from pathlib import Path
 
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
 
SHOW = True  
folder = Path(__file__).parent
df = pd.read_csv(folder / "hprice1.csv")
print("Data shape:", df.shape)
print(df[["price", "lotsize"]].describe(), "\n")
 
def ols(d):
    x = d["lotsize"].to_numpy(float)
    y = d["price"].to_numpy(float)
    n = len(x)
    xbar, ybar = x.mean(), y.mean()
    sst_x = ((x - xbar) ** 2).sum()
    b1 = ((x - xbar) * (y - ybar)).sum() / sst_x
    b0 = ybar - b1 * xbar
    fitted = b0 + b1 * x
    resid = y - fitted
    ssr = (resid ** 2).sum()
    sst = ((y - ybar) ** 2).sum()
    sigma2 = ssr / (n - 2)
    return {
        "n": n, "x": x, "y": y, "xbar": xbar, "ybar": ybar,
        "b0": b0, "b1": b1,
        "se_b1": np.sqrt(sigma2 / sst_x),
        "se_b0": np.sqrt(sigma2 * (1 / n + xbar ** 2 / sst_x)),
        "sigma": np.sqrt(sigma2), "sst_x": sst_x,
        "r2": 1 - ssr / sst, "fitted": fitted, "resid": resid,
    }
 
def report(r, label):
    print(f"--- {label} (n = {r['n']}) ---")
    print(f"Intercept b0 = {r['b0']:.4f}   (se = {r['se_b0']:.4f})")
    print(f"Slope     b1 = {r['b1']:.6f}   (se = {r['se_b1']:.6f})")
    print(f"t-stat for b1 = {r['b1'] / r['se_b1']:.3f}")
    print(f"R-squared     = {r['r2']:.4f}")
    print(f"sigma-hat     = {r['sigma']:.4f}\n")
 
 
# Question 1: Scatter plot
plt.figure(figsize=(6, 4.5))
plt.scatter(df["lotsize"], df["price"], s=18)
plt.xlabel("Lot size (Square feet)")
plt.ylabel("Price (thousands of dollars)")
plt.title("Question 1: Price vs Lot size")
plt.tight_layout()
plt.savefig(folder / "q1_scatter.png", dpi=150)
print("Q1: correlation(price, lotsize) =",
      round(df["price"].corr(df["lotsize"]), 4), "(positive relationship)\n")
 
# Question 2-4: Full sample regression, intercept, slope, R^2
full = ols(df)
print("Q2-Q4")
report(full,"Full sample")
print(f"Q2: estimated intercept = {full['b0']:.4f}")
print(f"Q3: +1 sq ft of lot -> price changes by {full['b1']:.6f} thousand $ "
      f"(about ${full['b1'] * 1000:.2f})")
print(f"Q4: R-squared = {full['r2']:.4f}  "
      f"-> lot size explains about {full['r2'] * 100:.1f}% of price variation\n")
 
check = np.polyfit(full["x"], full["y"], 1)
assert np.allclose(check, [full["b1"], full["b0"]]), "OLS mismatch"
 
# Question 5: Fitted values and residuals vs lot size
plt.figure(figsize=(6, 4.5))
plt.scatter(full["x"], full["fitted"], s=18)
plt.xlabel("Lot size (Square feet)")
plt.ylabel("Fitted price (Thousands of dollars)")
plt.title("Question 5a: Fitted values vs Lot size")
plt.tight_layout()
plt.savefig(folder / "q5a_fitted.png", dpi=150)
plt.figure(figsize=(6, 4.5))
plt.scatter(full["x"], full["resid"], s=18)
plt.axhline(0, color="k", lw=1)
plt.xlabel("Lot size (Square feet)")
plt.ylabel("Residual (Thousands of dollars)")
plt.title("Question 5b: Residuals vs Lot size")
plt.tight_layout()
plt.savefig(folder / "q5b_residuals.png", dpi=150)
print("Q5: saved q5a_fitted.png and q5b_residuals.png")
print(f"sum of residuals = {full['resid'].sum():.2e} (zero by construction)\n")

# Question 8: Regression on the first 50 observations
first50 = ols(df.iloc[:50])
print("Q8: FIRST 50 OBSERVATIONS")
report(first50, "First 50 observations")
print(f"Slope (first 50) = {first50['b1']:.6f} vs slope (full) = {full['b1']:.6f}")
print("Both are unbiased if the subsample is random (SLR.1-SLR.4 still hold),")
print("but individual estimates differ because of sampling variation / outliers.")
print(f"Largest lot in full sample: {int(df['lotsize'].max())} sq ft "
      f"(row {int(df['lotsize'].idxmax())}), "
      f"largest in first 50: {int(df['lotsize'].iloc[:50].max())} sq ft")

if SHOW:
    plt.show()
 