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

def gaussian_elimination(A):
    n = len(A)
    for i in range(n):
        max_row = i
        for j in range(i+1, n):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        if A[i][i] == 0:
            continue
        for j in range(n):
            if i != j:
                factor = Fraction(A[j][i], A[i][i])
                for k in range(n+1):
                    A[j][k] -= factor * A[i][k]
    return A

def rank(M):
    n = len(M)
    r = 0
    for i in range(n):
        if all(abs(M[j][i]) == 0 for j in range(r)):
            break
        r += 1
    return r

def communication_complexity(M):
    n = len(M)
    rank_M = rank(M)
    return rank_M * (n - rank_M)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_communication_protocol(n):
        M = [[random.randint(0, 1) for _ in range(n)] for _ in range(n)]
        for i in range(n):
            M[i][i] = 1
        return M
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_points = 0
    total_variance = 0
    instances_tested = 0
    n_max = 0
    
    for n in n_values:
        for _ in range(5):
            M = generate_communication_protocol(n)
            points_required = sum(sum(row) for row in M)
            rank_M = rank(M)
            variance = communication_complexity(M)
            total_points += points_required
            total_variance += variance**2
            instances_tested += 1
            n_max = max(n_max, n)
    
    mean_points = total_points / instances_tested
    mean_variance = total_variance / instances_tested
    
    if n_max < 16:
        return {
            "metric_name": "communication_complexity",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "n_max < 16"
        }
    
    C = math.sqrt(mean_points / mean_variance)
    conjecture_holds = all(C * variance**2 <= points_required for points_required, variance in zip(total_points // instances_tested, total_variance // instances_tested))
    
    return {
        "metric_name": "communication_complexity",
        "metric_value": C,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_C = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_C = math.sqrt(sum((r["metric_value"] - mean_C)**2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_C} std={std_C} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_C} std={std_C} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = "unknown"
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")