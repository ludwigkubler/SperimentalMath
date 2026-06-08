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

def generate_random_boolean_function(n):
    return [random.choice([0, 1]) for _ in range(2**n)]

def characteristic_polynomial(f):
    n = len(f)
    A = [[0] * (n + 1) for _ in range(n + 1)]
    for i in range(n):
        A[i][i] = -1
        A[n][i] = f[i]
    A[n][n] = 1
    return gaussian_elimination(A)

def gaussian_elimination(A):
    n = len(A)
    for i in range(n):
        max_row = i
        for j in range(i + 1, n):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        for j in range(i + 1, n):
            factor = A[j][i] / A[i][i]
            for k in range(n + 1):
                A[j][k] -= factor * A[i][k]
    return [A[i][-1] for i in range(n)]

def minimal_root_multiplicity_index(poly):
    roots = find_roots(poly)
    multiplicities = {root: roots.count(root) for root in set(roots)}
    return min(multiplicities.values())

def find_roots(poly):
    n = len(poly)
    if n == 1:
        return [0]
    elif n == 2:
        a, b = poly
        return [-b / a]
    else:
        roots = []
        for i in range(n):
            sub_poly = poly[:i] + poly[i+1:]
            root = -sub_poly[-1] / sum(sub_poly[j] * (i ** j) for j in range(i))
            roots.append(root)
        return roots

def communication_complexity_rank_variance(f):
    n = len(f)
    rank = 0
    for i in range(2**n):
        if f[i] == 1:
            rank += 1
    return rank / (2**n)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        f = generate_random_boolean_function(n)
        poly = characteristic_polynomial(f)
        mri = minimal_root_multiplicity_index(poly)
        cc_variance = communication_complexity_rank_variance(f)
        results.append((n, mri, cc_variance))
    
    if len(results) < 30:
        return {
            "metric_name": "log_sqrt_mri_over_log_cc_variance",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max(n for n, _, _ in results),
            "conjecture_holds": False,
            "counterexample": "insufficient_instances"
        }
    
    log_sqrt_mris = [math.log(math.sqrt(mri)) for _, mri, _ in results]
    log_cc_variances = [math.log(cc_variance) for _, _, cc_variance in results]
    mean_log_sqrt_mri = sum(log_sqrt_mris) / len(log_sqrt_mris)
    mean_log_cc_variance = sum(log_cc_variances) / len(log_cc_variances)
    
    if abs(mean_log_sqrt_mri - mean_log_cc_variance) > 0.1:
        return {
            "metric_name": "log_sqrt_mri_over_log_cc_variance",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max(n for n, _, _ in results),
            "conjecture_holds": False,
            "counterexample": "discrepancy_in_means"
        }
    
    return {
        "metric_name": "log_sqrt_mri_over_log_cc_variance",
        "metric_value": None,
        "instances_tested": len(results),
        "n_max": max(n for n, _, _ in results),
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    supported_trials = [r for r in results if r["conjecture_holds"]]
    support_fraction = len(supported_trials) / len(results)
    
    if support_fraction >= 0.8:
        RESULT = "SUPPORTED"
    elif any(r["counterexample"] == "insufficient_instances" for r in supported_trials):
        RESULT = "INCONCLUSIVE insufficient_instances"
    elif any(r["counterexample"] == "discrepancy_in_means" for r in supported_trials):
        RESULT = "INCONCLUSIVE discrepancy_in_means"
    else:
        RESULT = "FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed=0"
    
    print(f"{RESULT} mean=<x> std=<y> support_fraction={support_fraction}")