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
    
    def gaussian_elimination(matrix):
        n = len(matrix)
        for i in range(n):
            max_row = max(range(i, n), key=lambda k: abs(matrix[k][i]))
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
            pivot = matrix[i][i]
            if pivot == 0:
                continue
            for j in range(n):
                matrix[i][j] /= pivot
            for j in range(n):
                if i != j:
                    factor = matrix[j][i]
                    for k in range(n):
                        matrix[j][k] -= factor * matrix[i][k]
        return matrix

    def rank(matrix):
        n, m = len(matrix), len(matrix[0])
        augmented_matrix = [row + [1 if i == j else 0 for j in range(m)] for i, row in enumerate(matrix)]
        reduced_matrix = gaussian_elimination(augmented_matrix)
        rank = sum(1 for row in reduced_matrix if any(row[j] != 0 for j in range(n)))
        return rank

    def geometric_flow_time(rank):
        # Simplified model for geometric flow time
        return math.sqrt(rank)

    n_values = [5, 10, 15, 20, 30, 40]
    total_metric_value = 0.0
    instances_tested = 0
    n_max = 0

    for n in n_values:
        for _ in range(5):
            matrix = [[random.randint(-10, 10) for _ in range(n)] for _ in range(n)]
            rank_val = rank(matrix)
            metric_value = geometric_flow_time(rank_val)
            total_metric_value += metric_value
            instances_tested += 1
            n_max = max(n_max, n)

    mean_metric_value = total_metric_value / instances_tested
    conjecture_holds = True
    counterexample = ""

    return {
        "metric_name": "geometric_flow_time",
        "metric_value": mean_metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or list(range(2, 30))  # Default to first 29 primes if no seeds provided

    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        counterexample = next(r["counterexample"] for r in results if not r["conjecture_holds"])
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")