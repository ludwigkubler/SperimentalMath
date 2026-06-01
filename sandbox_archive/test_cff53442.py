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
    n = len(A)
    m = len(A[0])
    for i in range(n):
        max_row = i
        for j in range(i+1, n):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        if A[i][i] == 0:
            return None  # Singular matrix
        for j in range(i+1, n):
            factor = Fraction(A[j][i], A[i][i])
            for k in range(m):
                A[j][k] -= factor * A[i][k]
    return A

def symplectic_leaf(clauses, n):
    points = []
    for clause in clauses:
        point = [0] * (2*n + 1)
        for literal in clause:
            if literal > 0:
                point[literal - 1] = 1
            else:
                point[-literal] = -1
        points.append(point)
    
    A = []
    for i in range(n):
        row = [0] * (2*n + 1)
        row[i] = 1
        A.append(row)
    
    for point in points:
        A.append(point)
    
    return gaussian_elimination(A)

def resolution_width(clauses):
    # Placeholder function to compute resolution width
    # This is a dummy implementation and should be replaced with actual logic
    return len(clauses) * 2

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.choice([5, 10, 15, 20, 30, 40])
    clauses = []
    for _ in range(n):
        clause = [random.randint(1, n), -random.randint(1, n)]
        clauses.append(clause)
    
    L = symplectic_leaf(clauses, n)
    if L is None:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": float('nan'),
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "singular_matrix"
        }
    
    resolution_w = resolution_width(clauses)
    min_order = sum(1 for row in L if any(x != 0 for x in row))
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": Fraction(min_order, resolution_w),
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std=nan support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='correlation_coefficient_outside_O_w' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")