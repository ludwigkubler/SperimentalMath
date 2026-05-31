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
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from fractions import Fraction

def gaussian_elimination(A, b):
    n = len(b)
    for i in range(n):
        max_row = i + max(range(i, n), key=lambda k: abs(A[k][i]))
        A[i], A[max_row] = A[max_row], A[i]
        b[i], b[max_row] = b[max_row], b[i]
        for j in range(i + 1, n):
            factor = -A[j][i] / A[i][i]
            for k in range(i, n):
                A[j][k] += factor * A[i][k]
            b[j] += factor * b[i]
    x = [0] * n
    for i in range(n - 1, -1, -1):
        x[i] = (b[i] - sum(A[i][j] * x[j] for j in range(i + 1, n))) / A[i][i]
    return x

def matrix_multiply(A, B):
    m, k = len(A), len(B[0])
    n = len(B)
    C = [[0] * k for _ in range(m)]
    for i in range(m):
        for j in range(k):
            for l in range(n):
                C[i][j] += A[i][l] * B[l][j]
    return C

def polynomial_from_formula(formula):
    # Implement a procedure to convert Tseitin formula to polynomial
    # This is a placeholder implementation and should be replaced with actual logic
    raise ValueError("Invalid formula")

def tseitin_to_polynomial(clauses):
    n = len(clauses)
    A = [[0] * (2*n + 1) for _ in range(2*n + 1)]
    b = [0] * (2*n + 1)
    
    # Construct the system of linear equations
    for i, clause in enumerate(clauses):
        if len(clause) == 1:
            A[i][i + n] = 1
            b[i] = -1
        elif len(clause) == 2:
            x1, x2 = clause[0], clause[1]
            A[i][x1] = 1
            A[i][x2] = 1
            b[i] = -1
        else:
            raise ValueError("Invalid clause")
    
    # Solve the system of linear equations
    roots = gaussian_elimination(A, b)
    num_roots = sum(1 for root in roots if abs(root) > 1e-6)
    
    return num_roots

def resolution_width(clauses):
    # Implement a procedure to compute the resolution width
    # This is a placeholder implementation and should be replaced with actual logic
    return random.randint(1, 10)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    clauses = []
    for _ in range(n):
        if random.random() < 0.5:
            x = random.randint(1, n)
            clauses.append([x])
        else:
            x1, x2 = random.sample(range(1, n + 1), 2)
            clauses.append([x1, -x2])
    
    num_roots = tseitin_to_polynomial(clauses)
    proof_width = resolution_width(clauses)
    
    return {
        "metric_name": "num_roots",
        "metric_value": num_roots,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": False,
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_C = sum(result["metric_value"] for result in results) / len(results)
    std_C = math.sqrt(sum((result["metric_value"] - mean_C) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_C} std={std_C} support_fraction={support_fraction}")
    elif any(result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in enumerate(results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=mapping_undefined")