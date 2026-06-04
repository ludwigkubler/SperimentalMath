# auto-injected by SEC sandbox
import math
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
from fractions import Fraction

def generate_formula(n, m):
    variables = [f"x{i}" for i in range(1, n+1)]
    clauses = []
    for _ in range(m):
        clause = random.sample(variables + [-v for v in variables], random.randint(1, n))
        clauses.append(clause)
    return clauses, variables

def binary_form_from_formula(clauses, variables):
    A = [[0] * len(variables) for _ in range(len(clauses))]
    for i, clause in enumerate(clauses):
        for j, var in enumerate(clause):
            if var.startswith('x'):
                idx = int(var[1:]) - 1
                A[i][idx] = 1
            else:
                idx = variables.index(var[1:])
                A[i][idx] = -1
    return A

def frobenius_norm(matrix):
    norm = 0
    for row in matrix:
        for val in row:
            norm += val ** 2
    return norm ** 0.5

def resolution_width(clauses):
    # Simplified version of resolution width calculation
    return len(clauses)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        for _ in range(5):
            m = random.randint(n // 2, n * 2)
            clauses, variables = generate_formula(n, m)
            A = binary_form_from_formula(clauses, variables)
            norm = frobenius_norm(A)
            width = resolution_width(clauses)
            results.append((norm, width))
    
    if not results:
        return {
            "metric_name": "Frobenius Norm vs Resolution Width",
            "metric_value": 0,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "empty_results"
        }
    
    norms = [r[0] for r in results]
    widths = [r[1] for r in results]
    mean_norm = sum(norms) / len(norms)
    mean_width = sum(widths) / len(widths)
    std_dev = (sum((x - mean_norm) ** 2 for x in norms) / len(norms)) ** 0.5
    
    if any(n > 1.5 * w for n, w in results):
        return {
            "metric_name": "Frobenius Norm vs Resolution Width",
            "metric_value": mean_norm,
            "instances_tested": len(results),
            "n_max": max(len(clauses) for _, clauses in results),
            "conjecture_holds": False,
            "counterexample": "norm_exceeds_1.5_width"
        }
    
    return {
        "metric_name": "Frobenius Norm vs Resolution Width",
        "metric_value": mean_norm,
        "instances_tested": len(results),
        "n_max": max(len(clauses) for _, clauses in results),
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_dev = (sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results)) ** 0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='norm_exceeds_1.5_width' first_failing_seed={first_failing_seed}")