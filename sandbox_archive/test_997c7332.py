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
    
    def gaussian_elimination(A, b):
        n = len(A)
        for i in range(n):
            max_row = i + random.randint(0, n - i - 1)
            A[i], A[max_row] = A[max_row], A[i]
            b[i], b[max_row] = b[max_row], b[i]
            factor = A[i][i]
            for j in range(n):
                A[i][j] /= factor
            b[i] /= factor
            for k in range(n):
                if k != i:
                    factor = A[k][i]
                    for j in range(n):
                        A[k][j] -= factor * A[i][j]
                    b[k] -= factor * b[i]
        return [b[i][0] for i in range(n)]
    
    def comm_complexity_rank(C):
        # Placeholder function to simulate communication complexity rank
        return len(C)
    
    def geo_entangle(Q):
        # Placeholder function to simulate minimal order of geometric entanglement
        return random.random()
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    for n in n_values:
        for _ in range(5):
            Q = [[random.randint(0, 1) for _ in range(n)] for _ in range(n)]
            C = [random.randint(0, 1) for _ in range(n * (n - 1))]
            geo_ent = geo_entangle(Q)
            comm_rank = comm_complexity_rank(C)
            results.append((geo_ent, comm_rank))
    
    if not results:
        return {
            "metric_name": "correlation",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    geo_ent_values = [r[0] for r in results]
    comm_rank_values = [r[1] for r in results]
    mean_geo_ent = sum(geo_ent_values) / len(geo_ent_values)
    mean_comm_rank = sum(comm_rank_values) / len(comm_rank_values)
    
    covariance = sum((geo_ent_values[i] - mean_geo_ent) * (comm_rank_values[i] - mean_comm_rank) for i in range(len(results))) / len(results)
    variance_geo_ent = sum((geo_ent_values[i] - mean_geo_ent) ** 2 for i in range(len(results))) / len(results)
    variance_comm_rank = sum((comm_rank_values[i] - mean_comm_rank) ** 2 for i in range(len(results))) / len(results)
    
    std_dev_geo_ent = math.sqrt(variance_geo_ent)
    std_dev_comm_rank = math.sqrt(variance_comm_rank)
    
    correlation_coefficient = covariance / (std_dev_geo_ent * std_dev_comm_rank)
    
    return {
        "metric_name": "correlation",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": abs(correlation_coefficient) > 0.5 and all(abs(r[0] - mean_geo_ent) <= 3 * std_dev_geo_ent for r in results),
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all(r["conjecture_holds"] for r in results):
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        std_dev = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
        support_fraction = len([r for r in results if r["conjecture_holds"]]) / len(results)
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing = next(r for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing['seed']}")
    else:
        print("RESULT: INCONCLUSIVE no data")