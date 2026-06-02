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
    
    def generate_random_code(n):
        return [random.randint(0, 1) for _ in range(n)]
    
    def communication_complexity_rank(code):
        n = len(code)
        rank = 1
        for i in range(1, n):
            if all(code[j] != code[(j + i) % n] for j in range(i)):
                rank += 1
        return rank
    
    def minimal_p_adic_rank(code):
        n = len(code)
        p = 2
        min_rank = float('inf')
        for i in range(n):
            matrix = [[0] * (n + 1) for _ in range(n)]
            for j in range(n):
                matrix[j][i] = code[(j - i) % n]
            matrix[n][i] = 1
            rank = gaussian_elimination(matrix)
            min_rank = min(min_rank, rank)
        return min_rank
    
    def gaussian_elimination(A):
        m, n = len(A), len(A[0])
        for j in range(n - 1):
            pivot_row = j
            for i in range(j + 1, m):
                if abs(A[i][j]) > abs(A[pivot_row][j]):
                    pivot_row = i
            A[j], A[pivot_row] = A[pivot_row], A[j]
            if A[j][j] == 0:
                continue
            for i in range(j + 1, m):
                factor = A[i][j] / A[j][j]
                for k in range(n):
                    A[i][k] -= factor * A[j][k]
        rank = sum(1 for row in A if any(row[i] != 0 for i in range(n)))
        return rank
    
    n_values = [5, 10, 15, 20, 30, 40]
    min_ranks = []
    comm_complexity_ranks = []
    
    for n in n_values:
        code = generate_random_code(n)
        min_rank = minimal_p_adic_rank(code)
        comm_complexity_rank_val = communication_complexity_rank(code)
        
        min_ranks.append(min_rank)
        comm_complexity_ranks.append(comm_complexity_rank_val)
    
    correlation_coefficient = calculate_correlation(min_ranks, comm_complexity_ranks)
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(n_values),
        "n_max": max(n_values),
        "conjecture_holds": correlation_coefficient >= 0.7 and all(ccr >= 0.5 for ccr in comm_complexity_ranks),
        "counterexample": "" if correlation_coefficient >= 0.7 else f"correlation below 0.5 at n={n_values[comm_complexity_ranks.index(min(comm_complexity_ranks))]}"
    }

def calculate_correlation(x, y):
    n = len(x)
    mean_x = sum(x) / n
    mean_y = sum(y) / n
    cov_xy = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n)) / n
    std_x = math.sqrt(sum((x[i] - mean_x) ** 2 for i in range(n)) / n)
    std_y = math.sqrt(sum((y[i] - mean_y) ** 2 for i in range(n)) / n)
    return cov_xy / (std_x * std_y)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        seeds = [int(s) for s in sys.argv[1:]]
    else:
        primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
        seeds = random.sample(primes, 30)
    
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
    elif any(not r["conjecture_holds"] and r["counterexample"] != "" for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_evidence n_tested={len(results)}")