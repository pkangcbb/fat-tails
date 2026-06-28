# Puzzle 003: All 6 Sides

## Problem
You roll a fair six-sided die repeatedly. What is the expected number of rolls until you see all six faces at least once?

## Approach

$$E_k = 1*p + (1 - p)(1 + E_k)$$
where p is the probability of rolling a new face and k is the current stage number (number of distinct faces collected so far)

$$E_k = 1*p + (1 - p)(1 + E_k)$$
$$E_k = p + 1 + E_k - p - p*E_k$$
$$0 = 1 - p*E_k$$
$$p*E_k = 1$$
$$E_k = \frac{1}{p}$$

## Solution

When k = 0, p = 6/6 $$E_0 = 1$$
When k = 1, p = 5/6 $$E_1 = \frac{6}{5}$$
When k = 2, p = 4/6 $$E_2 = \frac{6}{4}$$
...
Continues until k = 6

$$E = 1 + \frac{6}{5} + \frac{6}{4} + \frac{6}{3} + \frac{6}{2} + \frac{6}{1} = 14.7$$

## Answer
**14.7 rolls expected.**