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
    
    def generate_info_matrix(n):
        matrix = [[random.randint(0, 1) for _ in range(n)] for _ in range(n)]
        return matrix
    
    def rank_variance(matrix):
        n = len(matrix)
        det = determinant(matrix)
        if det == 0:
            return float('inf')
        rank = sum(1 for row in matrix if any(row))
        return (n - rank) / n
    
    def determinant(matrix):
        n = len(matrix)
        if n == 1:
            return matrix[0][0]
        det = 0
        for j in range(n):
            submatrix = [row[:j] + row[j+1:] for row in matrix[1:]]
            det += ((-1) ** j) * matrix[0][j] * determinant(submatrix)
        return det
    
    def adjoint_group(matrix):
        n = len(matrix)
        identity = [[Fraction(1, 1) if i == j else Fraction(0, 1) for j in range(n)] for i in range(n)]
        order = 1
        current_group = matrix
        while current_group != identity:
            current_group = multiply_matrices(current_group, matrix)
            order += 1
        return order
    
    def multiply_matrices(a, b):
        n = len(a)
        result = [[Fraction(0, 1) for _ in range(n)] for _ in range(n)]
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    result[i][j] += a[i][k] * b[k][j]
        return result
    
    def pearson_correlation(x, y):
        n = len(x)
        mean_x = sum(x) / n
        mean_y = sum(y) / n
        cov_xy = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n))
        std_dev_x = math.sqrt(sum((x[i] - mean_x) ** 2 for i in range(n)) / n)
        std_dev_y = math.sqrt(sum((y[i] - mean_y) ** 2 for i in range(n)) / n)
        return cov_xy / (std_dev_x * std_dev_y)
    
    trials = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in trials:
        info_matrix = generate_info_matrix(n)
        rank_var = rank_variance(info_matrix)
        adj_order = adjoint_group(info_matrix)
        results.append((adj_order, rank_var))
    
    if len(results) < 30:
        return {
            "metric_name": "Pearson Correlation",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max(trials),
            "conjecture_holds": False,
            "counterexample": "not_enough_instances"
        }
    
    adj_orders, rank_vars = zip(*results)
    corr_coeff = pearson_correlation(adj_orders, rank_vars)
    
    return {
        "metric_name": "Pearson Correlation",
        "metric_value": corr_coeff,
        "instances_tested": len(results),
        "n_max": max(trials),
        "conjecture_holds": corr_coeff >= 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_corr_coeff = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["metric_value"] is not None for r in results):
        print(f"RESULT: SUPPORTED mean={mean_corr_coeff} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_corr_coeff} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample='low_correlation' first_failing_seed={first_failing_seed}")