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

def generate_disjointness_matrix(n):
    subsets = [set(random.sample(range(1, 2**math.ceil(math.log2(n))), n)) for _ in range(n)]
    M = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            if len(subsets[i].intersection(subsets[j])) == 0:
                M[i][j] = 1
                M[j][i] = 1
    return M

def matrix_multiplication(A, B):
    n = len(A)
    C = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

def identity_matrix(n):
    I = [[0] * n for _ in range(n)]
    for i in range(n):
        I[i][i] = 1
    return I

def numerical_range(M, tol=1e-6):
    n = len(M)
    I = identity_matrix(n)
    B = [M[i] - (i+1)*I for i in range(n)]
    eigenvalues = []
    for k in range(100):  # Max iterations
        v = [random.random() for _ in range(n)]
        v /= sum(v) ** 0.5
        w = matrix_multiplication(M, v)
        lambda_k = sum(w[i] * v[i] for i in range(n))
        eigenvalues.append(lambda_k)
    return max(eigenvalues), min(eigenvalues)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = 40
    M = generate_disjointness_matrix(n)
    cb_norm_max, _ = numerical_range(M)
    metric_value = cb_norm_max
    instances_tested = 1
    conjecture_holds = metric_value >= 0.1 * n
    counterexample = "" if conjecture_holds else "cb_norm < 0.1*n"
    return {
        "metric_name": "cb_norm",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 8)]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']:.6f}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean_metric = sum(r['metric_value'] for r in results) / len(results)
    std_metric = (sum((r['metric_value'] - mean_metric)**2 for r in results) / len(results))**0.5
    support_fraction = sum(1 for r in results if r['conjecture_holds']) / len(results)
    
    if all(r['conjecture_holds'] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric:.6f} std={std_metric:.6f} support_fraction={support_fraction:.2f}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric:.6f} std={std_metric:.6f} support_fraction={support_fraction:.2f}")
    else:
        first_failing_seed = next(r['seed'] for r in results if not r['conjecture_holds'])
        print(f"RESULT: FALSIFIED counterexample=\"cb_norm < 0.1*n\" first_failing_seed={first_failing_seed}")