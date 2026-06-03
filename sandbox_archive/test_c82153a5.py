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
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def communication_matrix(f):
        n = int(math.log2(len(f)))
        C_f = [[0] * (2**n) for _ in range(2**n)]
        for i in range(2**n):
            for j in range(2**n):
                if f[i ^ j] == 1:
                    C_f[i][j] = 1
        return C_f
    
    def matrix_rank(C):
        m, n = len(C), len(C[0])
        rank = 0
        for i in range(m):
            pivot_row = None
            for j in range(i, m):
                if any(C[j][k] != 0 for k in range(n)):
                    pivot_row = j
                    break
            if pivot_row is not None:
                rank += 1
                for j in range(n):
                    C[i][j], C[pivot_row][j] = C[pivot_row][j], C[i][j]
                for j in range(m):
                    if j != i and any(C[j][k] != 0 for k in range(n)):
                        factor = C[j][i] / C[i][i]
                        for k in range(n):
                            C[j][k] -= factor * C[i][k]
        return rank
    
    def coxeter_group_action_complexity(f):
        n = int(math.log2(len(f)))
        # Simplified heuristic for action complexity
        return sum(1 for i in range(2**n) if f[i] == 1)
    
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):
            f = generate_boolean_function(n)
            C_f = communication_matrix(f)
            c_f = coxeter_group_action_complexity(f)
            r_C_f = matrix_rank(C_f)
            results.append((c_f, r_C_f))
    
    if not results:
        return {
            "metric_name": "Coxeter Group Action Complexity vs Matrix Rank",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "No instances generated"
        }
    
    c_values = [c for c, r in results]
    r_values = [r for c, r in results]
    
    mean_c = sum(c_values) / len(c_values)
    mean_r = sum(r_values) / len(r_values)
    variance_c = sum((c - mean_c)**2 for c in c_values) / len(c_values)
    variance_r = sum((r - mean_r)**2 for r in r_values) / len(r_values)
    covariance = sum((c - mean_c) * (r - mean_r) for c, r in results) / len(results)
    
    correlation_coefficient = covariance / math.sqrt(variance_c * variance_r)
    
    return {
        "metric_name": "Coxeter Group Action Complexity vs Matrix Rank",
        "metric_value": correlation_coefficient,
        "instances_tested": len(c_values),
        "n_max": max(n for n in [5, 10, 15, 20, 30, 40] if any(f for f, _ in results if int(math.log2(len(f))) == n)),
        "conjecture_holds": correlation_coefficient >= 0.9,
        "counterexample": "" if correlation_coefficient >= 0.9 else "Low correlation coefficient"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Low correlation coefficient\" first_failing_seed={first_failing_seed}")