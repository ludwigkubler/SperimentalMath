# auto-injected by SEC sandbox
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from itertools import combinations

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def gaussian_elimination(A):
        m, n = len(A), len(A[0])
        rank = 0
        for j in range(n):
            i_max = next((i for i in range(rank, m) if A[i][j] != 0), None)
            if i_max is not None:
                A[rank], A[i_max] = A[i_max], A[rank]
                for i in range(m):
                    if i != rank and A[i][j] != 0:
                        factor = -A[i][j] / A[rank][j]
                        for k in range(n):
                            A[i][k] += factor * A[rank][k]
                rank += 1
        return rank

    def matrix_rank(M):
        return gaussian_elimination(M)

    def communication_complexity_rank(M):
        m, n = len(M), len(M[0])
        max_rank = 0
        for subset in combinations(range(n), m):
            submatrix = [[M[i][j] for j in subset] for i in range(m)]
            rank = matrix_rank(submatrix)
            if rank > max_rank:
                max_rank = rank
        return max_rank

    def generate_random_matrix(n):
        M = [[random.randint(0, 1) for _ in range(n)] for _ in range(n)]
        return M

    n_values = [5, 10, 15, 20, 30, 40]
    instances_tested = 0
    total_mtr_C = 0.0
    total_r_M = 0.0
    max_n = 0

    for n in n_values:
        for _ in range(5):
            M = generate_random_matrix(n)
            mtr_C = communication_complexity_rank(M)
            r_M = matrix_rank(M)
            
            if mtr_C == 0 or r_M == 0:
                continue
            
            instances_tested += 1
            total_mtr_C += mtr_C
            total_r_M += r_M
            max_n = n

    if instances_tested < 30:
        return {
            "metric_name": "communication_complexity_rank",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": max_n,
            "conjecture_holds": False,
            "counterexample": "insufficient_instances"
        }

    mean_mtr_C = total_mtr_C / instances_tested
    mean_r_M = total_r_M / instances_tested
    covariance = sum((mtr_C - mean_mtr_C) * (r_M - mean_r_M) for mtr_C, r_M in zip(mtr_C_values, r_M_values)) / instances_tested
    variance_mtr_C = sum((mtr_C - mean_mtr_C) ** 2 for mtr_C in mtr_C_values) / instances_tested
    variance_r_M = sum((r_M - mean_r_M) ** 2 for r_M in r_M_values) / instances_tested

    if variance_mtr_C == 0 or variance_r_M == 0:
        return {
            "metric_name": "communication_complexity_rank",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": max_n,
            "conjecture_holds": False,
            "counterexample": "variance_zero"
        }

    correlation_coefficient = covariance / (math.sqrt(variance_mtr_C) * math.sqrt(variance_r_M))

    return {
        "metric_name": "communication_complexity_rank",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": max_n,
        "conjecture_holds": correlation_coefficient > 0.7,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_metric_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")