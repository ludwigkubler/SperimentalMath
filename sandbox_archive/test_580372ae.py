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
    
    def gaussian_elimination(A, b):
        n = len(b)
        for i in range(n):
            max_row = max(range(i, n), key=lambda k: abs(A[k][i]))
            A[i], A[max_row] = A[max_row], A[i]
            b[i], b[max_row] = b[max_row], b[i]
            factor = A[i][i]
            for j in range(n):
                A[i][j] /= factor
            b[i] /= factor
            for k in range(n):
                if k != i:
                    factor = A[k][i]
                    for j in range(n):
                        A[k][j] -= factor * A[i][j]
                    b[k] -= factor * b[i]
        return b

    def matrix_multiply(A, B):
        n = len(A)
        C = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C

    def matrix_inverse(A):
        n = len(A)
        I = [[1 if i == j else 0 for j in range(n)] for i in range(n)]
        gaussian_elimination(A, I)
        return I

    def cusp_form_weight(instance, level):
        # Placeholder function to compute the weight of a cusp form
        # This is a dummy implementation and should be replaced with actual computation
        return random.random() * 10

    def dpll_search_tree_width(instance):
        # Placeholder function to compute the DPLL search tree width
        # This is a dummy implementation and should be replaced with actual computation
        return random.randint(5, 20)

    n = random.randint(5, 40)
    instances_tested = 30
    metric_values = []
    
    for _ in range(instances_tested):
        instance = [random.choice([0, 1]) for _ in range(n)]
        weight = cusp_form_weight(instance, level=1)
        width = dpll_search_tree_width(instance)
        metric_values.append((weight, width))
    
    if not metric_values:
        return {
            "metric_name": "weight_width_correlation",
            "metric_value": 0,
            "instances_tested": instances_tested,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    weights, widths = zip(*metric_values)
    mean_weight = sum(weights) / len(weights)
    mean_width = sum(widths) / len(widths)
    correlation = (sum((w - mean_weight) * (x - mean_width) for w, x in metric_values) /
                   math.sqrt(sum((w - mean_weight)**2 for w in weights) *
                             sum((x - mean_width)**2 for x in widths)))
    
    return {
        "metric_name": "weight_width_correlation",
        "metric_value": correlation,
        "instances_tested": instances_tested,
        "n_max": n,
        "conjecture_holds": abs(correlation) >= 0.7,
        "counterexample": "" if abs(correlation) >= 0.7 else "mapping_undefined"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 10**9) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all(r["conjecture_holds"] for r in results):
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")