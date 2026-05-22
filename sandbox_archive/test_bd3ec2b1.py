# auto-injected by SEC sandbox
import itertools
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from itertools import product, combinations, permutations, chain
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def is_prime(n):
        if n <= 1:
            return False
        for i in range(2, int(math.sqrt(n)) + 1):
            if n % i == 0:
                return False
        return True
    
    primes = [i for i in range(2, 100) if is_prime(i)]
    seed_primes = random.sample(primes, 30)
    
    def gaussian_elimination(A):
        m, n = len(A), len(A[0])
        for i in range(m):
            max_row = i
            for j in range(i + 1, m):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            factor = A[i][i]
            for j in range(n):
                A[i][j] /= factor
            for j in range(m):
                if j != i:
                    factor = A[j][i]
                    for k in range(n):
                        A[j][k] -= factor * A[i][k]
        return A
    
    def matrix_multiply(A, B):
        m, n, p = len(A), len(B), len(B[0])
        C = [[0 for _ in range(p)] for _ in range(m)]
        for i in range(m):
            for j in range(n):
                for k in range(p):
                    C[i][k] += A[i][j] * B[j][k]
        return C
    
    def compute_tropical_polynomial(n):
        coefficients = [random.uniform(-1, 1) for _ in range(n + 1)]
        return coefficients
    
    def compute_min_real_points(coefficients):
        n = len(coefficients) - 1
        A = [[0 for _ in range(n)] for _ in range(n)]
        b = [0] * n
        for i in range(n):
            for j in range(i, n):
                A[i][j] = coefficients[j + 1]
                if i == j:
                    A[i][j] += 1
            b[i] = -coefficients[0]
        
        A = gaussian_elimination(A)
        x = [0] * n
        for i in range(n - 1, -1, -1):
            x[i] = (b[i] - sum(A[i][j] * x[j] for j in range(i + 1, n))) / A[i][i]
        
        return sum(1 for xi in x if xi >= 0)
    
    def compute_acc0_circuit_threshold(D, S):
        epsilon = 0.1
        return 2 ** (D / 2 + epsilon * S)
    
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        coefficients = compute_tropical_polynomial(n)
        min_real_points = compute_min_real_points(coefficients)
        
        for D in range(1, 6):
            for S in range(1, 6):
                threshold = compute_acc0_circuit_threshold(D, S)
                results.append({
                    "n": n,
                    "D": D,
                    "S": S,
                    "coefficients": coefficients,
                    "min_real_points": min_real_points,
                    "threshold": threshold
                })
    
    mean_difference = sum(abs(result["min_real_points"] - result["threshold"]) for result in results) / len(results)
    
    return {
        "metric_name": "Mean Difference",
        "metric_value": mean_difference,
        "instances_tested": len(results),
        "conjecture_holds": mean_difference <= 1,
        "counterexample": "" if mean_difference <= 1 else f"mean_diff={mean_difference}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, **{trial_result}}}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mean_diff_exceeded\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")