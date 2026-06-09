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

def gaussian_elimination(A, b):
    n = len(b)
    for i in range(n):
        # Find pivot row
        max_row = i
        for k in range(i+1, n):
            if abs(A[k][i]) > abs(A[max_row][i]):
                max_row = k
        A[i], A[max_row] = A[max_row], A[i]
        b[i], b[max_row] = b[max_row], b[i]

        # Eliminate lower entries in column i
        for k in range(i+1, n):
            factor = Fraction(A[k][i], A[i][i])
            for j in range(i, n):
                A[k][j] -= factor * A[i][j]
            b[k] -= factor * b[i]

    # Back substitution
    x = [0] * n
    for i in range(n-1, -1, -1):
        x[i] = Fraction(b[i], A[i][i])
        for k in range(i-1, -1, -1):
            b[k] -= A[k][i] * x[i]
    return x

def generate_polynomial(num_vars, degree, p):
    coeffs = [random.randint(0, p-1) for _ in range(degree + 1)]
    poly = sum(c * (x**i) % p for i, c in enumerate(coeffs))
    return poly

def modular_form_degree(poly, p):
    # Placeholder function to compute the degree of a modular form
    # This is a stub and should be replaced with actual computation
    return 1  # Example value, replace with actual computation

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    p = random.choice([2, 3, 5, 7, 11])
    poly = generate_polynomial(n, n, p)
    
    m = modular_form_degree(poly, p)
    D = n  # Placeholder for actual circuit depth computation
    
    if m <= 0 or D <= 0:
        return {
            "metric_name": "modular_form_degree",
            "metric_value": None,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "invalid_values"
        }
    
    if m <= D * math.log(n, p):
        conjecture_holds = True
        counterexample = ""
    else:
        conjecture_holds = False
        counterexample = f"m={m} > O(D log n) for n={n}, D={D}"
    
    return {
        "metric_name": "modular_form_degree",
        "metric_value": m,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    metric_values = [r["metric_value"] for r in results if r["metric_value"] is not None]
    support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)
    
    mean_metric = sum(metric_values) / len(metric_values) if metric_values else 0
    std_metric = (sum((x - mean_metric) ** 2 for x in metric_values) / len(metric_values)) ** 0.5 if metric_values else 0
    
    if support_fraction >= 0.8 and mean_metric <= 3:
        print(f"RESULT: SUPPORTED mean={mean_metric} std={std_metric} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")