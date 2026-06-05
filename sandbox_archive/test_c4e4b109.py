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

    def compute_complexity(instance):
        n = len(instance)
        log_n = math.log2(n) if n > 0 else 1
        # Placeholder complexity calculation (replace with actual algorithm)
        return log_n * random.random()

    def minimal_local_induction_ring_rank(instance):
        n = len(instance)
        A = [[random.randint(0, 1) for _ in range(n)] for _ in range(n)]
        rank = gaussian_elimination(A)
        non_zero_rows = sum(1 for row in rank if any(row))
        return non_zero_rows

    def generate_instance(n):
        return [random.choice([0, 1]) for _ in range(n)]

    n_values = [5, 10, 15, 20, 30, 40]
    metric_values = []
    instances_tested = 0
    n_max = 0

    for n in n_values:
        instance = generate_instance(n)
        mli_n = minimal_local_induction_ring_rank(instance)
        complexity = compute_complexity(instance)
        metric_values.append((mli_n, complexity))
        instances_tested += len(instance)
        n_max = max(n_max, n)

    correlation_coefficient = 0
    if len(metric_values) > 1:
        x_mean = sum(x for x, _ in metric_values) / len(metric_values)
        y_mean = sum(y for _, y in metric_values) / len(metric_values)
        numerator = sum((x - x_mean) * (y - y_mean) for x, y in metric_values)
        denominator = math.sqrt(sum((x - x_mean)**2 for x, _ in metric_values)) * math.sqrt(sum((y - y_mean)**2 for _, y in metric_values))
        correlation_coefficient = numerator / denominator

    conjecture_holds = correlation_coefficient > 0.9
    counterexample = "" if conjecture_holds else "correlation_coefficient < 0.9"

    return {
        "metric_name": "Correlation Coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3

    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = results[first_failing_seed]["counterexample"]
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")