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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def gaussian_elimination(A):
        n = len(A)
        m = len(A[0])
        for i in range(n):
            max_row = i
            for j in range(i+1, n):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            pivot = A[i][i]
            if pivot == 0:
                continue
            for j in range(m):
                A[i][j] /= pivot
            for j in range(n):
                if j != i:
                    factor = A[j][i]
                    for k in range(m):
                        A[j][k] -= factor * A[i][k]
        return A
    
    def is_sat(instance):
        n, m = len(instance), len(instance[0])
        A = [[0] * (n + 1) for _ in range(n)]
        for i in range(n):
            for j in range(m):
                if instance[i][j]:
                    A[i][j] = 1
                    A[i][-1] = 1
        reduced_A = gaussian_elimination(A)
        for row in reduced_A:
            if row[-1] == 1 and all(x == 0 for x in row[:-1]):
                return False
        return True
    
    def clause_set_complexity(instance):
        n, m = len(instance), len(instance[0])
        count = 0
        for i in range(n):
            for j in range(m):
                if instance[i][j]:
                    count += 1
        return count
    
    def generate_instance(n, m):
        return [[random.choice([0, 1]) for _ in range(m)] for _ in range(n)]
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    for n in n_values:
        for _ in range(5):
            instance = generate_instance(n, m)
            if not is_sat(instance):
                continue
            c_phi = clause_set_complexity(instance)
            log_n = math.log(n)
            log_m = math.log(m)
            results.append((log_n, log_m, c_phi))
    
    if len(results) < 30:
        return {
            "metric_name": "Pearson correlation coefficient",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "insufficient_instances"
        }
    
    n = len(results)
    x_sum = sum(x for x, _, _ in results)
    y_sum = sum(y for _, y, _ in results)
    z_sum = sum(c_phi for _, _, c_phi in results)
    xy_sum = sum(x * y for x, y, _ in results)
    xz_sum = sum(x * c_phi for x, _, c_phi in results)
    yz_sum = sum(y * c_phi for _, y, c_phi in results)
    
    x_mean = x_sum / n
    y_mean = y_sum / n
    z_mean = z_sum / n
    
    xy_cov = xy_sum - x_mean * y_mean
    xz_cov = xz_sum - x_mean * z_mean
    yz_cov = yz_sum - y_mean * z_mean
    
    x_var = sum((x - x_mean) ** 2 for x, _, _ in results) / n
    y_var = sum((y - y_mean) ** 2 for _, y, _ in results) / n
    z_var = sum((c_phi - z_mean) ** 2 for _, _, c_phi in results) / n
    
    r_xy = xy_cov / (math.sqrt(x_var * y_var))
    r_xz = xz_cov / (math.sqrt(x_var * z_var))
    r_yz = yz_cov / (math.sqrt(y_var * z_var))
    
    return {
        "metric_name": "Pearson correlation coefficient",
        "metric_value": r_xy,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": r_xy >= 0.7,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all(r["conjecture_holds"] for r in results):
        mean_r_xy = sum(r["metric_value"] for r in results) / len(results)
        std_r_xy = math.sqrt(sum((r["metric_value"] - mean_r_xy) ** 2 for r in results) / len(results))
        support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
        print(f"RESULT: SUPPORTED mean={mean_r_xy} std={std_r_xy} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"r_xy < 0.7\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")