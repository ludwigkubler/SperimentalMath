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

def generate_instance(n):
    A = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
    for i in range(n):
        A[i][i] = 0
    return A

def matrix_multiplication(A, B):
    n = len(A)
    C = [[0 for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

def characteristic_polynomial(A):
    n = len(A)
    p = [[Fraction(0) for _ in range(n)] for _ in range(n)]
    p[0][0] = Fraction(1)
    for i in range(1, n + 1):
        p[i % n] = matrix_multiplication(A, p[(i - 1) % n])
        p[i % n][-1] -= Fraction(i)
    return p[-1]

def minimal_p_adic_hodge_trace(poly):
    n = len(poly)
    trace = 0
    for i in range(n):
        trace += poly[i][i]
    return abs(trace)

def rank_variance(A):
    n = len(A)
    rank = 0
    for row in A:
        if any(row):
            rank += 1
    return (n - rank) / n

def run_instance(n):
    A = generate_instance(n)
    poly = characteristic_polynomial(A)
    trace = minimal_p_adic_hodge_trace(poly)
    variance = rank_variance(A)
    return trace, variance

def run_trial(seed: int) -> dict:
    random.seed(seed)
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):
            try:
                trace, variance = run_instance(n)
                results.append((trace, variance))
            except Exception as e:
                return {
                    "metric_name": "Correlation",
                    "metric_value": None,
                    "instances_tested": len(results),
                    "n_max": n,
                    "conjecture_holds": False,
                    "counterexample": str(e)
                }
    if not results:
        return {
            "metric_name": "Correlation",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "No valid instances generated"
        }
    
    trace_values = [r[0] for r in results]
    variance_values = [r[1] for r in results]
    n_total = len(results)
    mean_trace = sum(trace_values) / n_total
    mean_variance = sum(variance_values) / n_total
    
    correlation = 0
    for i in range(n_total):
        correlation += (trace_values[i] - mean_trace) * (variance_values[i] - mean_variance)
    correlation /= n_total * math.sqrt(sum((x - mean_trace) ** 2 for x in trace_values)) * math.sqrt(sum((y - mean_variance) ** 2 for y in variance_values))
    
    return {
        "metric_name": "Correlation",
        "metric_value": correlation,
        "instances_tested": n_total,
        "n_max": max([r[0] for r in results]),
        "conjecture_holds": 0.8 <= abs(correlation) <= 1.2,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len([r for r in results if r["metric_value"] is not None])
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results if r["metric_value"] is not None)) / len([r for r in results if r["metric_value"] is not None])
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        counterexample = "First failing seed"
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")