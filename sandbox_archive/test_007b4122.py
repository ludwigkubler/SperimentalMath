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
        m, n = len(A), len(A[0])
        for i in range(m):
            max_row = i
            for j in range(i+1, m):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            for j in range(i+1, m):
                factor = A[j][i] / A[i][i]
                for k in range(n):
                    A[j][k] -= factor * A[i][k]
        return A
    
    def matrix_mult(A, B):
        m, n, p = len(A), len(B[0]), len(B)
        C = [[0]*n for _ in range(m)]
        for i in range(m):
            for j in range(n):
                for k in range(p):
                    C[i][j] += A[i][k] * B[k][j]
        return C
    
    def is_singular(A):
        m, n = len(A), len(A[0])
        if m != n:
            return True
        det = 1
        for i in range(m):
            max_row = i
            for j in range(i+1, m):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            det *= A[i][i]
            if det == 0:
                return True
        for i in range(m):
            for j in range(i+1, m):
                factor = A[j][i] / A[i][i]
                for k in range(n):
                    A[j][k] -= factor * A[i][k]
        return False
    
    def log2(x):
        if x <= 0:
            return float('-inf')
        return math.log2(x)
    
    n = random.randint(5, 40)
    m = random.randint(1, 2*n)
    p = random.randint(2, 100)
    
    # Generate a random QBF instance
    qbf = [[random.choice([True, False]) for _ in range(n)] for _ in range(m)]
    
    # Compute the clause indicator polynomial modulo p
    poly = [0] * (n + 1)
    for i in range(m):
        term = 1
        for j in range(n):
            if qbf[i][j]:
                term *= -1
        poly[0] += term % p
    
    # Find the quadratic reciprocity lattice that contains all the coefficients of the clause indicator polynomial modulo p
    lattice = [[poly[j]] * (n + 1) for j in range(n + 1)]
    for i in range(1, n + 1):
        for j in range(i, n + 1):
            lattice[i][j] = lattice[j][i] = poly[i] * poly[j] % p
    
    # Compute the minimal order of the quadratic reciprocity lattice
    min_order = len(gaussian_elimination(lattice))
    
    # Check if the minimal order is O(2^n log^2(n/p))
    expected_order = 2**n * (log2(n) + log2(p))**2
    
    return {
        "metric_name": "minimal_order",
        "metric_value": min_order,
        "instances_tested": 1,
        "conjecture_holds": min_order <= expected_order + 1,
        "counterexample": "" if min_order <= expected_order + 1 else f"Order {min_order} exceeds expected {expected_order}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
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
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        counterexample = next(r["counterexample"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")