"""
Puzzle 001: Coin Flip
---------------------
Problem: Flip a fair coin until heads. What is the expected number of flips?

Approach:
- Recognized as geometric distribution with p = 0.5
- Used recursive argument: E = 1/2(1) + 1/2(1 + E)
- Solved to get E = 2
- Also verified using geometric series derivative trick

Answer: 2
"""

import numpy as np

# recursive derivation
# E = 1/2(1) + 1/2(1 + E)
# E/2 = 1
# E = 2
theoretical = 2

# simulation to verify
flips = np.random.geometric(p=0.5, size=1000000)
simulated = flips.mean()

print(f"Theoretical: {theoretical}")
print(f"Simulated:   {simulated:.4f}")