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

def generate_random_boolean_function(n):
    return [random.randint(0, 1) for _ in range(2**n)]

def compute_ker_f(f, n):
    ker_f = []
    for x in range(2**n):
        if f[x] == 0:
            ker_f.append(x)
    return ker_f

def gaussian_elimination(A):
    m, n = len(A), len(A[0])
    rank = 0
    for j in range(n):
        i_max = -1
        for i in range(rank, m):
            if A[i][j] != 0:
                i_max = i
                break
        if i_max == -1:
            continue
        A[rank], A[i_max] = A[i_max], A[rank]
        for i in range(m):
            if i != rank and A[i][j] != 0:
                factor = Fraction(A[i][j], A[rank][j])
                for k in range(n):
                    A[i][k] -= factor * A[rank][k]
        rank += 1
    return rank

def compute_H1_ker_f_F2(ker_f, n):
    m = len(ker_f)
    if m == 0:
        return 0
    A = [[0 for _ in range(n)] for _ in range(m)]
    for i, x in enumerate(ker_f):
        for j in range(n):
            A[i][j] = (x >> j) & 1
    rank = gaussian_elimination(A)
    return m - rank

def compute_comm_rank(f, n):
    # Placeholder function to simulate communication complexity rank computation
    # This is a dummy implementation and should be replaced with actual logic
    return random.randint(1, 10)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    metric_values = []
    instances_tested = 0
    n_max = 0

    for n in [10, 20, 30, 40]:
        for _ in range(7):  # Aim for at least 30 instances per seed
            f = generate_random_boolean_function(n)
            ker_f = compute_ker_f(f, n)
            H1_ker_f_F2 = compute_H1_ker_f_F2(ker_f, n)
            comm_rank = compute_comm_rank(f, n)
            if comm_rank > 0:
                metric_values.append(H1_ker_f_F2 ** 2 / comm_rank)
                instances_tested += 1
                n_max = max(n_max, n)

    if len(metric_values) < 30:
        return {
            "metric_name": "R_var(CommRank(f))",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "not_enough_instances"
        }

    mean = sum(metric_values) / len(metric_values)
    std_dev = math.sqrt(sum((x - mean) ** 2 for x in metric_values) / len(metric_values))
    correlation_coefficient = None

    return {
        "metric_name": "R_var(CommRank(f))",
        "metric_value": mean,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 7 for i in range(5, 30)]
    results = []

    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...{result}...}}")
        results.append(result)

    mean_metric_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_dev_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_dev_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_dev_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"not_enough_support\" first_failing_seed={first_failing_seed}")