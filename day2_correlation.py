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

# fig, ax = plt.subplots(figsize=(8, 6))
# im = ax.imshow(corr, cmap="coolwarm", vmin=-1, vmax=1)
# plt.colorbar(im)

# ax.set_xticks(range(len(tickers)))
# ax.set_yticks(range(len(tickers)))
# ax.set_xticklabels(tickers)
# ax.set_yticklabels(tickers)

# for i in range(len(tickers)):
#     for j in range(len(tickers)):
#         text = ax.text(j, i, f"{corr.iloc[i, j]:.2f}", ha="center", va="center", fontsize=10)

# ax.set_title("Return correlation matrix")
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