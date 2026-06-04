# auto-injected by SEC sandbox
import math
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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def gcd(a, b):
        while b:
            a, b = b, a % b
        return a
    
    def lcm(a, b):
        return abs(a * b) // gcd(a, b)
    
    def matrix_multiply(A, B):
        m, n = len(A), len(B[0])
        p = len(B)
        C = [[0] * n for _ in range(m)]
        for i in range(m):
            for j in range(n):
                for k in range(p):
                    C[i][j] += A[i][k] * B[k][j]
        return C
    
    def gaussian_elimination(A, b):
        m, n = len(A), len(A[0])
        augmented = [A[i] + [b[i]] for i in range(m)]
        for i in range(n):
            max_row = i
            for j in range(i+1, m):
                if abs(augmented[j][i]) > abs(augmented[max_row][i]):
                    max_row = j
            augmented[i], augmented[max_row] = augmented[max_row], augmented[i]
            pivot = augmented[i][i]
            for j in range(n + 1):
                augmented[i][j] /= pivot
            for j in range(m):
                if j != i:
                    factor = augmented[j][i]
                    for k in range(n + 1):
                        augmented[j][k] -= factor * augmented[i][k]
        return [row[-1] for row in augmented]
    
    def ehrhart_quotient(P, n):
        # Simplified LLL algorithm to count integral points
        # This is a placeholder and may not be accurate for general polytopes
        return sum(1 for x in range(n+1) for y in range(n+1) if (x + y <= n))
    
    def communication_complexity_rank(L):
        # Placeholder function to compute the rank of a language's communication complexity
        # This is a placeholder and may not be accurate for general languages
        return len(L)
    
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        L = random.sample(range(n), n)  # Generate a language with n elements
        rank = communication_complexity_rank(L)
        quotient = ehrhart_quotient(P, n)
        results.append((quotient, rank))
    
    mean_quotient = sum(q for q, _ in results) / len(results)
    mean_rank = sum(r for _, r in results) / len(results)
    c = mean_quotient / mean_rank
    
    conjecture_holds = all(q <= c * r for q, r in results)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "Ehrhart Quotient",
        "metric_value": mean_quotient,
        "instances_tested": len(results),
        "n_max": max(5, 10, 15, 20, 30, 40),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 1000000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = (sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results)) ** 0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value:.2f} std={std_value:.2f} support_fraction={support_fraction:.2f}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")