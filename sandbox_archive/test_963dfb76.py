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

def run_trial(seed: int) -> dict:
    n = 30
    M = [[random.choice([-1, 1]) for _ in range(n)] for _ in range(n)]
    
    def log_det(M_t):
        U = gaussian_elimination(M_t)
        det = 1.0
        for i in range(n):
            det *= U[i][i]
        return math.log(abs(det))
    
    def f(t):
        M_t = [[M[i][j] + t * delta(i, j) for j in range(n)] for i in range(n)]
        return log_det(M_t)
    
    def adaptive_quadrature(f, a, b):
        n = 10
        s = 0.5 * (f(a) + f(b))
        h = (b - a) / (2 * n)
        for k in range(1, n):
            s += f(a + (2 * k - 1) * h)
        return s * h
    
    phi_M = adaptive_quadrature(f, -10, 10) / (2 * math.pi)
    
    metric_value = phi_M / math.sqrt(n)
    conjecture_holds = metric_value >= 0.8
    counterexample = "" if conjecture_holds else "phi(M) < 0.7√n"
    
    return {
        "metric_name": "free_entropy_ratio",
        "metric_value": metric_value,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

def gaussian_elimination(A):
    n = len(A)
    for i in range(n):
        max_row = i + argmax(abs(row[i]) for row in A[i:])
        A[i], A[max_row] = A[max_row], A[i]
        for j in range(i+1, n):
            factor = A[j][i] / A[i][i]
            A[j] = [A[j][k] - factor * A[i][k] for k in range(n)]
    return A

def argmax(iterable):
    return max(range(len(iterable)), key=iterable.__getitem__)

if __name__ == "__main__":
    import sys
    seeds = list(map(int, sys.argv[1:])) or [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']:.6f}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean = sum(r["metric_value"] for r in results) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean:.6f} std={std_dev:.6f} support_fraction={support_fraction:.2f}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"phi(M) < 0.7√n\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient data")