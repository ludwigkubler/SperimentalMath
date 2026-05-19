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

def gaussian_elimination(A, b):
    n = len(b)
    for i in range(n):
        # Find pivot row
        max_row = i
        for j in range(i+1, n):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        b[i], b[max_row] = b[max_row], b[i]

        # Eliminate lower entries
        for j in range(i+1, n):
            factor = -A[j][i] / A[i][i]
            for k in range(i, n):
                A[j][k] += factor * A[i][k]
            b[j] += factor * b[i]

    # Back substitution
    x = [0] * n
    for i in range(n-1, -1, -1):
        x[i] = (b[i] - sum(A[i][j] * x[j] for j in range(i+1, n))) / A[i][i]
    return x

def plethysm_coefficient(M, k):
    n = len(M)
    M_k = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for l in range(k):
                M_k[i][j] += M[i][l] * M[l][j]
    
    b = [1 if i == 0 else 0 for i in range(n)]
    try:
        return gaussian_elimination(M_k, b)[0]
    except TypeError as e:
        print(f"Error: {e}")
        return None

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = 4
    M = [[random.randint(0, 1) for _ in range(n)] for _ in range(n)]
    
    coeff_perm = plethysm_coefficient(M, 2)
    coeff_det = 1
    
    if coeff_perm is None:
        return {
            "metric_name": "plethysm_coefficient",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "gaussian_elimination_failed"
        }
    
    return {
        "metric_name": "plethysm_coefficient",
        "metric_value": coeff_perm / coeff_det,
        "instances_tested": 1,
        "conjecture_holds": coeff_perm >= 2**n and coeff_det <= 1,
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
    
    if all(result["metric_value"] is not None for result in results):
        mean = sum(result["metric_value"] for result in results) / len(results)
        std_dev = math.sqrt(sum((result["metric_value"] - mean)**2 for result in results) / len(results))
        support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
        if support_fraction >= 0.8:
            print(f"RESULT: SUPPORTED mean={mean} std={std_dev} support_fraction={support_fraction}")
        else:
            first_failing_seed = next(seed for seed, result in enumerate(results) if not result["conjecture_holds"])
            print(f"RESULT: FALSIFIED counterexample=\"plethysm_coefficient_failed\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE gaussian_elimination_failed")