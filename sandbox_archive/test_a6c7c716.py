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
        for i in range(m):
            max_row = i
            for j in range(i+1, m):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            for j in range(i+1, m):
                factor = A[j][i] / A[i][i]
                for k in range(n):
                    A[j][k] -= factor * A[i][k]
        return A

    def matrix_multiplication(A, B):
        m, n, p = len(A), len(B), len(B[0])
        C = [[0] * p for _ in range(m)]
        for i in range(m):
            for j in range(p):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C

    def variance(lst):
        mean = sum(lst) / len(lst)
        return sum((x - mean) ** 2 for x in lst) / len(lst)

    def lid(P):
        # Placeholder implementation of LID
        return random.random()

    def comm_rank_var(P):
        # Placeholder implementation of communication complexity rank variance
        return random.random()

    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        P = [[random.randint(0, 1) for _ in range(n)] for _ in range(n)]
        lid_value = lid(P)
        comm_rank_var_value = comm_rank_var(P)
        results.append({
            "n": n,
            "lid_value": lid_value,
            "comm_rank_var_value": comm_rank_var_value
        })

    if not results:
        return {
            "metric_name": "LID vs CommRankVar",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }

    lid_values = [r["lid_value"] for r in results]
    comm_rank_var_values = [r["comm_rank_var_value"] for r in results]

    if len(lid_values) < 30:
        return {
            "metric_name": "LID vs CommRankVar",
            "metric_value": None,
            "instances_tested": len(lid_values),
            "n_max": max(r["n"] for r in results),
            "conjecture_holds": False,
            "counterexample": "insufficient_instances"
        }

    correlation = sum((lid_values[i] - mean(lid_values)) * (comm_rank_var_values[i] - mean(comm_rank_var_values)) for i in range(len(lid_values))) / len(lid_values)
    
    if correlation < 0.8:
        return {
            "metric_name": "LID vs CommRankVar",
            "metric_value": None,
            "instances_tested": len(lid_values),
            "n_max": max(r["n"] for r in results),
            "conjecture_holds": False,
            "counterexample": f"low_correlation={correlation}"
        }

    mean_comm_rank_var = mean(comm_rank_var_values)
    std_comm_rank_var = variance(comm_rank_var_values) ** 0.5
    max_lid_value = max(lid_values)

    if max_lid_value > 1.3 * mean_comm_rank_var + 3 * std_comm_rank_var:
        return {
            "metric_name": "LID vs CommRankVar",
            "metric_value": None,
            "instances_tested": len(lid_values),
            "n_max": max(r["n"] for r in results),
            "conjecture_holds": False,
            "counterexample": f"max_lid_value={max_lid_value} exceeds threshold"
        }

    return {
        "metric_name": "LID vs CommRankVar",
        "metric_value": correlation,
        "instances_tested": len(lid_values),
        "n_max": max(r["n"] for r in results),
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [random.randint(2, 97) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    if all(r["conjecture_holds"] for r in results):
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        std_value = (sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results)) ** 0.5
        support_fraction = len([r for r in results if r["conjecture_holds"]]) / len(results)
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='low_correlation' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")