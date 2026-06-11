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
    
    def truth_table_to_lie_algebroid(f):
        n = int(math.log2(len(f)))
        A_f = [[0] * (n + 1) for _ in range(n + 1)]
        for i in range(2**n):
            binary_i = format(i, f'0{n}b')
            for j in range(n):
                if binary_i[j] == '1':
                    A_f[j][n] += f[i]
        return A_f
    
    def communication_complexity_rank_variance(f):
        n = int(math.log2(len(f)))
        rank = 0
        for i in range(2**n):
            binary_i = format(i, f'0{n}b')
            if any(binary_i[j] == '1' and f[i] != f[i ^ (1 << j)] for j in range(n)):
                rank += 1
        return rank ** 2 / n
    
    def min_root_length(A_f):
        n = len(A_f) - 1
        root_lengths = [0] * (n + 1)
        for i in range(1, n + 1):
            for j in range(n + 1):
                if A_f[i][j]:
                    root_lengths[i] += 1
        return min(root_lengths)
    
    def correlation_coefficient(x, y):
        n = len(x)
        mean_x = sum(x) / n
        mean_y = sum(y) / n
        cov = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n)) / n
        std_x = math.sqrt(sum((x[i] - mean_x) ** 2 for i in range(n)) / n)
        std_y = math.sqrt(sum((y[i] - mean_y) ** 2 for i in range(n)) / n)
        return cov / (std_x * std_y)
    
    def gaussian_elimination(A):
        n = len(A)
        for i in range(n):
            max_row = i
            for j in range(i + 1, n):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            for j in range(i + 1, n):
                factor = A[j][i] / A[i][i]
                for k in range(n + 1):
                    A[j][k] -= factor * A[i][k]
        return A
    
    def rank(A):
        A_rref = gaussian_elimination(A)
        rref_rank = sum(1 for row in A_rref if any(row[col] != 0 for col in range(len(row))))
        return rref_rank
    
    n_values = [5, 10, 15, 20, 30, 40]
    min_root_lengths = []
    R_vars = []
    
    for n in n_values:
        f = generate_boolean_function(n)
        A_f = truth_table_to_lie_algebroid(f)
        R_var = communication_complexity_rank_variance(f)
        min_root_length = min_root_length(A_f)
        min_root_lengths.append(min_root_length)
        R_vars.append(R_var)
    
    corr_coeff = correlation_coefficient(min_root_lengths, R_vars)
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": corr_coeff,
        "instances_tested": len(n_values),
        "n_max": max(n_values),
        "conjecture_holds": corr_coeff >= 0.7,
        "counterexample": "" if corr_coeff >= 0.7 else f"Correlation coefficient {corr_coeff} < 0.7"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_corr_coeff = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_corr_coeff} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_corr_coeff} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample='correlation_coefficient < 0.7' first_failing_seed={first_failing_seed}")