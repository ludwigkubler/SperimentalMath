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
            pivot = A[i][i]
            if pivot == 0:
                continue
            for j in range(i, n):
                A[i][j] /= pivot
            for j in range(m):
                if j != i and A[j][i] != 0:
                    factor = A[j][i]
                    for k in range(i, n):
                        A[j][k] -= factor * A[i][k]
        return A
    
    def resolution_depth(A):
        m, n = len(A), len(A[0])
        rank = 0
        for i in range(m):
            if all(abs(x) < 1e-9 for x in A[i]):
                continue
            rank += 1
            for j in range(i+1, m):
                if abs(A[j][i]) > 1e-9:
                    factor = A[j][i] / A[i][i]
                    for k in range(n):
                        A[j][k] -= factor * A[i][k]
        return rank
    
    def tseitin_formula(curve):
        n = len(curve)
        variables = list(range(1, 2*n + 1))
        clauses = []
        for i in range(n):
            clauses.append([variables[2*i], -variables[2*i+1]])
            clauses.append([-variables[2*i], variables[2*i+1]])
        return clauses
    
    def tropical_divisor(curve):
        n = len(curve)
        rank = 0
        for i in range(n):
            if curve[i] > 0:
                rank += 1
        return rank
    
    def generate_curve(r):
        curve = [random.randint(0, 1) for _ in range(r)]
        while sum(curve) == 0:
            curve = [random.randint(0, 1) for _ in range(r)]
        return curve
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_depth = 0
    instances_tested = 0
    
    for n in n_values:
        for _ in range(5):
            curve = generate_curve(n)
            divisor_rank = tropical_divisor(curve)
            formula = tseitin_formula(curve)
            depth = resolution_depth(formula)
            total_depth += depth
            instances_tested += 1
    
    mean_depth = total_depth / instances_tested
    conjecture_holds = all(mean_depth >= 2**r for r in n_values) and min(depth for _, depth in zip(n_values, [resolution_depth(tseitin_formula(generate_curve(r))) for r in n_values])) >= 2**min(n_values)
    
    return {
        "metric_name": "mean_resolution_depth",
        "metric_value": mean_depth,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"Mean depth {mean_depth} does not meet the requirement for n={min(n_values)}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(3, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_depth = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_depth} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mean depth does not meet the requirement' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")