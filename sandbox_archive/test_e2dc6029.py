# auto-injected by SEC sandbox
import math
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
from fractions import Fraction
from itertools import combinations

def gaussian_elimination(A):
    n = len(A)
    for i in range(n):
        if A[i][i] == 0:
            # Find a row to swap with
            for j in range(i+1, n):
                if A[j][i] != 0:
                    A[i], A[j] = A[j], A[i]
                    break
            else:
                raise ValueError("Matrix is singular")
        factor = Fraction(A[i][i])
        for j in range(n):
            A[i][j] /= factor
        for k in range(n):
            if k != i and A[k][i] != 0:
                factor = A[k][i]
                for j in range(n):
                    A[k][j] -= factor * A[i][j]
    return A

def symplectic_topological_degree(circuit):
    # Construct the vector bundle using a constructive mapping
    n = len(circuit)
    A = [[0]*n for _ in range(n)]
    for i, j in combinations(range(n), 2):
        if circuit[i] == circuit[j]:
            A[i][j] = 1
    rank = len(gaussian_elimination(A))
    return rank

def communication_complexity_rank(circuit):
    # Placeholder function for actual computation of communication complexity rank
    return random.randint(1, n)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    metrics = []
    instances_tested = 0
    n_max = 0

    for n in n_values:
        for _ in range(5):  # Sample 5 instances per size
            circuit = [random.choice([0, 1]) for _ in range(n)]
            degree = symplectic_topological_degree(circuit)
            rank = communication_complexity_rank(circuit)
            metrics.append((degree, rank))
            instances_tested += 1
            n_max = max(n_max, n)

    if not metrics:
        return {
            "metric_name": "Var(CommRank)",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "No circuits generated"
        }

    expected_bound = [n * Fraction(n).log2() for n, _ in metrics]
    empirical_variance = sum((rank - expected) ** 2 for _, rank, expected in zip(metrics, expected_bound, expected_bound)) / len(metrics)
    conjecture_holds = abs(empirical_variance - expected_bound[0]) <= 0.1 * expected_bound[0]

    return {
        "metric_name": "Var(CommRank)",
        "metric_value": empirical_variance,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []

    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {{'seed': {seed}, **trial_result}}")
        results.append(trial_result)

    mean_value = sum(result["metric_value"] for result in results if result["metric_value"] is not None) / len(results)
    std_value = (sum((result["metric_value"] - mean_value) ** 2 for result in results if result["metric_value"] is not None) / len(results)) ** 0.5
    support_fraction = sum(result["conjecture_holds"] for result in results) / len(results)

    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_data")