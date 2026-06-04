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
    
    def rank(matrix):
        m, n = len(matrix), len(matrix[0])
        T = [[max(row[j], col[j]) for j in range(n)] for row in matrix]
        U = []
        for i in range(m):
            if any(T[i][j] != float('-inf') for j in range(n)):
                u = [T[i][j] - T[i][0] for j in range(n)]
                U.append(u)
        rank_U = len(U)
        return rank_U
    
    def generate_communication_matrix(n):
        M = [[random.randint(0, 10) for _ in range(n)] for _ in range(n)]
        return M
    
    n_max = 40
    instances_tested = 0
    correlation_sum = 0.0
    support_count = 0
    
    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):
            M = generate_communication_matrix(n)
            rank_M = rank(M)
            # Construct the tropical curve (identity matrix for simplicity)
            T = [[max(row[j], col[j]) for j in range(n)] for row in M]
            rank_T = len([u for u in T if any(u[j] != float('-inf') for j in range(n))])
            
            instances_tested += 1
            correlation_sum += abs(rank_M - rank_T) / max(rank_M, rank_T)
    
    if instances_tested < 30:
        return {
            "metric_name": "correlation",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "insufficient_instances"
        }
    
    correlation_avg = correlation_sum / instances_tested
    if correlation_avg >= 0.5:
        support_count += 1
    
    return {
        "metric_name": "correlation",
        "metric_value": correlation_avg,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": support_count / len([5, 10, 15, 20, 30, 40]) >= 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(10000, 99999) for _ in range(30)]
    
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
    elif any(not r["conjecture_holds"] for r in results) and any(r["metric_value"] is not None for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_below_threshold\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")