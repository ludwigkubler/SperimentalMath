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
        n = len(A)
        for i in range(n):
            max_row = i + max(range(i, n), key=lambda k: abs(A[k][i]))
            A[i], A[max_row] = A[max_row], A[i]
            b[i], b[max_row] = b[max_row], b[i]
            for j in range(i + 1, n):
                factor = Fraction(A[j][i], A[i][i])
                for k in range(n):
                    A[j][k] -= factor * A[i][k]
                b[j] -= factor * b[i]
        return A, b
    
    def solve_linear_system(A, b):
        n = len(A)
        x = [0] * n
        for i in range(n - 1, -1, -1):
            x[i] = Fraction(b[i], A[i][i])
            for j in range(i + 1, n):
                x[i] -= Fraction(x[j] * A[i][j], A[i][i])
        return x
    
    def lattice_points_covering(A, b):
        n = len(A)
        solutions = []
        for i in range(2**n):
            point = [0] * n
            for j in range(n):
                if (i >> j) & 1:
                    point[j] = 1
            if all(point[i] * A[i][j] <= b[j] for j in range(n)):
                solutions.append(point)
        return len(solutions)
    
    def dpll_search_tree(A, b, assignment):
        n = len(A)
        if not any(A[i][j] * assignment[j] > b[i] for i in range(n)):
            return 1
        var = next(j for j in range(n) if assignment[j] is None)
        assignment[var] = True
        true_branch = dpll_search_tree(A, b, assignment)
        assignment[var] = False
        false_branch = dpll_search_tree(A, b, assignment)
        return 1 + max(true_branch, false_branch)
    
    def generate_random_ip(n, m):
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
            A, b = generate_random_ip(n, random.randint(1, n))
            L = lattice_points_covering(A, b)
            assignment = [None] * n
            D = dpll_search_tree(A, b, assignment)
            L_total += L
            D_total += D
            instances_tested += 1
            if n > n_max:
                n_max = n
    
    mean_L = Fraction(L_total, instances_tested)
    mean_D = Fraction(D_total, instances_tested)
    
    correlation_coefficient = (instances_tested * sum(L * D for L, D in zip([mean_L] * instances_tested, [mean_D] * instances_tested)) - 
                               sum(L for L in [mean_L] * instances_tested) * sum(D for D in [mean_D] * instances_tested)) / \
                              math.sqrt((instances_tested * sum(L**2 for L in [mean_L] * instances_tested) - sum(L for L in [mean_L] * instances_tested)**2) *
                                        (instances_tested * sum(D**2 for D in [mean_D] * instances_tested) - sum(D for D in [mean_D] * instances_tested)**2))
    
    conjecture_holds = correlation_coefficient >= 0.8
    counterexample = "" if conjecture_holds else "correlation_coefficient < 0.8"
    
    return {
        "metric_name": "Correlation Coefficient",
        "metric_value": float(correlation_coefficient),
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, **result}}")
        results.append(result)
    
    mean_value = sum(res["metric_value"] for res in results) / len(results)
    std_value = math.sqrt(sum((res["metric_value"] - mean_value)**2 for res in results) / len(results))
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not res["conjecture_holds"] for res in results) and support_fraction >= 0.8:
        first_failing_seed = next(res["seed"] for res in results if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient < 0.8\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE support_fraction < 0.8")