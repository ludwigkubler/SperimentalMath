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

def gaussian_elimination(A):
    rows, cols = len(A), len(A[0])
    for i in range(rows):
        # Find pivot
        max_row = i + A[i:].index(max(abs(row[i]) for row in A[i:]))
        if A[max_row][i] == 0:
            continue
        A[i], A[max_row] = A[max_row], A[i]
        
        # Eliminate below
        for j in range(i+1, rows):
            factor = A[j][i] / A[i][i]
            for k in range(cols):
                A[j][k] -= factor * A[i][k]
    return A

def matrix_rank(A):
    rank = 0
    A = gaussian_elimination(A)
    for row in A:
        if any(row):
            rank += 1
    return rank

def generate_protocol(n):
    protocol = [[random.choice([0, 1]) for _ in range(2**n)] for _ in range(2**n)]
    return protocol

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    metric_name = "correlation_coefficient"
    metric_value = 0.0
    instances_tested = 0
    n_max = 0
    conjecture_holds = True
    counterexample = ""

    for n in n_values:
        if n > 40:
            break

        protocol = generate_protocol(n)
        rank_comm_complexity = matrix_rank(protocol)

        # Calculate p-adic unit ball rank (simplified example)
        padic_unit_ball_rank = n  # Simplified example, replace with actual calculation

        instances_tested += len(protocol)
        n_max = max(n_max, n)

        metric_value += rank_comm_complexity * padic_unit_ball_rank
        if instances_tested > 1:
            mean_msl = metric_value / instances_tested
            std_dev = math.sqrt(sum((x - mean_msl) ** 2 for x in [rank_comm_complexity * padic_unit_ball_rank]) / (instances_tested - 1))
            correlation_coefficient = (metric_value - len(protocol) * mean_msl) / (len(protocol) * std_dev)
            if abs(correlation_coefficient) < 0.5:
                conjecture_holds = False
                counterexample = f"n={n}, rank_comm_complexity={rank_comm_complexity}, padic_unit_ball_rank={padic_unit_ball_rank}"
                break

    return {
        "metric_name": metric_name,
        "metric_value": metric_value / instances_tested if instances_tested > 0 else 0.0,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)

    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    std_dev = math.sqrt(sum((result["metric_value"] - mean_metric_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)

    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_dev} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results) and any(result["counterexample"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE")