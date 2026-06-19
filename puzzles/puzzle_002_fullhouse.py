"""
Puzzle 002: Full House
----------------------
Problem: How many ways can you get a full house in a 5-card hand from a standard 52-card deck? What is the probability of being dealt a full house?

Approach: 
- A full house consists of 3 cards of one rank and 2 cards of another rank.
- To count the number of full house hands:
1. Choose the rank for the three of a kind: 13 choices
2. Choose 3 suits for the three of a kind: C(4, 3) = 4 choices
3. Choose the rank for the pair (different from the three of a kind): 12 choices
4. Choose 2 suits for the pair: C(4, 2) = 6 choices
- Total full house hands = 13 * 4 * 12 * 6 = 3744
- Total 5-card hands from a 52-card deck = C(52, 5) = 2598960
- Probability = 3744 / 2598960 ≈ 0.00144058

Answer: 3744 ways, Probability ≈ 0.00144058
"""

import numpy as np
from itertools import combinations

# create a deck
deck = [(rank, suit) for rank in range(13) for suit in range(4)]

def is_full_house(hand):
    ranks = [card[0] for card in hand]
    counts = sorted([ranks.count(r) for r in set(ranks)])
    return counts == [2, 3]

# simulate
n_trials = 100000
count = 0
for _ in range(n_trials):
    hand = [deck[i] for i in np.random.choice(len(deck), 5, replace=False)]
    if is_full_house(hand):
        count += 1

print(f"Simulated: {count/n_trials:.6f}")
print(f"Theoretical: {3744/2598960:.6f}")