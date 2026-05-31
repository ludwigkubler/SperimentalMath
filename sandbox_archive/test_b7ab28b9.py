# auto-injected by SEC sandbox
import json
import sys
import os
import time
import re
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from fractions import Fraction
import itertools
import collections

def gaussian_elimination(A, b):
    n = len(b)
    for i in range(n):
        max_row = i
        for j in range(i+1, n):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        b[i], b[max_row] = b[max_row], b[i]
        for j in range(i+1, n):
            factor = Fraction(A[j][i], A[i][i])
            for k in range(n):
                A[j][k] -= factor * A[i][k]
            b[j] -= factor * b[i]
    x = [0] * n
    for i in range(n-1, -1, -1):
        x[i] = Fraction(b[i], A[i][i])
        for j in range(i-1, -1, -1):
            b[j] -= A[j][i] * x[i]
    return x

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    aff_roots_sum = 0
    comm_complexity_sum = 0
    instances_tested = 0
    n_max = 0

    for n in n_values:
        if n > n_max:
            n_max = n
        for _ in range(5):  # Sample 5 instances per size
            A = [[random.randint(-10, 10) for _ in range(n)] for _ in range(n)]
            b = [random.randint(-10, 10) for _ in range(n)]
            x = gaussian_elimination(A, b)
            aff_roots = sum(1 for row in A if all(val == 0 for val in row))
            comm_complexity = n * (n + 1) // 2  # Example communication complexity measure
            aff_roots_sum += aff_roots
            comm_complexity_sum += comm_complexity
            instances_tested += 1

    mean_aff_roots = Fraction(aff_roots_sum, instances_tested)
    mean_comm_complexity = Fraction(comm_complexity_sum, instances_tested)
    correlation_coefficient = (instances_tested * aff_roots_sum * comm_complexity_sum - aff_roots_sum * aff_roots_sum * comm_complexity_sum) / (
        math.sqrt(instances_tested * aff_roots_sum * aff_roots_sum - aff_roots_sum * aff_roots_sum) *
        math.sqrt(instances_tested * comm_complexity_sum * comm_complexity_sum - comm_complexity_sum * comm_complexity_sum)
    )

    conjecture_holds = correlation_coefficient >= 0.7
    counterexample = "" if conjecture_holds else "correlation_coefficient < 0.7"

    return {
        "metric_name": "Pearson Correlation Coefficient",
        "metric_value": float(correlation_coefficient),
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or list(range(2, 30))  # Default to first 30 primes if no seeds provided

    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...{result}...}}")
        results.append(result)

    mean_metric_value = sum(res["metric_value"] for res in results) / len(results)
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)

    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction=1.0")
    elif any(res["metric_value"] <= 0.3 for res in results):
        first_failing_seed = next(res["seed"] for res in results if res["metric_value"] <= 0.3)
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient <= 0.3\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction}")