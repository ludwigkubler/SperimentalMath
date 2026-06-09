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
    
    def gaussian_elimination(A):
        n = len(A)
        for i in range(n):
            max_row = i
            for j in range(i+1, n):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            pivot = A[i][i]
            if pivot == 0:
                continue
            for j in range(i, n):
                A[i][j] /= pivot
            for k in range(n):
                if k != i and abs(A[k][i]) > 1e-9:
                    factor = A[k][i]
                    for j in range(i, n):
                        A[k][j] -= factor * A[i][j]
        return A

    def matrix_multiply(A, B):
        n = len(A)
        C = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C

    def is_positive_definite(A):
        n = len(A)
        for i in range(n):
            if A[i][i] <= 0:
                return False
            for j in range(i+1, n):
                A[j][i] /= A[i][i]
            for k in range(i+1, n):
                for l in range(i+1, n):
                    A[k][l] -= A[k][i] * A[l][i]
        return True

    def characteristic_polynomial(A):
        n = len(A)
        det = 0
        for p in itertools.permutations(range(n)):
            sign = (-1) ** sum(i > j for i, j in enumerate(p))
            term = sign
            for i in range(n):
                term *= A[i][p[i]]
            det += term
        return det

    def min_representation_size(poly):
        n = len(poly)
        if n == 0:
            return 0
        size = n
        for i in range(1, n+1):
            if poly % i == 0:
                size = min(size, i)
        return size

    n = random.randint(5, 40)
    m = random.randint(n, n*3)
    variables = list(range(n))
    clauses = [random.sample(variables, random.randint(1, n)) for _ in range(m)]
    
    A = [[0] * n for _ in range(n)]
    for clause in clauses:
        for i in clause:
            for j in clause:
                if i != j:
                    A[i][j] += 1
    
    A = gaussian_elimination(A)
    det = characteristic_polynomial(A)
    
    if det == 0:
        return {
            "metric_name": "rank_variance",
            "metric_value": float('inf'),
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "det(A) = 0"
        }
    
    min_size = min_representation_size(det)
    
    rank_variance = sum(abs(A[i][j]) for i in range(n) for j in range(i+1, n)) / (n * (n-1) / 2)
    
    return {
        "metric_name": "rank_variance",
        "metric_value": rank_variance,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": rank_variance <= min_size,
        "counterexample": ""
    }

if __name__ == "__main__":
    if len(sys.argv) > 1:
        seeds = [int(s) for s in sys.argv[1:]]
    else:
        primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
        seeds = random.sample(primes, min(30, len(primes)))
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    metric_values = [r["metric_value"] for r in results if "metric_value" in r]
    conjecture_holds = all(r["conjecture_holds"] for r in results if "conjecture_holds" in r)
    
    mean_value = sum(metric_values) / len(metric_values) if metric_values else float('nan')
    std_value = math.sqrt(sum((x - mean_value) ** 2 for x in metric_values) / len(metric_values)) if metric_values else float('nan')
    support_fraction = sum(1 for r in results if "conjecture_holds" in r and r["conjecture_holds"]) / len(results)
    
    if conjecture_holds:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(r["counterexample"] for r in results):
        counterexample = next(r["counterexample"] for r in results if "counterexample" in r)
        first_failing_seed = next(r["seed"] for r in results if "conjecture_holds" not in r or not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE no_conjecture_holds")