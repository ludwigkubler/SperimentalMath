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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def communication_complexity_rank(f):
        n = len(f)
        rank = 0
        for i in range(n):
            if f[i] != f[0]:
                rank += 1
        return rank
    
    def matrix_representation(f, n):
        m = [[0]*n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                if (i & j) == 0:
                    m[i][j] = f[i]
        return m
    
    def gaussian_elimination(A):
        m, n = len(A), len(A[0])
        rank = 0
        for i in range(m):
            if A[i][rank] == 0:
                swap_found = False
                for j in range(i+1, m):
                    if A[j][rank] != 0:
                        A[i], A[j] = A[j], A[i]
                        swap_found = True
                        break
                if not swap_found:
                    continue
            pivot = Fraction(A[i][rank])
            for j in range(n):
                A[i][j] /= pivot
            for j in range(m):
                if j != i and A[j][rank] != 0:
                    factor = -A[j][rank]
                    for k in range(n):
                        A[j][k] += factor * A[i][k]
            rank += 1
        return rank
    
    def minimal_order_of_brauer_group(f, n):
        m = matrix_representation(f, n)
        rank = gaussian_elimination(m)
        return rank
    
    def log_base_2(x):
        if x <= 0:
            return None
        count = 0
        while x > 1:
            x /= 2
            count += 1
        return count
    
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        f = generate_boolean_function(n)
        r_f = communication_complexity_rank(f)
        order = minimal_order_of_brauer_group(f, n)
        if order is not None:
            results.append((n, order))
    
    if len(results) < 30:
        return {
            "metric_name": "Minimal Order of Brauer Groups",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max(n for n, _ in results),
            "conjecture_holds": False,
            "counterexample": "Insufficient instances tested"
        }
    
    total_order = sum(order for _, order in results)
    mean_order = Fraction(total_order, len(results))
    log_r_f_values = [log_base_2(r_f) for n, r_f in results if r_f > 0]
    if not log_r_f_values:
        return {
            "metric_name": "Minimal Order of Brauer Groups",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max(n for n, _ in results),
            "conjecture_holds": False,
            "counterexample": "No valid r_f values found"
        }
    
    total_log_r_f = sum(log_r_f for log_r_f in log_r_f_values)
    mean_log_r_f = Fraction(total_log_r_f, len(log_r_f_values))
    
    conjecture_holds = all(order <= 2**log_r_f for n, order in results if r_f > 0)
    
    return {
        "metric_name": "Minimal Order of Brauer Groups",
        "metric_value": mean_order,
        "instances_tested": len(results),
        "n_max": max(n for n, _ in results),
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else "Mapping undefined"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 7 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all("conjecture_holds" in result and result["conjecture_holds"] for result in results):
        mean_value = sum(result["metric_value"] for result in results) / len(results)
        std_value = (sum((result["metric_value"] - mean_value)**2 for result in results) / len(results))**0.5
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any("conjecture_holds" in result and not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if "conjecture_holds" in result and not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='Mapping undefined' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")