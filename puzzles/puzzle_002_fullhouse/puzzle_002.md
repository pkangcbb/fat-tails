# Puzzle 002: Full House

## Problem
How many ways can you get a full house in a 5-card hand from a standard 52-card deck? What is the probability of being dealt a full house?

## Approach — State Equations

**Formulas:**
Total # of Full House Combinations 
$$13*\binom{4}{3} + 12*\binom{4}{2}$$

Total # of 5-card Hands
$$\binom{52}{5}$$

## Solution

$$13*\binom{4}{3} + 12*\binom{4}{2} = 3744$$
$$\binom{52}{5} = 2598960$$
$\frac{3744}{2598960} = 0.00144058$

## Answer
**p = 0.00144058**