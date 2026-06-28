import numpy as np

def simulate_two_heads(n_trials=1000000):
    results = []
    for _ in range(n_trials):
        prev_flip = 0
        rolls = 0
        head_count = 0
        while head_count < 2:
            flip = np.random.randint(0, 2)
            head_count = flip + prev_flip
            rolls += 1
            prev_flip = flip
        results.append(rolls)
    return np.mean(results)

print(f"Simulated: {simulate_two_heads():.4f}")
print(f"Theoretical: 6.0000")