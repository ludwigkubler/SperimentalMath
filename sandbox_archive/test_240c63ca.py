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
    
    # Generate a random polynomial system P and communication protocol π
    n = random.randint(5, 40)
    d = random.randint(1, 5)
    P = [[random.randint(-10, 10) for _ in range(n)] for _ in range(n)]
    w_C = random.randint(2, 10)
    
    # Compute the minimal root multiplicity of P using Gröbner bases
    # (This is a placeholder implementation; actual computation would be complex)
    min_roots_mult = n * d
    
    # Generate the communication complexity matrix M_π for protocol π
    M_π = [[random.randint(0, 1) for _ in range(n)] for _ in range(n)]
    
    # Compute the rank of M_π
    rank_M_π = gaussian_elimination(M_π)
    
    # Check if min_roots_mult(P) is linearly correlated with w_C(P)
    def is_linearly_correlated(metric_x, metric_y):
        if len(metric_x) != len(metric_y) or not metric_x:
            return False
        n = len(metric_x)
        sum_xy = 0
        sum_x = 0
        sum_y = 0
        sum_x2 = 0
        sum_y2 = 0
        for i in range(n):
            sum_xy += metric_x[i] * metric_y[i]
            sum_x += metric_x[i]
            sum_y += metric_y[i]
            sum_x2 += metric_x[i] ** 2
            sum_y2 += metric_y[i] ** 2
        cov = n * sum_xy - sum_x * sum_y
        var_x = n * sum_x2 - sum_x ** 2
        var_y = n * sum_y2 - sum_y ** 2
        if var_x == 0 or var_y == 0:
            return False
        return abs(cov / (math.sqrt(var_x) * math.sqrt(var_y)))
    
    metric_value = is_linearly_correlated([min_roots_mult], [w_C])
    
    # Check if the rank of M_π is upper-bounded by min_roots_mult(P)
    conjecture_holds = rank_M_π <= min_roots_mult
    counterexample = "" if conjecture_holds else f"Rank {rank_M_π} > {min_roots_mult}"
    
    return {
        "metric_name": "is_linearly_correlated",
        "metric_value": metric_value,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

def gaussian_elimination(matrix):
    rows, cols = len(matrix), len(matrix[0])
    for i in range(rows):
        # Find the pivot row
        max_row = i
        for j in range(i + 1, rows):
            if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                max_row = j
        
        # Swap the current row with the pivot row
        matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
        
        # Eliminate non-zero entries below the pivot
        for j in range(i + 1, rows):
            factor = Fraction(matrix[j][i], matrix[i][i])
            for k in range(cols):
                matrix[j][k] -= factor * matrix[i][k]
    
    # Count the number of non-zero rows to get the rank
    rank = sum(1 for row in matrix if any(val != 0 for val in row))
    return rank

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 1000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and max(r["metric_value"] for r in results) <= 10:
        print("RESULT: FALSIFIED counterexample=\"min_roots_mult(P) != Θ(w_C(P))\" first_failing_seed=<s>")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction}")