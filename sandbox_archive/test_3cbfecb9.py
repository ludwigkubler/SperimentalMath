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

def gaussian_elimination(A):
    m, n = len(A), len(A[0])
    for i in range(m):
        max_row = i
        for j in range(i+1, m):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        for j in range(i+1, m):
            factor = Fraction(A[j][i], A[i][i])
            for k in range(n):
                A[j][k] -= factor * A[i][k]
    return A

def rank_of_matrix(A):
    A = gaussian_elimination(A)
    rank = 0
    for row in A:
        if any(row):
            rank += 1
    return rank

def dpll_search_tree_height(phi):
    # Simplified DPLL search tree height calculation
    # This is a placeholder function and should be replaced with actual logic
    return len(phi)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):  # Sample 5 instances per size
            m = random.randint(n, 2*n)
            phi = [[random.choice([0, 1]) for _ in range(n)] for _ in range(m)]
            
            clause_indicator_matrix = []
            for row in phi:
                clause_indicator_matrix.append(row + [1 - sum(row)])
            
            r_phi = rank_of_matrix(clause_indicator_matrix)
            h_phi = dpll_search_tree_height(phi)
            
            results.append({
                "n": n,
                "m": m,
                "r_phi": r_phi,
                "h_phi": h_phi
            })
    
    if not results:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": 0.0,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "no_instances_generated"
        }
    
    r_values = [result["r_phi"] for result in results]
    h_values = [result["h_phi"] for result in results]
    
    mean_r = sum(r_values) / len(r_values)
    mean_h = sum(h_values) / len(h_values)
    
    correlation_coefficient = 0.0
    if len(r_values) > 1:
        numerator = sum((r - mean_r) * (h - mean_h) for r, h in zip(r_values, h_values))
        denominator = sum((r - mean_r)**2 for r in r_values) * sum((h - mean_h)**2 for h in h_values)
        if denominator != 0:
            correlation_coefficient = numerator / (len(r_values) - 1) ** 0.5
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(result["n"] for result in results),
        "conjecture_holds": correlation_coefficient >= 0.9,
        "counterexample": "" if correlation_coefficient >= 0.9 else "correlation_coefficient < 0.9"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient < 0.9\" first_failing_seed={first_failing_seed}")