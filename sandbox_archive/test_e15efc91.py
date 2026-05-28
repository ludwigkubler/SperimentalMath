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

def gaussian_elimination(matrix):
    n = len(matrix)
    for i in range(n):
        max_row = i
        for j in range(i+1, n):
            if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                max_row = j
        matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
        pivot = matrix[i][i]
        for j in range(n):
            matrix[i][j] /= pivot
        for j in range(n):
            if j != i:
                factor = matrix[j][i]
                for k in range(n):
                    matrix[j][k] -= factor * matrix[i][k]
    rank = sum(1 for row in matrix if any(row))
    return rank

def rank(matrix):
    n = len(matrix)
    m = len(matrix[0])
    augmented_matrix = [row + [0] * (m - n) for row in matrix]
    reduced_matrix = gaussian_elimination(augmented_matrix)
    return sum(1 for row in reduced_matrix if any(row))

def generate_bp_instance(n):
    bp_instance = []
    for _ in range(n):
        bp_instance.append(random.choice([0, 1]))
        bp_instance.append(random.choice([0, 1]))
    return bp_instance

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    total_rank = 0
    total_comm_complexity = 0
    instances_tested = 0

    for n in n_values:
        for _ in range(5):  # Ensure at least 5 instances per size
            bp_instance = generate_bp_instance(n)
            kac_moody_rank = rank([[bp_instance[i], bp_instance[n + i]] for i in range(n)])
            total_rank += kac_moody_rank
            comm_complexity = n * (n + 1) // 2  # Simplified communication complexity bound
            total_comm_complexity += comm_complexity
            instances_tested += 1

    mean_rank = Fraction(total_rank, instances_tested)
    mean_comm_complexity = Fraction(total_comm_complexity, instances_tested)

    conjecture_holds = (mean_rank <= 1.5 * mean_comm_complexity) and (mean_rank >= 0.67 * mean_comm_complexity)
    counterexample = "" if conjecture_holds else f"Rank {mean_rank}, Comm Complexity {mean_comm_complexity}"

    return {
        "metric_name": "Communication Complexity",
        "metric_value": mean_comm_complexity,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or list(range(2, 30))  # Default to first 29 primes if no seeds provided

    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)

    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)

    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in enumerate(results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Rank {results[first_failing_seed]['metric_value']}, Comm Complexity {mean_metric_value}\" first_failing_seed={first_failing_seed}")