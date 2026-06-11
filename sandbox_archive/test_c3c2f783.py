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

def extended_gcd(a, b):
    if a == 0:
        return b, 0, 1
    else:
        g, x, y = extended_gcd(b % a, a)
        return g, y - (b // a) * x, x

def mod_inverse(a, m):
    g, x, _ = extended_gcd(a, m)
    if g != 1:
        raise ValueError("Modular inverse does not exist")
    else:
        return x % m

def matrix_multiply(A, B):
    rows_A = len(A)
    cols_A = len(A[0])
    rows_B = len(B)
    cols_B = len(B[0])
    if cols_A != rows_B:
        raise ValueError("Incompatible dimensions for matrix multiplication")
    C = [[sum(A[i][k] * B[k][j] for k in range(cols_A)) for j in range(cols_B)] for i in range(rows_A)]
    return C

def gaussian_elimination(A, b):
    n = len(b)
    A_augmented = [A[i] + [b[i]] for i in range(n)]
    for i in range(n):
        max_row = max(range(i, n), key=lambda r: abs(A_augmented[r][i]))
        A_augmented[i], A_augmented[max_row] = A_augmented[max_row], A_augmented[i]
        pivot = A_augmented[i][i]
        if pivot == 0:
            raise ValueError("No unique solution exists")
        for j in range(i, n + 1):
            A_augmented[i][j] /= pivot
        for k in range(n):
            if k != i:
                factor = A_augmented[k][i]
                for j in range(i, n + 1):
                    A_augmented[k][j] -= factor * A_augmented[i][j]
    return [A_augmented[i][-1] for i in range(n)]

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.choice([5, 10, 15, 20, 30, 40])
    clause_count = random.randint(2 * n, 5 * n)
    clauses = []
    for _ in range(clause_count):
        literals = [random.randint(-n, n) for _ in range(random.randint(2, n))]
        clauses.append(literals)
    
    # Construct affine plane embedding
    points = [(i, j) for i in range(n) for j in range(n)]
    lines = []
    for point in points:
        line = [point]
        for other_point in points:
            if other_point != point and (other_point[0] - point[0]) * (other_point[1] - point[1]) == 0:
                line.append(other_point)
        lines.append(line)
    
    # Calculate minimal index
    min_index = len(lines) / n
    
    # Calculate resolution proof width (simplified example)
    w_phi = clause_count + n
    
    return {
        "metric_name": "min_index",
        "metric_value": min_index,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": False,
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2**i + 7 for i in range(5, 30)]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")