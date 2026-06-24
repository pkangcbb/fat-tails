import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

tickers = ["AAPL", "MSFT", "GOOGL", "AMZN", "META", 
           "JPM", "JNJ", "XOM", "GLD", "TLT"]
data = yf.download(tickers, start="2019-01-01", end="2024-12-31", auto_adjust=True)
returns = data["Close"].pct_change().dropna()
print(returns.head())
print(returns.shape)
print(returns.corr())

corr = returns.corr()

fig, ax = plt.subplots(figsize=(8, 6))
im = ax.imshow(corr, cmap="coolwarm", vmin=-1, vmax=1)
plt.colorbar(im)

ax.set_xticks(range(len(tickers)))
ax.set_yticks(range(len(tickers)))
ax.set_xticklabels(tickers)
ax.set_yticklabels(tickers)

for i in range(len(tickers)):
    for j in range(len(tickers)):
        text = ax.text(j, i, f"{corr.iloc[i, j]:.2f}", ha="center", va="center", fontsize=10)

ax.set_title("Return correlation matrix")
# plt.show()

r = returns.values
n = len(r)

# recenter all return values on 0
r_demeaned = r - r.mean(axis=0)

# covariance matrix from scratch
cov_scratch = (r_demeaned.T @ r_demeaned) / (n - 1)

cov_pandas = returns.cov().values

# compare scratch vs pandas covariance
print("Max difference:", abs(cov_scratch - cov_pandas).max())

std = np.sqrt(np.diag(cov_scratch))                 # shape (10,)
outer = std.reshape(-1,1) @ std.reshape(1,-1)       # shape (10, 1) @ shape (1, 10) = shape (10, 10) - this is the outer product of the std vector with itself
corr_scratch = cov_scratch / outer                  # shape (10, 10) - elementwise division to get correlation matrix

corr_pandas = returns.corr().values
print("Max difference:", abs(corr_scratch - corr_pandas).max())

# PCA finds the direction in your data where there is the most variance and then projects your data onto that direction. The first principal component is the direction of maximum variance, the second is the direction of maximum variance orthogonal to the first, and so on. 
# By looking at the eigenvalues of the covariance matrix, you can see how much variance is explained by each principal component. If the first few eigenvalues are much larger than the rest, it means that most of the variance in your data can be captured by 
# just a few principal components, which is why PCA is often used for dimensionality reduction.

# An eigenvector is a vector that does not change direction when a linear transformation is applied to it. In the context of PCA, the eigenvectors of the covariance matrix represent the directions of maximum variance in the data. 
# The corresponding eigenvalues indicate the amount of variance explained by each eigenvector (principal component).
# Say the covariance matrix is [[3, 1], [1, 3]], then both [1, 1] and [1, -1] are eigenvectors, with eigenvalues 4 and 2 respectively. This means that the direction [1, 1] captures more variance in the data than the direction [1, -1], when doing matrix multiplication.
# The sum of eigenvalues = total variance in the data, which is also the sum of the diagonal elements of the covariance matrix (the variance of each individual variable), aka the trace. 4 + 2 = 6 = 3 + 3. The PCA explains 67% of the variance (4/6).

eigenvalues, eigenvectors = np.linalg.eigh(cov_scratch)

idx = np.argsort(eigenvalues)[::-1]
eigenvalues = eigenvalues[idx]
eigenvectors = eigenvectors[:, idx]

print("Eigenvalues:", eigenvalues)
print("\nVariance explained by each component:")
print(eigenvalues / eigenvalues.sum())

print("First principal component weights:")
for ticker, weight in zip(tickers, eigenvectors[:, 0]):
    print(f"{ticker}: {weight:.4f}")



# get SPY for comparison
spy = yf.download("SPY", start="2019-01-01", end="2024-12-31", auto_adjust=True)
spy_returns = spy["Close"].pct_change().dropna().squeeze()

# compute your PC1 time series
# project each day's demeaned returns onto the first eigenvector
pc1 = r_demeaned @ eigenvectors[:, 0]

# convert to pandas series with proper dates to align with SPY
pc1_series = pd.Series(pc1, index=returns.index)

# align dates between pc1 and spy
aligned = pd.DataFrame({"PC1": pc1_series, "SPY": spy_returns}).dropna()

correlation = aligned["PC1"].corr(aligned["SPY"])
print(f"Correlation between PC1 and SPY: {correlation:.4f}")



#SUMMARY
# Covariance measures the shape of co-movement between 2 stocks' deviations from their own typical behavior (their mean). 
# High positive covariance means that, as a statistical tendency across many observed days, when one stock has a good day relative to its own normal, the other stock also tends to have a good day relative to its own normal.
# Covariance does NOT describe whether 2 stocks are moving in the same direction, rather it describes similarity in their shape of movement. So, one stock could be going up and another going down, but their covariance could still be high if they have similar deviation


#DAY 3 - Residual Stripping

betas = np.zeros(10)
for i in range(10):
    stock_returns = r_demeaned[:, i]
    beta = np.cov(stock_returns, pc1)[0, 1] /np.var(pc1)
    betas[i] = beta

print("Betas to PC1 (market factor):")
for ticker, beta in zip(tickers, betas):
    print(f"{ticker}: {beta:.4f}")

residuals = np.zeros_like(r_demeaned)
for i in range(10):
    residuals[:, i] = r_demeaned[:, i] - betas[i] * pc1

print("Original correlations:")
print(np.corrcoef(r_demeaned.T).round(2))
print("\nResidual correlations after removing PC1:")
print(np.corrcoef(residuals.T).round(2))