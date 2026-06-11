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
    
    def matrix_multiply(A, B):
        n = len(A)
        result = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    result[i][j] += A[i][k] * B[k][j]
        return result
    
    def gaussian_elimination(matrix):
        n = len(matrix)
        for i in range(n):
            max_row = i
            for j in range(i+1, n):
                if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                    max_row = j
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
            factor = matrix[i][i]
            for j in range(n):
                matrix[i][j] /= factor
            for j in range(n):
                if j != i:
                    factor = matrix[j][i]
                    for k in range(n):
                        matrix[j][k] -= factor * matrix[i][k]
        return matrix
    
    def rank(matrix):
        n = len(matrix)
        rref = gaussian_elimination(matrix)
        rank = 0
        for row in rref:
            if any(row):
                rank += 1
        return rank
    
    def communication_complexity_rank_variance(f, n):
        m = len(f)
        matrix = [[f[i * (2**(n-1)) + j] for i in range(2**(n-1))] for j in range(2**(n-1))]
        r = rank(matrix)
        return r * (m - r) / m
    
    def entropic_quasi_group(f, n):
        m = len(f)
        matrix = [[f[i * (2**(n-1)) + j] for i in range(2**(n-1))] for j in range(2**(n-1))]
        rref = gaussian_elimination(matrix)
        order = 0
        for row in rref:
            if any(row):
                order += 1
        return order
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        f = generate_boolean_function(n)
        rc_f = communication_complexity_rank_variance(f, n)
        eq_f_order = entropic_quasi_group(f, n)
        results.append({
            "n": n,
            "rc_f": rc_f,
            "eq_f_order": eq_f_order
        })
    
    if not results:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": 0.0,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    rc_values = [r["rc_f"] for r in results]
    order_values = [r["eq_f_order"] for r in results]
    correlation_coefficient = sum((rc_values[i] - mean(rc_values)) * (order_values[i] - mean(order_values)) for i in range(len(results))) / math.sqrt(sum((rc_values[i] - mean(rc_values))**2 for i in range(len(results)))) / math.sqrt(sum((order_values[i] - mean(order_values))**2 for i in range(len(results))))
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(r["n"] for r in results),
        "conjecture_holds": abs(correlation_coefficient) >= 0.8 and all(abs(order_values[i]) <= 3 * rc_values[i] for i in range(len(results))),
        "counterexample": "" if correlation_coefficient >= 0.8 else f"correlation_coefficient={correlation_coefficient}"
    }

def mean(values):
    return sum(values) / len(values)

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 1000003) for _ in range(30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if not all(r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{trial_result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        mean_value = mean([r["metric_value"] for r in results])
        std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results)) / len(results)
        support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")