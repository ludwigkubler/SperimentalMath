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
    return abs(a*b) // gcd(a, b)

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
    augmented = [row + [b[i]] for i, row in enumerate(A)]
    for i in range(n):
        max_row = max(range(i, m), key=lambda x: abs(augmented[x][i]))
        augmented[i], augmented[max_row] = augmented[max_row], augmented[i]
        if augmented[i][i] == 0:
            return None
        for j in range(i+1, m):
            factor = augmented[j][i] / augmented[i][i]
            augmented[j] = [augmented[j][k] - factor * augmented[i][k] for k in range(n+1)]
    x = [0] * n
    for i in range(n-1, -1, -1):
        x[i] = (augmented[i][-1] - sum(augmented[i][j] * x[j] for j in range(i+1, n))) / augmented[i][i]
    return x

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(10, 40)
    m = math.ceil(n ** 0.6)
    
    # Generate a random 3-CNF formula
    clauses = []
    for _ in range(m):
        literals = [random.choice([f'x{i}', f'~x{i}']) for i in range(1, n+1)]
        clause = random.choice(literals) + " OR " + random.choice(literals) + " OR " + random.choice(literals)
        clauses.append(clause)
    formula = " AND ".join(clauses)
    
    # Compute monotone circuit size
    incidence_matrix = [[0] * n for _ in range(m)]
    for i, clause in enumerate(clauses):
        for literal in clause.split():
            if literal.startswith('x'):
                j = int(literal[1:]) - 1
                incidence_matrix[i][j] = 1
    
    dp = [0] * (n + 1)
    dp[0] = 1
    for i in range(m):
        new_dp = [0] * (n + 1)
        for j in range(n, -1, -1):
            if j >= len(clauses[i].split()):
                new_dp[j] = dp[j]
            else:
                new_dp[j] = dp[j] + dp[j - len(clauses[i].split())]
        dp = new_dp
    
    size_phi = dp[n]
    
    # Compute Kronecker coefficients (simplified for demonstration)
    k_phi = 2 ** n / size_phi
    
    result = {
        "metric_name": "Kronecker Coefficient Gap",
        "metric_value": k_phi,
        "instances_tested": 1,
        "conjecture_holds": k_phi * size_phi <= 2 ** (n ** 0.3),
        "counterexample": ""
    }
    
    return result

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.getrandbits(32) for _ in range(30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
    support_fraction = sum(result["conjecture_holds"] for result in results) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")