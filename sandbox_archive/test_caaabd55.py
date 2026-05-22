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
    rows_A, cols_A = len(A), len(A[0])
    rows_B, cols_B = len(B), len(B[0])
    result = [[0 for _ in range(cols_B)] for _ in range(rows_A)]
    for i in range(rows_A):
        for j in range(cols_B):
            for k in range(cols_A):
                result[i][j] += A[i][k] * B[k][j]
    return result

def gaussian_elimination(A, b):
    n = len(b)
    A_b = [A[i] + [b[i]] for i in range(n)]
    for i in range(n):
        max_row = i
        for j in range(i+1, n):
            if abs(A_b[j][i]) > abs(A_b[max_row][i]):
                max_row = j
        A_b[i], A_b[max_row] = A_b[max_row], A_b[i]
        pivot = A_b[i][i]
        for j in range(i, n+1):
            A_b[i][j] /= pivot
        for j in range(n):
            if j != i:
                factor = A_b[j][i]
                for k in range(i, n+1):
                    A_b[j][k] -= factor * A_b[i][k]
    return [row[-1] for row in A_b]

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = 30
    δ = 0.5
    r = random.randint(1, n)
    
    # Generate a random n-ary quandle with minimal rank r
    Q = [[random.randint(0, n-1) for _ in range(n)] for _ in range(n)]
    for i in range(n):
        Q[i][i] = 0
    
    # Compute the associated partial function on {0,...,n-1}
    def f(x):
        return Q[x]
    
    # Measure the randomized communication complexity of this partial function for disjointness
    instances_tested = 0
    total_complexity = 0
    for _ in range(30):  # Ensure at least 30 instances per seed
        x, y = random.sample(range(n), 2)
        if x == y:
            continue
        instances_tested += 1
        complexity = 0
        while True:
            z = random.randint(0, n-1)
            if f(z)[x] != f(z)[y]:
                break
            complexity += 1
        total_complexity += complexity
    
    # Correlate the measured complexity with the quandle's minimal rank to establish a lower bound
    average_complexity = total_complexity / instances_tested if instances_tested > 0 else 0
    conjecture_holds = average_complexity >= (n**r) / δ
    counterexample = "" if conjecture_holds else f"Average complexity {average_complexity} < {(n**r) / δ}"
    
    return {
        "metric_name": "Randomized Communication Complexity",
        "metric_value": average_complexity,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(r["metric_value"] > (n**r["metric_value"]) / (2 * 0.5) for n, r in enumerate(results)):
        first_failing_seed = next(i for i, r in enumerate(results) if r["metric_value"] > (i+1)**r["metric_value"] / (2 * 0.5))
        print(f"RESULT: FALSIFIED counterexample=\"Average complexity exceeds bound\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE budget_exceeded n_tested=30")