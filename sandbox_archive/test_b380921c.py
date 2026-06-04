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
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def communication_complexity_rank(f):
        n = len(f)
        rank = 0
        for i in range(2**(n-1)):
            a = f[i:i+n//2]
            b = f[i+n//2:i+n]
            if all(a[j] != b[j] for j in range(n//2)):
                rank += 1
        return rank
    
    def eta_invariant(f):
        n = len(f)
        matrix = [[f[i] ^ f[j] for j in range(n)] for i in range(n)]
        det = determinant(matrix)
        if det == 0:
            return None
        return Fraction(det, 2**n)
    
    def determinant(matrix):
        n = len(matrix)
        if n == 1:
            return matrix[0][0]
        det = 0
        for j in range(n):
            submatrix = [row[:j] + row[j+1:] for row in matrix[1:]]
            det += (-1)**j * matrix[0][j] * determinant(submatrix)
        return det
    
    n_values = [5, 10, 15, 20, 30, 40]
    eta_values = []
    rank_values = []
    
    for n in n_values:
        f = generate_boolean_function(n)
        rank = communication_complexity_rank(f)
        eta = eta_invariant(f)
        if eta is not None:
            eta_values.append(eta)
            rank_values.append(rank)
    
    if len(eta_values) < 30 or len(rank_values) < 30:
        return {
            "metric_name": "communication_complexity_rank",
            "metric_value": None,
            "instances_tested": len(eta_values),
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "not_enough_instances"
        }
    
    correlation_coefficient = pearson_correlation(eta_values, rank_values)
    p_value = t_statistic(correlation_coefficient, len(eta_values) - 2)
    
    return {
        "metric_name": "communication_complexity_rank",
        "metric_value": correlation_coefficient,
        "instances_tested": len(eta_values),
        "n_max": max(n_values),
        "conjecture_holds": correlation_coefficient >= 0.7 and p_value <= 0.05,
        "counterexample": "" if correlation_coefficient >= 0.7 else f"correlation_coefficient={correlation_coefficient}"
    }

def pearson_correlation(x, y):
    n = len(x)
    mean_x = sum(x) / n
    mean_y = sum(y) / n
    cov_xy = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n)) / n
    std_dev_x = math.sqrt(sum((x[i] - mean_x)**2 for i in range(n)) / n)
    std_dev_y = math.sqrt(sum((y[i] - mean_y)**2 for i in range(n)) / n)
    return cov_xy / (std_dev_x * std_dev_y)

def t_statistic(r, n):
    if r == 0:
        return 0
    return r * math.sqrt((n - 2) / (1 - r**2))

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [37, 61, 73, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199, 211, 223, 227, 229]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all(result["conjecture_holds"] for result in results):
        mean_value = sum(result["metric_value"] for result in results) / len(results)
        std_dev = math.sqrt(sum((result["metric_value"] - mean_value)**2 for result in results) / len(results))
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] and result["counterexample"] != "" for result in results):
        counterexample = next(result["counterexample"] for result in results if not result["conjecture_holds"] and result["counterexample"] != "")
        first_failing_seed = next(result["seed"] for result in results if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")
    else:
        support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction}")