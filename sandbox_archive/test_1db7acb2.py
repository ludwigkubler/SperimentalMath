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

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def lcm(a, b):
    return abs(a * b) // gcd(a, b)

def matrix_multiply(A, B):
    m, k = len(A), len(B)
    n = len(B[0])
    C = [[0] * n for _ in range(m)]
    for i in range(m):
        for j in range(n):
            for l in range(k):
                C[i][j] += A[i][l] * B[l][j]
    return C

def gaussian_elimination(A, b):
    m, n = len(A), len(A[0])
    augmented = [A[i] + [b[i]] for i in range(m)]
    for j in range(n):
        pivot_row = max(range(j, m), key=lambda i: abs(augmented[i][j]))
        augmented[j], augmented[pivot_row] = augmented[pivot_row], augmented[j]
        for i in range(j + 1, m):
            factor = augmented[i][j] / augmented[j][j]
            for k in range(n + 1):
                augmented[i][k] -= factor * augmented[j][k]
    x = [0] * n
    for j in range(n - 1, -1, -1):
        x[j] = (augmented[j][-1] - sum(augmented[j][k] * x[k] for k in range(j + 1, n))) / augmented[j][j]
    return x

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    k = random.randint(2, min(n // 2, 8))
    
    # Generate a random monotone DNF formula for k-CLIQUE
    clauses = []
    for _ in range(k):
        clause = [random.choice([1, -1]) * i for i in range(1, n + 1)]
        clauses.append(clause)
    
    # Compute the polymatroid spread via clause-based rank function analysis
    def rank(S):
        return sum(all(x >= 0 for x in (sum(c[i] for c in clauses) for i in S)) for S in range(1, 2**n))
    
    spread = max(rank(S) - rank(S ^ {i}) for i in range(n))
    
    # Measure DNF size
    dnf_size = len(clauses)
    
    # Check the conjecture
    if spread < k**(1/4) * math.log(n):
        return {
            "metric_name": "spread",
            "metric_value": spread,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "spread_too_small"
        }
    if dnf_size < n**(k**(1/4)):
        return {
            "metric_name": "dnf_size",
            "metric_value": dnf_size,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "dnf_size_too_small"
        }
    
    return {
        "metric_name": "spread",
        "metric_value": spread,
        "instances_tested": 1,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 7 for i in range(5, 35)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    spread_values = [r["metric_value"] for r in results if r["conjecture_holds"]]
    dnf_size_values = [r["metric_value"] for r in results if r["conjecture_holds"]]
    
    mean_spread = sum(spread_values) / len(spread_values)
    std_spread = math.sqrt(sum((x - mean_spread)**2 for x in spread_values) / len(spread_values))
    support_fraction = len(spread_values) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_spread} std={std_spread} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        counterexample = next(r["counterexample"] for r in results if not r["conjecture_holds"])
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")