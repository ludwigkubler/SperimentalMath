# auto-injected by SEC sandbox
import math
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
from fractions import Fraction

def gaussian_elimination(A):
    m, n = len(A), len(A[0])
    for i in range(m):
        if A[i][i] == 0:
            return None  # Singular matrix
        for j in range(i + 1, m):
            factor = -A[j][i] / A[i][i]
            for k in range(n):
                A[j][k] += factor * A[i][k]
    rank = sum(1 for row in A if any(row))
    return rank

def rank(matrix):
    A_rref = [row[:] for row in matrix]
    return gaussian_elimination(A_rref)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_tests = 30
    instances_tested = 0
    correlation_sum = 0.0
    max_n = 0

    for _ in range(n_tests):
        k = random.randint(5, 40)
        max_n = max(max_n, k)

        # Generate a random k-ary communication problem
        matrix = [[random.randint(-10, 10) for _ in range(k)] for _ in range(k)]
        rank_variance = rank(matrix)

        if rank_variance is None:
            continue

        instances_tested += 1

    correlation = correlation_sum / instances_tested if instances_tested > 0 else 0
    conjecture_holds = correlation >= 0.8 and all(abs(g - R) <= 3 for g, R in zip(genus_values, rank_variance_values))
    counterexample = "mapping_undefined" if not conjecture_holds else ""

    return {
        "metric_name": "correlation",
        "metric_value": correlation,
        "instances_tested": instances_tested,
        "n_max": max_n,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else list(range(2, 30)) + list(random.sample([i for i in range(50, 100)], 27))
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_corr = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_corr} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_corr} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")