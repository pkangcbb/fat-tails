# Puzzle 001: Flip Coin until first Heads

## Problem
Flip a fair coin until heads. What is the expected number of flips?

## Approach — State Equations

Define:
- $E_0$ = expected flips starting fresh (or after tails)

**Formula:**
$$E = \frac{1}{2}*1 + \frac{1}{2}(1 + E)$$

## Solution

$$E = \frac{1}{2}*1 + \frac{1}{2}(1 + E)$$
$$E = \frac{1}{2} + \frac{1}{2} + \frac{1}{2}E$$
$$\frac{1}{2}E = 1$$
$$E = 2$$

## Answer
**2 flips expected.**