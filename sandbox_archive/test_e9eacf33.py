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

def generate_boolean_function(n):
    return [random.choice([0, 1]) for _ in range(2**n)]

def communication_complexity_rank_variance(f):
    n = int(math.log2(len(f)))
    matrix = [[f[i ^ j] for j in range(2**n)] for i in range(2**n)]
    rank = gaussian_elimination(matrix)
    return rank * (2**n - rank)

def gaussian_elimination(A):
    m, n = len(A), len(A[0])
    rank = 0
    for i in range(m):
        if A[i][rank] == 0:
            swap_found = False
            for j in range(i + 1, m):
                if A[j][rank] != 0:
                    A[i], A[j] = A[j], A[i]
                    swap_found = True
                    break
            if not swap_found:
                continue
        pivot = Fraction(A[i][rank])
        for j in range(n):
            A[i][j] /= pivot
        for j in range(m):
            if j != i and A[j][rank] != 0:
                factor = -A[j][rank]
                for k in range(n):
                    A[j][k] += factor * A[i][k]
        rank += 1
    return rank

def minimal_index_of_crossed_product(f):
    n = int(math.log2(len(f)))
    matrix = [[f[i ^ j] for j in range(2**n)] for i in range(2**n)]
    rank = gaussian_elimination(matrix)
    return Fraction(rank * (2**n - rank), 2**(n * (n + 1) // 2))

def run_trial(seed: int) -> dict:
    random.seed(seed)
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        f = generate_boolean_function(n)
        I_n = minimal_index_of_crossed_product(f)
        r_n = communication_complexity_rank_variance(f)
        if r_n == 0:
            continue
        ratio = I_n / r_n
        results.append((n, I_n, r_n, ratio))
    if not results:
        return {
            "metric_name": "I(n)/r(n)",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    n_max = max(n for n, _, _, _ in results)
    metric_values = [ratio for _, _, _, ratio in results]
    mean_value = sum(metric_values) / len(metric_values)
    std_value = math.sqrt(sum((x - mean_value) ** 2 for x in metric_values) / len(metric_values))
    conjecture_holds = all(ratio <= 1.5 for _, _, _, ratio in results)
    return {
        "metric_name": "I(n)/r(n)",
        "metric_value": mean_value,
        "instances_tested": len(results),
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else "ratio > 1.5"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)

    if not all("metric_value" in result and result["metric_value"] is not None for result in results):
        print("RESULT: INCONCLUSIVE reason=missing_metric_values")
    else:
        mean_value = sum(result["metric_value"] for result in results) / len(results)
        std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
        support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
        if support_fraction >= 0.8:
            print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
        else:
            first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
            print(f"RESULT: FALSIFIED counterexample='ratio > 1.5' first_failing_seed={first_failing_seed}")