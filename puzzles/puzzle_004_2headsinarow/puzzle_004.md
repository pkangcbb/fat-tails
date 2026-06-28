# Puzzle 004: Two Heads in a Row

## Problem
What is the expected number of fair coin flips to get two heads in a row?

## Approach — State Equations

Define:
- $E_0$ = expected flips starting fresh (or after tails)
- $E_1$ = expected flips after one head

**From State 0:**
$$E_0 = p_{heads}(1 + E_1) + p_{tails}(1 + E_0)$$
$$E_0 = \frac{1}{2}(1 + E_1) + \frac{1}{2}(1 + E_0)$$
$$E_0 = \frac{1}{2} + \frac{1}{2}E_1 + \frac{1}{2} + \frac{1}{2}E_0$$
$$E_0 = 1 + \frac{1}{2}E_1 + \frac{1}{2}E_0$$

**From State 1:**
$$E_1 = p_{heads}(1) + p_{tails}(1 + E_0)$$
$$E_1 = \frac{1}{2} + \frac{1}{2}(1 + E_0)$$
$$E_1 = 1 + \frac{1}{2}E_0$$

## Solution

Substitute $E_1$ into the first equation:
$$E_0 = 1 + \frac{1}{2}\left(1 + \frac{1}{2}E_0\right) + \frac{1}{2}E_0$$
$$E_0 = \frac{3}{2} + \frac{3}{4}E_0$$
$$E_0 = 6$$

## Answer
**6 flips expected.**