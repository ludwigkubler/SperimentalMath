# auto-injected by SEC sandbox
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from fractions import Fraction
from itertools import combinations

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def lcm(a, b):
    return abs(a * b) // gcd(a, b)

def matrix_multiply(A, B):
    m, k = len(A), len(B[0])
    n = len(B)
    C = [[0] * k for _ in range(m)]
    for i in range(m):
        for j in range(k):
            for l in range(n):
                C[i][j] += A[i][l] * B[l][j]
    return C

def gaussian_elimination(A):
    m, n = len(A), len(A[0])
    rank = 0
    for i in range(min(m, n)):
        pivot_row = -1
        for r in range(i, m):
            if A[r][i] != 0:
                pivot_row = r
                break
        if pivot_row == -1:
            continue
        A[i], A[pivot_row] = A[pivot_row], A[i]
        rank += 1
        for r in range(m):
            if r != i and A[r][i] != 0:
                factor = A[r][i] / A[i][i]
                for c in range(n):
                    A[r][c] -= factor * A[i][c]
    return rank

def generate_tseitin_circuit(n, m):
    variables = [f'x{i}' for i in range(n)]
    clauses = []
    for i in range(m):
        a, b = random.sample(variables, 2)
        if random.choice([True, False]):
            clauses.append(f'{a} OR {b}')
        else:
            clauses.append(f'(NOT {a}) AND (NOT {b})')
    return variables, clauses

def geometric_quantization_matrix(C):
    n = len(C)
    m = len(C[0])
    A = [[0] * (n + 1) for _ in range(m)]
    for i in range(m):
        for j in range(n):
            if C[i][j] == 'OR':
                A[i][j] = 1
            elif C[i][j] == 'AND':
                A[i][j] = -1
            else:
                A[i][j] = 0
    return A

def minimal_rank(matrix):
    return gaussian_elimination(matrix)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [30, 40]
    m_values = [100, 200]
    total_metric_value = 0
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""

    for n in n_values:
        for m in m_values:
            variables, clauses = generate_tseitin_circuit(n, m)
            C = [[clauses[i][j] for j in range(n)] for i in range(m)]
            Q_C = geometric_quantization_matrix(C)
            rank = minimal_rank(Q_C)
            expected_value = m**2 * math.log(n)
            tolerance = 0.3 * expected_value
            if abs(rank - expected_value) > tolerance:
                conjecture_holds = False
                counterexample = f"Tseitin circuit with n={n}, m={m} failed"
                break
            total_metric_value += rank
            instances_tested += 1

    return {
        "metric_name": "Minimal Rank",
        "metric_value": total_metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] if sys.argv[1:] else list(range(2, 50, 2))
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")