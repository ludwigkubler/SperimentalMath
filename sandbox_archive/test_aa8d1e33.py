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
    
    def communication_complexity(f):
        n = int(math.log2(len(f)))
        C = [[0] * (2**(n-1)) for _ in range(2**(n-1))]
        for i in range(2**(n-1)):
            for j in range(2**(n-1)):
                x = [i & (1 << k) for k in range(n)]
                y = [j & (1 << k) for k in range(n)]
                C[i][j] = f[x.index(0)] ^ f[y.index(0)]
        return C
    
    def rank(matrix):
        m, n = len(matrix), len(matrix[0])
        if m == 0 or n == 0:
            return 0
        for i in range(m):
            if matrix[i][i] == 0:
                found = False
                for j in range(i+1, m):
                    if matrix[j][i] != 0:
                        matrix[i], matrix[j] = matrix[j], matrix[i]
                        found = True
                        break
                if not found:
                    return rank(matrix[:i] + matrix[i+1:])
            for j in range(n):
                if i != j and matrix[i][j] != 0:
                    factor = -matrix[j][i] / matrix[i][i]
                    for k in range(n):
                        matrix[j][k] += factor * matrix[i][k]
        rank = sum(1 for row in matrix if any(row))
        return rank
    
    def min_non_degenerate_representation(f):
        n = int(math.log2(len(f)))
        V = [f[x.index(0)] for x in range(2**n)]
        basis = []
        for v in V:
            if all(v != sum(b * b_i for b, b_i in zip(basis, v)) for b in basis):
                basis.append(v)
        return len(basis)
    
    def variance(lst):
        mean = sum(lst) / len(lst)
        return sum((x - mean)**2 for x in lst) / len(lst)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        f = generate_boolean_function(n)
        C = communication_complexity(f)
        sigma_min = min_non_degenerate_representation(f)
        rank_C = rank(C)
        results.append((n, sigma_min, rank_C))
    
    if len(results) < 30:
        return {
            "metric_name": "sigma_min/variance",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max(n for n, _, _ in results),
            "conjecture_holds": False,
            "counterexample": "not_enough_instances"
        }
    
    sigma_mins = [sigma_min for _, sigma_min, _ in results]
    variances = [variance([rank_C for _, _, rank_C in results])]
    ratio = sum(sigma_mins) / sum(variances)
    
    return {
        "metric_name": "sigma_min/variance",
        "metric_value": ratio,
        "instances_tested": len(results),
        "n_max": max(n for n, _, _ in results),
        "conjecture_holds": ratio <= 10**6 * n_values[-1],
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
    
    mean_ratio = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_deviation = math.sqrt(sum((r["metric_value"] - mean_ratio)**2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std={std_deviation} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_ratio} std={std_deviation} support_fraction={support_fraction}")
    else:
        for r in results:
            if not r["conjecture_holds"]:
                print(f"RESULT: FALSIFIED counterexample=\"sigma_min/variance does not match\" first_failing_seed={r['seed']}")
                break