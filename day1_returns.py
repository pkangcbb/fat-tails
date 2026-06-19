import yfinance as yf
import numpy as np
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

aapl = yf.download("AAPL", start="2019-01-01", end="2024-12-31", auto_adjust=True)
print(aapl.head())

aapl["Return"] = aapl["Close"].pct_change()
print(aapl["Return"].head(10))

returns = aapl["Return"].dropna()
print(returns.describe())

print(f"Skewness: {returns.skew()}")
print(f"Kurtosis: {returns.kurtosis()}")

r = returns.values
n = len(r)

mean = np.sum(r) / n
std = np.sqrt(np.sum((r - mean) ** 2) / (n - 1))
z_scores = (r - mean) / std
skew = np.sum(z_scores ** 3) / (n - 1)
kurt = np.sum(z_scores ** 4) / (n - 1) - 3 

print(f"Mean: {mean:.6f}  vs pandas: {returns.mean():.6f}")
print(f"Std:  {std:.6f}  vs pandas: {returns.std():.6f}")
print(f"Skew: {skew:.6f}  vs pandas: {returns.skew():.6f}")
print(f"Kurt: {kurt:.6f}  vs pandas: {returns.kurtosis():.6f}")

fig, ax = plt.subplots(figsize=(10,6))

ax.hist(returns, bins=80, density=True, alpha=0.6, color="#4C8BF5", label="Actual returns")

x = np.linspace(returns.min(), returns.max(), 300)
ax.plot(x, stats.norm.pdf(x, mean, std), "r--", linewidth=2, label="Normal distribution")

# ax.set_xlim(-0.15, 0.15)
# ax.set_ylim(0, 2)
ax.set_xlabel("Daily return")
ax.set_ylabel("Density")
ax.set_title("AAPL return distribution vs normal")
ax.legend()
plt.show()
plt.close()

print(returns.index)

# resample to monthly returns
monthly = (1 + returns).resample('ME').prod() - 1

fig, axes = plt.subplots(1, 2, figsize=(14, 5))

axes[0].hist(returns, bins=80, density=True, alpha=0.6, color="#4C8BF5")
axes[0].set_title(f"Daily returns — kurtosis: {returns.kurtosis():.2f}")

axes[1].hist(monthly, bins=30, density=True, alpha=0.6, color="#34A853")
axes[1].set_title(f"Monthly returns — kurtosis: {monthly.kurtosis():.2f}")

plt.tight_layout()
plt.show()