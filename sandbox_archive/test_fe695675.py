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

def gaussian_elimination(A):
    m, n = len(A), len(A[0])
    for i in range(m):
        # Find pivot
        max_row = i
        for r in range(i+1, m):
            if abs(A[r][i]) > abs(A[max_row][i]):
                max_row = r
        A[i], A[max_row] = A[max_row], A[i]
        
        # Eliminate below
        for r in range(i+1, m):
            factor = A[r][i] / A[i][i]
            for c in range(n):
                A[r][c] -= factor * A[i][c]

def matrix_multiply(A, B):
    m, n, p = len(A), len(B), len(B[0])
    C = [[0 for _ in range(p)] for _ in range(m)]
    for i in range(m):
        for j in range(p):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

def compute_monotone_complexity(f):
    n = len(f)
    if n == 1:
        return 1
    complexity = 0
    for i in range(1, n):
        for j in range(1, math.ceil(math.log2(i+1)) + 1):
            if all(f[i*2**j + k] <= f[i*2**(j-1) + k] for k in range(2**(j-1))):
                complexity += 1
    return complexity

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    f = [random.choice([0, 1]) for _ in range(2**n)]
    
    monotone_complexity = compute_monotone_complexity(f)
    twisted_differential_forms_rank = len(gaussian_elimination([[f[i*2**j + k] for k in range(2**(j-1))] for j in range(1, math.ceil(math.log2(n+1)) + 1)]))
    
    ratio = Fraction(twisted_differential_forms_rank, monotone_complexity) if monotone_complexity != 0 else Fraction(0)
    
    metric_value = ratio.numerator / ratio.denominator
    conjecture_holds = 0.5 <= metric_value <= 1.5 and abs(metric_value - 1) < 0.2
    counterexample = "" if conjecture_holds else f"Ratio {metric_value} out of bounds"
    
    return {
        "metric_name": "Ratio of Twisted Differential Forms Rank to Monotone Complexity",
        "metric_value": metric_value,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else list(range(2, 30*41, 41))
    
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
        print(f"RESULT: FALSIFIED counterexample=\"Ratio out of bounds\" first_failing_seed={first_failing_seed}")