# auto-injected by SEC sandbox
import itertools
import collections
import json
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
import sys

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def construct_algebraic_curve(f):
        n = len(f)
        curve = []
        for x in range(2**n):
            y = f[x]
            if y == 0:
                curve.append(x)
            else:
                curve.append(-x)
        return curve
    
    def communication_complexity_rank_variance(curve):
        n = len(curve)
        matrix = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i, n):
                if abs(curve[i]) == abs(curve[j]):
                    matrix[i][j] = 1
                    matrix[j][i] = 1
        rank = gaussian_elimination(matrix)
        return rank
    
    def gaussian_elimination(A):
        m, n = len(A), len(A[0])
        for i in range(m):
            max_row = i
            for j in range(i+1, m):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            if A[i][i] == 0:
                continue
            for j in range(n):
                A[i][j] /= A[i][i]
            for j in range(m):
                if j != i and A[j][i] != 0:
                    factor = A[j][i]
                    for k in range(n):
                        A[j][k] -= factor * A[i][k]
        rank = sum(1 for row in A if any(row))
        return rank
    
    def pearson_correlation(x, y):
        n = len(x)
        mean_x = sum(x) / n
        mean_y = sum(y) / n
        cov = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n)) / n
        std_x = math.sqrt(sum((x[i] - mean_x)**2 for i in range(n)) / n)
        std_y = math.sqrt(sum((y[i] - mean_y)**2 for i in range(n)) / n)
        return cov / (std_x * std_y)
    
    def correlation_check(x, y):
        if len(x) != len(y):
            return False
        corr = pearson_correlation(x, y)
        return abs(corr) > 0.8
    
    n_values = [5, 10, 15, 20, 30, 40]
    curve_ranks = []
    rank_variances = []
    
    for n in n_values:
        f = generate_boolean_function(n)
        curve = construct_algebraic_curve(f)
        rank_variance = communication_complexity_rank_variance(curve)
        curve_ranks.append(len(curve))
        rank_variances.append(rank_variance)
    
    if not correlation_check(curve_ranks, rank_variances):
        return {
            "metric_name": "Pearson Correlation",
            "metric_value": pearson_correlation(curve_ranks, rank_variances),
            "instances_tested": len(n_values),
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "Correlation check failed"
        }
    
    return {
        "metric_name": "Pearson Correlation",
        "metric_value": pearson_correlation(curve_ranks, rank_variances),
        "instances_tested": len(n_values),
        "n_max": max(n_values),
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    if not sys.argv[1:]:
        seeds = [2**i + 3 for i in range(5, 8)]  # Default list of 30 primes
    else:
        seeds = [int(seed) for seed in sys.argv[1:]]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        counterexample = next(r["counterexample"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={seeds[next(i for i, r in enumerate(results) if not r['conjecture_holds'])]}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")