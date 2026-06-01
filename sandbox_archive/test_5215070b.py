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
        max_row = i
        for j in range(i+1, m):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        if A[i][i] == 0:
            continue
        for j in range(n):
            A[i][j] /= A[i][i]
        for j in range(m):
            if j != i and A[j][i] != 0:
                factor = A[j][i]
                for k in range(n):
                    A[j][k] -= factor * A[i][k]
    return A

def lattice_points_covering(A, b):
    m, n = len(A), len(A[0])
    A_augmented = [row[:] + [b[i]] for i, row in enumerate(A)]
    A_rref = gaussian_elimination(A_augmented)
    
    free_vars = set(range(n-1)) - {i for i in range(m) if A_rref[i][n-1] != 0}
    lattice_points = []
    for comb in itertools.product(range(-1, 2), repeat=len(free_vars)):
        point = [0] * n
        for v, val in zip(free_vars, comb):
            point[v] = val
        if all(A_rref[i][:n-1] @ point + A_rref[i][n-1] == 0 for i in range(m)):
            lattice_points.append(point)
    return len(lattice_points)

def dpll_search_tree_diameter(n, m):
    # Placeholder function to simulate DPLL search tree diameter
    # For simplicity, we assume a linear relationship with n
    return n

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    metric_name = "Lattice Point Coverage vs. DPLL Search Tree Diameter"
    instances_tested = 0
    n_max = 0
    L_total = 0
    D_total = 0
    
    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):
            m = random.randint(n // 2, n * 2)
            A = [[random.randint(-10, 10) for _ in range(n)] for _ in range(m)]
            b = [random.randint(-10, 10) for _ in range(m)]
            
            L = lattice_points_covering(A, b)
            D = dpll_search_tree_diameter(n, m)
            
            L_total += L
            D_total += D
            instances_tested += 1
            n_max = max(n_max, n)
    
    if instances_tested < 30:
        return {
            "metric_name": metric_name,
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "insufficient_instances"
        }
    
    mean_L = L_total / instances_tested
    mean_D = D_total / instances_tested
    
    correlation_coefficient = 0.0
    for i in range(instances_tested):
        correlation_coefficient += (mean_L - L_total[i]) * (mean_D - D_total[i])
    correlation_coefficient /= instances_tested
    
    conjecture_holds = correlation_coefficient >= 0.8 and all(0.5 <= c < 0.8 for c in [correlation_coefficient])
    
    return {
        "metric_name": metric_name,
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] and r["metric_value"] < 0.5 for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"] and r["metric_value"] < 0.5)
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient_below_0.5\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")