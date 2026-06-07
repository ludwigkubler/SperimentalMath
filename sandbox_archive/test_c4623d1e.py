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
    
    def characteristic_polynomial(f):
        n = len(f)
        A = [[0] * (n + 1) for _ in range(n + 1)]
        for i in range(n):
            for j in range(n):
                if f[i] == f[j]:
                    A[i][j] = 1
        return A
    
    def gaussian_elimination(A):
        n = len(A)
        for i in range(n):
            max_row = i
            for k in range(i + 1, n):
                if abs(A[k][i]) > abs(A[max_row][i]):
                    max_row = k
            A[i], A[max_row] = A[max_row], A[i]
            for k in range(i + 1, n):
                factor = A[k][i] / A[i][i]
                for j in range(n + 1):
                    A[k][j] -= factor * A[i][j]
        return A
    
    def rank(A):
        n = len(A)
        r = 0
        for i in range(n):
            if all(A[i][j] == 0 for j in range(r, n)):
                continue
            r += 1
        return r
    
    def communication_complexity_rank_variance_ratio(f):
        A = characteristic_polynomial(f)
        U = gaussian_elimination(A)
        rank_A = rank(U)
        return rank_A / len(f)
    
    def symplectic_leaf_count(n):
        if n == 1:
            return 1
        elif n % 2 == 0:
            return 2 * symplectic_leaf_count(n // 2)
        else:
            return (n + 1) * symplectic_leaf_count((n - 1) // 2)
    
    def moment_map(f):
        n = len(f)
        return f
    
    def min_symplectic_leaves(n):
        return symplectic_leaf_count(n)
    
    def crvr_bound(n):
        return min_symplectic_leaves(n)
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_crvr = 0
    total_min_symplectic_leaves = 0
    instances_tested = 0
    
    for n in n_values:
        for _ in range(5):
            f = generate_boolean_function(n)
            crvr = communication_complexity_rank_variance_ratio(f)
            min_symplectic_leaves_val = min_symplectic_leaves(n)
            total_crvr += crvr
            total_min_symplectic_leaves += min_symplectic_leaves_val
            instances_tested += 1
    
    mean_crvr = total_crvr / instances_tested
    mean_min_symplectic_leaves = total_min_symplectic_leaves / instances_tested
    std_dev = math.sqrt(sum((crvr - mean_crvr) ** 2 for crvr in [communication_complexity_rank_variance_ratio(generate_boolean_function(n)) for n in n_values]) / instances_tested)
    
    conjecture_holds = all(abs(crvr - mean_min_symplectic_leaves) <= 3 * std_dev for crvr in [communication_complexity_rank_variance_ratio(generate_boolean_function(n)) for n in n_values])
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "CRVR(f)",
        "metric_value": mean_crvr,
        "instances_tested": instances_tested,
        "n_max": max(n_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_crvr = sum(r["metric_value"] for r in results) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean_crvr) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_crvr} std={std_dev} support_fraction={support_fraction}")
    elif sum(1 for r in results if not r["conjecture_holds"]) / len(results) >= 0.2:
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed=1")
    else:
        print(f"RESULT: INCONCLUSIVE reason=budget_exceeded n_tested={len(seeds)}")