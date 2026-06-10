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
            for j in range(n):
                A[i][j] /= pivot
            for j in range(m):
                if j != i and A[j][i] != 0:
                    factor = A[j][i]
                    for k in range(n):
                        A[j][k] -= factor * A[i][k]
        return A

    def rank(A):
        rref = gaussian_elimination([row[:] for row in A])
        rank = 0
        for row in rref:
            if any(x != 0 for x in row):
                rank += 1
        return rank

    def resolution_width(phi):
        # Placeholder function to simulate resolution width calculation
        # Replace with actual implementation as needed
        return random.randint(1, 10)

    def affine_hull_dimension(G):
        # Placeholder function to simulate affine hull dimension calculation
        # Replace with actual implementation as needed
        return rank(G)

    instances_tested = 0
    n_max = 0
    total_dim = 0.0
    total_width = 0.0

    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):
            phi = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
            width = resolution_width(phi)
            dim = affine_hull_dimension(phi)
            
            if width == 0 or dim > 2 * width:
                continue
            
            instances_tested += 1
            n_max = max(n_max, n)
            total_dim += dim
            total_width += width

    if instances_tested < 30:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "insufficient_instances"
        }

    mean_dim = total_dim / instances_tested
    mean_width = total_width / instances_tested
    correlation_coefficient = (instances_tested * sum(d * w for d, w in zip(dim_list, width_list)) -
                               sum(dim_list) * sum(width_list)) / \
                              math.sqrt((instances_tested * sum(d**2 for d in dim_list) - sum(dim_list)**2) *
                                        (instances_tested * sum(w**2 for w in width_list) - sum(width_list)**2))

    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": correlation_coefficient >= 0.8 and p_value <= 0.05,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [random.randint(2, 10**9) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient\" first_failing_seed={first_failing_seed}")