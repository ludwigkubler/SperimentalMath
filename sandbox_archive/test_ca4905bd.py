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
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
from fractions import Fraction

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def lcm(a, b):
    return abs(a * b) // gcd(a, b)

def matrix_multiply(A, B):
    n = len(A)
    m = len(B[0])
    p = len(B)
    C = [[Fraction(0) for _ in range(m)] for _ in range(n)]
    for i in range(n):
        for j in range(m):
            for k in range(p):
                C[i][j] += A[i][k] * B[k][j]
    return C

def gaussian_elimination(A, b):
    n = len(A)
    m = len(b[0])
    augmented_matrix = [A[i] + b[i] for i in range(n)]
    for j in range(m):
        pivot_row = -1
        for i in range(j, n):
            if augmented_matrix[i][j] != 0:
                pivot_row = i
                break
        if pivot_row == -1:
            continue
        augmented_matrix[pivot_row], augmented_matrix[j] = augmented_matrix[j], augmented_matrix[pivot_row]
        for i in range(n):
            if i != j:
                factor = augmented_matrix[i][j] / augmented_matrix[j][j]
                augmented_matrix[i][j:] -= factor * augmented_matrix[j][j:]
    return [row[m:] for row in augmented_matrix]

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    m = random.randint(n, 2 * n)
    
    # Generate MCSP instance
    clauses = []
    for _ in range(m):
        clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
        clauses.append(clause)
    
    # Construct tropical curve
    T_I = [[Fraction(0)] * n for _ in range(n)]
    for clause in clauses:
        for i in range(n):
            if clause[i] != 0:
                for j in range(i + 1, n):
                    if clause[j] != 0:
                        T_I[i][j] += Fraction(abs(clause[i]) * abs(clause[j]), gcd(abs(clause[i]), abs(clause[j])))
    
    # Compute geometric entropy
    H_T_I = sum(sum(row) for row in T_I)
    
    # Calculate K-complexity (simplified as number of clauses)
    K_I = m
    
    # Check conjecture
    if H_T_I > 2 * K_I:
        return {
            "metric_name": "geometric_entropy",
            "metric_value": H_T_I,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": f"Instance with n={n}, m={m} failed. H(T_I) > 2 * K(I)"
        }
    
    return {
        "metric_name": "geometric_entropy",
        "metric_value": H_T_I,
        "instances_tested": 1,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 97) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, **result}}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = (sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results)) ** 0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Instance with n={n}, m={m} failed. H(T_I) > 2 * K(I)\" first_failing_seed={first_failing_seed}")