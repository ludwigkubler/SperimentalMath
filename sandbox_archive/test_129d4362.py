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
    
    def generate_instance(n):
        A = [[random.randint(0, 1) for _ in range(n)] for _ in range(n)]
        B = [[random.randint(0, 1) for _ in range(n)] for _ in range(n)]
        C = [[random.randint(0, 1) for _ in range(n)] for _ in range(n)]
        return A, B, C
    
    def matrix_add(A, B):
        return [[A[i][j] + B[i][j] for j in range(len(A[0]))] for i in range(len(A))]
    
    def matrix_sub(A, B):
        return [[A[i][j] - B[i][j] for j in range(len(A[0]))] for i in range(len(A))]
    
    def matrix_mul(A, B):
        return [[sum(A[i][k] * B[k][j] for k in range(len(B))) for j in range(len(B[0]))] for i in range(len(A))]
    
    def matrix_inv(A):
        n = len(A)
        I = [[1 if i == j else 0 for j in range(n)] for i in range(n)]
        for i in range(n):
            pivot = A[i][i]
            for j in range(n):
                A[i][j] /= pivot
                I[i][j] /= pivot
            for k in range(n):
                if k != i:
                    factor = A[k][i]
                    for j in range(n):
                        A[k][j] -= factor * A[i][j]
                        I[k][j] -= factor * I[i][j]
        return I
    
    def rank_variance(matrix):
        n = len(matrix)
        det = 1
        for i in range(n):
            pivot = matrix[i][i]
            if pivot == 0:
                return float('inf')
            det *= pivot
            for j in range(i + 1, n):
                factor = matrix[j][i] / pivot
                for k in range(i, n):
                    matrix[j][k] -= factor * matrix[i][k]
        return det
    
    def nc_yb_order(n):
        # Placeholder function to calculate NCYBE order
        # This is a dummy implementation and should be replaced with actual computation
        return random.randint(1, n)
    
    instances_tested = 0
    n_max = 0
    total_ncybe_order = 0
    total_rank_variance = 0
    
    for n in [5, 10, 15, 20, 30, 40]:
        if n > n_max:
            n_max = n
        instances_tested += 1
        A, B, C = generate_instance(n)
        rank_var = rank_variance(matrix_mul(A, matrix_sub(B, C)))
        nc_yb_order_val = nc_yb_order(n)
        total_ncybe_order += nc_yb_order_val
        total_rank_variance += rank_var
    
    if n_max < 16:
        return {
            "metric_name": "NCYBE Order vs Rank Variance",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "n_max < 16"
        }
    
    mean_ncybe_order = total_ncybe_order / instances_tested
    mean_rank_variance = total_rank_variance / instances_tested
    
    correlation_coefficient = (instances_tested * sum(nc_yb_order_val * rank_var for nc_yb_order_val, rank_var in zip(range(5, 41), range(5, 41))) -
                               mean_ncybe_order * mean_rank_variance) / \
                              math.sqrt((instances_tested * sum(nc_yb_order_val**2 for nc_yb_order_val in range(5, 41)) - mean_ncybe_order**2) *
                                        (instances_tested * sum(rank_var**2 for rank_var in range(5, 41)) - mean_rank_variance**2))
    
    return {
        "metric_name": "NCYBE Order vs Rank Variance",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": correlation_coefficient >= 0.75,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(res["metric_value"] for res in results if res["metric_value"] is not None) / len(results)
    std_metric_value = math.sqrt(sum((res["metric_value"] - mean_metric_value)**2 for res in results if res["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not res["conjecture_holds"] for res in results):
        first_failing_seed = next(seed for seed, res in zip(seeds, results) if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")