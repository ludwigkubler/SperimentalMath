import random
import math
import sys
import json

def xor(a, b):
    return a ^ b

def mat_mul(A, B):
    m = len(A)
    n = len(B[0])
    p = len(B)
    C = [[0 for _ in range(n)] for _ in range(m)]
    for i in range(m):
        for j in range(n):
            for k in range(p):
                C[i][j] ^= A[i][k] & B[k][j]
    return C

def gaussian_elimination(A, b):
    m = len(A)
    n = len(A[0])
    augmented = [A[i] + [b[i]] for i in range(m)]
    for i in range(n):
        max_row = i
        for j in range(i+1, m):
            if abs(augmented[j][i]) > abs(augmented[max_row][i]):
                max_row = j
        augmented[i], augmented[max_row] = augmented[max_row], augmented[i]
        pivot = augmented[i][i]
        for j in range(n + 1):
            augmented[i][j] ^= pivot & augmented[i][j]
        for j in range(m):
            if j != i:
                factor = augmented[j][i]
                for k in range(n + 1):
                    augmented[j][k] ^= factor & augmented[i][k]
    return [row[-1] for row in augmented]

def min_distance(H):
    m = len(H)
    n = len(H[0])
    distances = [0] * m
    for i in range(m):
        syndrome = 0
        for j in range(n):
            if H[i][j]:
                syndrome ^= 1 << (n - j - 1)
        distances[i] = bin(syndrome).count('1')
    return min(distances)

def generate_random_function(k, n):
    F = [[random.randint(0, 1) for _ in range(n)] for _ in range(2**k)]
    return F

def dual_code(F):
    m = len(F)
    n = len(F[0])
    H = []
    for i in range(m):
        row = [F[i][j] for j in range(n)]
        if sum(row) % 2 == 1:
            H.append(row)
    return H

def run_trial(seed: int) -> dict:
    random.seed(seed)
    k = random.randint(3, 5)
    n = random.choice([5, 8, 11, 14])
    F = generate_random_function(k, n)
    H = dual_code(F)
    d = min_distance(H)
    seed_length = len(bin(seed).replace("0b", ""))
    c = 2  # Empirical constant
    conjecture_holds = seed_length >= c * d
    counterexample = "" if conjecture_holds else f"Seed {seed} does not meet the bound"
    return {
        "metric_name": "seed_length",
        "metric_value": seed_length,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [11, 23, 37, 53, 71]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(json.dumps({"TRIAL": {"seed": seed, **result}}))
        results.append(result)

    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Seed {first_failing_seed} does not meet the bound\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")