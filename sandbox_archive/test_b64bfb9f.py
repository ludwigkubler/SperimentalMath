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
        S = [(i >> j & 1 for j in range(n)) for i in range(2**n)]
        M = [[f(tuple(S[i])) == f(tuple(S[j])) for j in range(2**n)] for i in range(2**n)]
        return M
    
    def geometric_fluctuation(M):
        n = len(M)
        total = 0
        for i in range(n):
            for j in range(i+1, n):
                if M[i][j] != M[j][i]:
                    total += abs(i - j)
        return total / (n * (n - 1) / 2)
    
    def rank(matrix):
        n = len(matrix)
        A = [row[:] for row in matrix]
        pivot_row = 0
        for i in range(n):
            if pivot_row >= n:
                break
            max_abs = abs(A[i][pivot_row])
            max_row = i
            for j in range(i+1, n):
                if abs(A[j][pivot_row]) > max_abs:
                    max_abs = abs(A[j][pivot_row])
                    max_row = j
            if max_abs == 0:
                pivot_row += 1
                continue
            A[i], A[max_row] = A[max_row], A[i]
            for j in range(i+1, n):
                factor = A[j][pivot_row] / A[i][pivot_row]
                for k in range(n):
                    A[j][k] -= factor * A[i][k]
            pivot_row += 1
        rank = sum(1 for row in A if any(row))
        return rank
    
    def correlation(x, y):
        n = len(x)
        mean_x = sum(x) / n
        mean_y = sum(y) / n
        cov = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n)) / n
        std_x = math.sqrt(sum((x[i] - mean_x)**2 for i in range(n)) / n)
        std_y = math.sqrt(sum((y[i] - mean_y)**2 for i in range(n)) / n)
        return cov / (std_x * std_y) if std_x * std_y != 0 else 0
    
    results = []
    n_values = [5, 10, 15, 20, 30, 40]
    
    for n in n_values:
        f = generate_boolean_function(n)
        M = matrix_representation(f, n)
        G_f = geometric_fluctuation(M)
        rank_f = rank(M)
        results.append((G_f, rank_f))
    
    if len(results) < 100:
        return {
            "metric_name": "correlation",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "not_enough_instances"
        }
    
    G_f_values, rank_f_values = zip(*results)
    corr_coeff = correlation(G_f_values, rank_f_values)
    
    return {
        "metric_name": "correlation",
        "metric_value": corr_coeff,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": corr_coeff > 0.9,
        "counterexample": "" if corr_coeff > 0.9 else f"corr_coeff={corr_coeff}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all(result["conjecture_holds"] for result in results):
        mean_corr_coeff = sum(result["metric_value"] for result in results) / len(results)
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_corr_coeff} std=0.0 support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")