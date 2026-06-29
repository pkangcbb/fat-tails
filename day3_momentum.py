import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# download data — more stocks for a better momentum strategy
tickers = ["AAPL", "MSFT", "GOOGL", "AMZN", "META", 
           "JPM", "JNJ", "XOM", "GLD", "TLT",
           "NVDA", "TSLA", "BAC", "PFE", "DIS"]

data = yf.download(tickers, start="2019-01-01", end="2024-12-31", auto_adjust=True)
prices = data["Close"]
returns = prices.pct_change()

print(prices.shape)
print(prices.head())

# calculate 3-month (63 trading day) momentum signal
# skip most recent month (21 days) — standard in momentum research
lookback = 63
skip = 21

momentum = prices.shift(skip) / prices.shift(lookback + skip) - 1

print(momentum.tail())


# rank stocks by momentum each day — 1 = lowest, 15 = highest
ranks = momentum.rank(axis=1)

# long top 3, short bottom 3
n_stocks = 3

longs = (ranks.ge(ranks.max(axis=1) - n_stocks + 1, axis=0)).astype(float)
shorts = (ranks.le(n_stocks, axis=0)).astype(float)

# normalize so each side sums to 1
longs = longs.div(longs.sum(axis=1), axis=0)
shorts = shorts.div(shorts.sum(axis=1), axis=0)

# portfolio weights: long winners, short losers
weights = longs - shorts

print(weights.tail())


# A portfolio where weights sum to 0 is called market neutral or a dollar neutral long/short portfolio.
# It is important for each row to have a zero-sum property because my returns come purely from the spread between winners and losers,
# not from if the market goes up or down overall. So, if the market crashes by 20%, the longs lose but the shorts gain roughly the same amount,
# so the market exposure cancels out. You're betting on relative performance, not absolute direction.

# strategy returns — next day's return weighted by today's position
strategy_returns = (weights.shift(1) * returns).sum(axis=1)
cumulative = (1 + strategy_returns).cumprod()

# Any signal such as momentum weights calculated on day t can only be applied to returns on day t+1 or later. Never day t itself.

print(strategy_returns.describe())

sharpe = (strategy_returns.mean() / strategy_returns.std()) * np.sqrt(252)
print(f"Annualized Sharpe ratio: {sharpe:.2f}")

# plot cumulative returns
fig, axes = plt.subplots(2, 1, figsize=(12, 8))

# cumulative return
axes[0].plot(cumulative.index, cumulative, color='#378ADD', linewidth=1.5)
axes[0].axhline(1, color='gray', linewidth=0.5, linestyle='--')
axes[0].set_title(f'Momentum Strategy Cumulative Return (Sharpe: {sharpe:.2f})')
axes[0].set_ylabel('Growth of $1')

# daily returns
axes[1].bar(strategy_returns.index, strategy_returns, 
            color=['#1D9E75' if r > 0 else '#D85A30' for r in strategy_returns],
            width=1)
axes[1].set_title('Daily Returns')
axes[1].set_ylabel('Daily Return')

plt.tight_layout()
# plt.show()

# estimate transaction costs
# assume 10 basis points (0.1%) per trade, each side
turnover = weights.diff().abs().sum(axis=1) / 2
transaction_costs = turnover * 0.001  # 10 bps

# net returns after costs
net_returns = strategy_returns - transaction_costs
net_cumulative = (1 + net_returns).cumprod()
net_sharpe = (net_returns.mean() / net_returns.std()) * np.sqrt(252)

print(f"Gross Sharpe: {sharpe:.2f}")
print(f"Net Sharpe (after costs): {net_sharpe:.2f}")

# plot comparison
plt.figure(figsize=(12, 5))
plt.plot(cumulative.index, cumulative, label=f'Gross (Sharpe: {sharpe:.2f})', color='#378ADD')
plt.plot(net_cumulative.index, net_cumulative, label=f'Net (Sharpe: {net_sharpe:.2f})', color='#D85A30')
plt.axhline(1, color='gray', linewidth=0.5, linestyle='--')
plt.title('Momentum Strategy: Gross vs Net of Transaction Costs')
plt.legend()
plt.show()

# with lookahead bias — wrong
biased_returns = (weights * returns).sum(axis=1)
biased_cumulative = (1 + biased_returns).cumprod()
biased_sharpe = (biased_returns.mean() / biased_returns.std()) * np.sqrt(252)

# without lookahead bias — correct
correct_returns = (weights.shift(1) * returns).sum(axis=1)
correct_cumulative = (1 + correct_returns).cumprod()
correct_sharpe = (correct_returns.mean() / correct_returns.std()) * np.sqrt(252)

print(f"Biased Sharpe:  {biased_sharpe:.2f}")
print(f"Correct Sharpe: {correct_sharpe:.2f}")

plt.figure(figsize=(12, 5))
plt.plot(biased_cumulative.index, biased_cumulative, 
         label=f'With lookahead bias (Sharpe: {biased_sharpe:.2f})', color='#D85A30')
plt.plot(correct_cumulative.index, correct_cumulative, 
         label=f'Correct (Sharpe: {correct_sharpe:.2f})', color='#378ADD')
plt.axhline(1, color='gray', linewidth=0.5, linestyle='--')
plt.title('Lookahead Bias: Does it actually matter?')
plt.legend()
plt.show()