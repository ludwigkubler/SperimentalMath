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
        A = [[0] * (2**n) for _ in range(2**n)]
        for i in range(2**n):
            for j in range(2**n):
                A[i][j] = f[(i & j) ^ (i >> 1)]
        return A
    
    def rank(matrix):
        m, n = len(matrix), len(matrix[0])
        if m == 0 or n == 0:
            return 0
        U = [row[:] for row in matrix]
        r = min(m, n)
        for i in range(r):
            max_idx = i
            for j in range(i+1, m):
                if abs(U[j][i]) > abs(U[max_idx][i]):
                    max_idx = j
            U[i], U[max_idx] = U[max_idx], U[i]
            if U[i][i] == 0:
                r -= 1
                continue
            for j in range(i+1, m):
                factor = U[j][i] / U[i][i]
                for k in range(n):
                    U[j][k] -= factor * U[i][k]
        return sum(1 for row in U if any(row))
    
    def characteristic_polynomial(matrix):
        n = len(matrix)
        A = [[0] * (n+1) for _ in range(n+1)]
        for i in range(n):
            for j in range(n):
                A[i][j] = matrix[i][j]
        for i in range(n):
            A[i][n] = -sum(matrix[i])
        det = 0
        for p in itertools.permutations(range(n)):
            sign = (-1) ** sum(i < p[i] for i in range(n))
            prod = 1
            for i in range(n):
                prod *= A[p[i]][i]
            det += sign * prod
        return det
    
    def grothendieck_witt_class(det):
        if det == 0:
            return 0
        det_abs = abs(det)
        log_det = math.log2(det_abs) if det_abs > 1 else -math.inf
        return log_det
    
    n_values = [5, 10, 15, 20, 30, 40]
    max_rank_diffs = []
    gw_class_logs = []
    
    for n in n_values:
        f = generate_boolean_function(n)
        A = matrix_representation(f, n)
        det = characteristic_polynomial(A)
        gw_class = grothendieck_witt_class(det)
        max_rank = rank(A)
        min_rank = 0
        while True:
            B = [row[:] for row in A]
            random.shuffle(B)
            new_min_rank = rank(B)
            if new_min_rank == min_rank:
                break
            min_rank = new_min_rank
        
        max_rank_diffs.append(max_rank - min_rank)
        gw_class_logs.append(gw_class)
    
    mean_max_rank_diff = sum(max_rank_diffs) / len(max_rank_diffs)
    std_max_rank_diff = math.sqrt(sum((x - mean_max_rank_diff) ** 2 for x in max_rank_diffs) / len(max_rank_diffs))
    correlation_coefficient = sum((gw_class_logs[i] - mean_gw_class_logs) * (max_rank_diffs[i] - mean_max_rank_diff) for i in range(len(gw_class_logs))) / (len(gw_class_logs) * std_gw_class_logs * std_max_rank_diff)
    
    return {
        "metric_name": "communication_complexity_rank_variance",
        "metric_value": mean_max_rank_diff,
        "instances_tested": len(max_rank_diffs),
        "n_max": max(n_values),
        "conjecture_holds": correlation_coefficient >= 0.8,
        "counterexample": "" if correlation_coefficient >= 0.8 else f"Correlation coefficient {correlation_coefficient} < 0.8"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2**i - 1 for i in range(5, 31)]
    
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
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient < 0.8\" first_failing_seed={first_failing_seed}")