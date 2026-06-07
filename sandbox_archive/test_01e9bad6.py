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
    
    def matrix_representation(f, n):
        A = []
        for i in range(2**n):
            row = []
            for j in range(2**n):
                x = bin(i)[2:].zfill(n)
                y = bin(j)[2:].zfill(n)
                z = ''.join(str(int(x[k]) ^ int(y[k])) for k in range(n))
                row.append(f[int(z, 2)])
            A.append(row)
        return A
    
    def p_adic_valuation_degree(A, p):
        n = len(A)
        max_val = 0
        for i in range(n):
            for j in range(n):
                if A[i][j] != 0:
                    val = 0
                    while A[i][j] % p == 0:
                        A[i][j] //= p
                        val += 1
                    max_val = max(max_val, val)
        return max_val
    
    def communication_complexity_rank(A):
        n = len(A)
        rank = 0
        for i in range(n):
            if any(A[j][i] != 0 for j in range(n)):
                rank += 1
        return rank
    
    p = 2  # Fixed prime for p-adic valuation
    n_values = [5, 10, 15, 20, 30, 40]
    total_ratio = 0
    instances_tested = 0
    n_max = 0
    
    for n in n_values:
        for _ in range(5):  # Ensure at least 30 instances per seed
            f = generate_boolean_function(n)
            A = matrix_representation(f, n)
            vd_p_f = p_adic_valuation_degree(A, p)
            cr_f = communication_complexity_rank(A)
            if vd_p_f != 0 and cr_f != 0:
                ratio = vd_p_f / cr_f
                total_ratio += ratio
                instances_tested += 1
                n_max = max(n_max, n)
    
    if instances_tested == 0:
        return {
            "metric_name": "vd_p(f) / cr_f",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "No valid instances found"
        }
    
    avg_ratio = total_ratio / instances_tested
    return {
        "metric_name": "vd_p(f) / cr_f",
        "metric_value": avg_ratio,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": 0.7 < avg_ratio <= 0.3,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    avg_metric_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - avg_metric_value)**2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={avg_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={avg_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in enumerate(results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")