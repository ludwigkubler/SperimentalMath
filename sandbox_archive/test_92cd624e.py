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
    random.seed(seed)
    
    def gaussian_elimination(A, b):
        n = len(b)
        for i in range(n):
            max_row = i
            for j in range(i+1, n):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            b[i], b[max_row] = b[max_row], b[i]
            for j in range(i+1, n):
                factor = Fraction(A[j][i], A[i][i])
                A[j] = [A[j][k] - factor * A[i][k] for k in range(n)]
                b[j] -= factor * b[i]
        x = [0] * n
        for i in range(n-1, -1, -1):
            x[i] = Fraction(b[i], A[i][i])
            for j in range(i-1, -1, -1):
                b[j] -= A[j][i] * x[i]
        return x
    
    def lattice_points_covering(A, b):
        n = len(b)
        points = []
        for i in range(2**n):
            point = [0] * n
            for j in range(n):
                if (i >> j) & 1:
                    point[j] = 1
            if all(point[i] * A[i][j] <= b[j] for j in range(n)):
                points.append(point)
        return len(points)
    
    def dpll_search_tree(A, b):
        n = len(b)
        def solve(i, assignment):
            if i == n:
                return all(assignment[j] * A[j][k] <= b[k] for k in range(n))
            if 0 not in [A[i][j] for j in range(n)] and 1 not in [A[i][j] for j in range(n)]:
                return False
            if 0 in [A[i][j] for j in range(n)]:
                assignment[i] = 0
                if solve(i+1, assignment):
                    return True
            if 1 in [A[i][j] for j in range(n)]:
                assignment[i] = 1
                if solve(i+1, assignment):
                    return True
            return False
        assignment = [None] * n
        return solve(0, assignment)
    
    def generate_ip(n, m):
        A = [[random.randint(-5, 5) for _ in range(n)] for _ in range(m)]
        b = [random.randint(-10, 10) for _ in range(m)]
        return A, b
    
    n_values = [5, 10, 15, 20, 30, 40]
    L_total = 0
    D_total = 0
    instances_tested = 0
    n_max = 0
    
    for n in n_values:
        for _ in range(5):
            A, b = generate_ip(n, random.randint(n, 2*n))
            L = lattice_points_covering(A, b)
            D = dpll_search_tree(A, b)
            L_total += L
            D_total += D
            instances_tested += 1
            n_max = max(n_max, n)
    
    if instances_tested < 30:
        return {
            "metric_name": "correlation",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "insufficient_instances"
        }
    
    L_avg = L_total / instances_tested
    D_avg = D_total / instances_tested
    
    correlation = 0
    for i in range(instances_tested):
        correlation += (L_avg - L_total / instances_tested) * (D_avg - D_total / instances_tested)
    correlation /= instances_tested * (L_total / instances_tested - L_avg) * (D_total / instances_tested - D_avg)
    
    return {
        "metric_name": "correlation",
        "metric_value": correlation,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": 0.5 <= correlation <= 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] + list(range(31, 100))
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, **result}}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] and r["metric_value"] < 0.5 for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"] and r["metric_value"] < 0.5)
        print(f"RESULT: FALSIFIED counterexample=\"low_correlation\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction}")