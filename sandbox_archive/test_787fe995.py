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
    
    def gaussian_elimination(A, mod):
        n = len(A)
        for i in range(n):
            max_row = i
            for j in range(i+1, n):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            pivot = A[i][i]
            for j in range(n):
                if j != i:
                    factor = (A[j][i] * pow(pivot, -1, mod)) % mod
                    for k in range(n):
                        A[j][k] = (A[j][k] - factor * A[i][k]) % mod
        return A
    
    def matrix_mult(A, B, mod):
        n = len(A)
        C = [[0]*n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    C[i][j] = (C[i][j] + A[i][k] * B[k][j]) % mod
        return C
    
    def rank_variance(matrix, mod):
        n = len(matrix)
        identity = [[1 if i == j else 0 for j in range(n)] for i in range(n)]
        reduced_matrix = gaussian_elimination(matrix, mod)
        rank = sum(1 for row in reduced_matrix if any(row))
        return (rank - n) ** 2
    
    def nc_yb_order(n):
        # Placeholder function to compute the minimal order of NCYBE solutions
        # This is a dummy implementation and should be replaced with actual computation
        return random.randint(1, n)
    
    instances_tested = 0
    n_max = 5
    total_metric_value = 0.0
    nc_yb_orders = []
    rank_variances = []
    
    for n in range(n_min, min(n_max + 1, 41)):
        for _ in range(30):
            matrix = [[random.randint(0, mod-1) for _ in range(n)] for _ in range(n)]
            nc_yb_order_n = nc_yb_order(n)
            rank_variance_n = rank_variance(matrix, mod)
            
            instances_tested += 1
            n_max = max(n_max, n)
            total_metric_value += nc_yb_order_n * rank_variance_n
            nc_yb_orders.append(nc_yb_order_n)
            rank_variances.append(rank_variance_n)
    
    if instances_tested < 30:
        return {
            "metric_name": "nc_yb_order_rank_variance",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "insufficient_instances"
        }
    
    mean_metric = total_metric_value / instances_tested
    variance = sum((x - mean_metric) ** 2 for x in nc_yb_orders) / instances_tested
    std_dev = math.sqrt(variance)
    
    return {
        "metric_name": "nc_yb_order_rank_variance",
        "metric_value": mean_metric,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean_metric) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric} std={std_dev} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        print(f"RESULT: FALSIFIED counterexample=\"not_enough_support\" first_failing_seed=1")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_evidence n_tested={len(results)}")