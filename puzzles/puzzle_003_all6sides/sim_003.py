"""
Puzzle 003: Coupon Collector (6-sided die)
-------------------------------------------
Problem: "You roll a fair six-sided die repeatedly. What is the expected number of rolls until you see all six faces at least once?"

Approach: 
- This is a classic "coupon collector" problem. The expected number of rolls can be calculated using the formula: E(n) = n * (1 + 1/2 + 1/3 + ... + 1/n), where n is the number of distinct outcomes (in this case, 6).
- For n = 6, the expected number of rolls is: E(6) = 6 * (1 + 1/2 + 1/3 + 1/4 + 1/5 + 1/6) = 6 * (1 + 0.5 + 0.3333 + 0.25 + 0.2 + 0.1667) = 6 * 2.45 = 14.7 rolls
- Recursively, E_k = p * 1 + (1-p) * (1 + E_k), where p is the probability of rolling a new face and k is the current stage number (number of distinct faces collected so far)
    - Simplifies to E_k = 1/p
    - For the first face, p = 6/6 = 1, for the second face, p = 5/6, for the third face, p = 4/6, and so on. -> E(6) = 1 + 6/5 + 6/4 + 6/3 + 6/2 + 6/1 = 14.7 rolls


Answer: 14.7 rolls
"""

import numpy as np

# theoretical calculation
n = 6
expected_rolls = n * sum(1/i for i in range(1, n+1))
print(f"Theoretical expected rolls: {expected_rolls:.2f}")

# simulation to verify
def simulate_coupon_collector(n_faces=6, n_trials=10000):
    results = []
    for _ in range(n_trials):
        seen = set()
        rolls = 0
        while len(seen) < n_faces:
            roll = np.random.randint(1, n_faces+1)
            seen.add(roll)
            rolls += 1
        results.append(rolls)
    return np.mean(results)

print(f"Simulated expected rolls: {simulate_coupon_collector():.2f}")