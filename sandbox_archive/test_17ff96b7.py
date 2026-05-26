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
    
    def gaussian_elimination(A):
        m, n = len(A), len(A[0])
        rank = 0
        for i in range(n):
            if rank >= m:
                break
            pivot_row = -1
            for j in range(rank, m):
                if A[j][i] != 0:
                    pivot_row = j
                    break
            if pivot_row == -1:
                continue
            A[rank], A[pivot_row] = A[pivot_row], A[rank]
            for j in range(n):
                if j != i and A[rank][j] != 0:
                    factor = A[j][i] / A[rank][i]
                    for k in range(n):
                        A[j][k] -= factor * A[rank][k]
            rank += 1
        return rank
    
    def min_rank_quadratic_form(M):
        n = len(M)
        F = [[0] * (n * n) for _ in range(n * n)]
        for i in range(n):
            for j in range(n):
                if M[i][j]:
                    idx = i * n + j
                    F[idx][idx] += 1
                    for k in range(i, n):
                        for l in range(j, n):
                            F[idx][k * n + l] += M[k][l]
                            F[k * n + l][idx] += M[k][l]
        return gaussian_elimination(F)
    
    def tensor_product_valuation(M1, M2):
        n = len(M1)
        result = [[0] * (n * n) for _ in range(n * n)]
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    for l in range(n):
                        result[i * n + j][k * n + l] = M1[i][k] * M2[j][l]
        return result
    
    def log_n(n):
        if n <= 0:
            return float('-inf')
        return math.log(n)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    for n in n_values:
        M1 = [[random.randint(0, 1) for _ in range(n)] for _ in range(n)]
        M2 = [[random.randint(0, 1) for _ in range(n)] for _ in range(n)]
        T = tensor_product_valuation(M1, M2)
        rank = min_rank_quadratic_form(T)
        results.append((n, rank))
    
    if not results:
        return {
            "metric_name": "min_rank",
            "metric_value": float('nan'),
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    min_rank = min(results, key=lambda x: x[1])[1]
    max_rank = max(results, key=lambda x: x[1])[1]
    avg_rank = sum(x[1] for x in results) / len(results)
    std_dev = math.sqrt(sum((x[1] - avg_rank) ** 2 for x in results) / len(results))
    
    expected_min_rank = log_n(n_values[-1])
    expected_max_rank = 2 * log_n(n_values[-1])
    
    if min_rank < expected_min_rank or max_rank > expected_max_rank:
        return {
            "metric_name": "min_rank",
            "metric_value": avg_rank,
            "instances_tested": len(results),
            "conjecture_holds": False,
            "counterexample": f"Rank out of bounds: min={min_rank}, max={max_rank}"
        }
    
    return {
        "metric_name": "min_rank",
        "metric_value": avg_rank,
        "instances_tested": len(results),
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    avg_metric = sum(x['metric_value'] for x in results) / len(results)
    std_metric = math.sqrt(sum((x['metric_value'] - avg_metric) ** 2 for x in results) / len(results))
    support_fraction = sum(1 for x in results if x['conjecture_holds']) / len(results)
    
    if all(x['conjecture_holds'] for x in results):
        print(f"RESULT: SUPPORTED mean={avg_metric} std={std_metric} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={avg_metric} std={std_metric} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(x['seed'] for x in results if not x['conjecture_holds'])
        counterexample = next(x['counterexample'] for x in results if x['counterexample'])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")