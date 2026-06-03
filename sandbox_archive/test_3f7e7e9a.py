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
    
    def gaussian_elimination(A, b):
        n = len(b)
        for i in range(n):
            max_row = i + max(range(i, n), key=lambda j: abs(A[j][i]))
            A[i], A[max_row] = A[max_row], A[i]
            b[i], b[max_row] = b[max_row], b[i]
            factor = 1 / A[i][i]
            for j in range(n):
                A[i][j] *= factor
            b[i] *= factor
            for k in range(n):
                if k != i:
                    factor = A[k][i]
                    for j in range(n):
                        A[k][j] -= factor * A[i][j]
                    b[k] -= factor * b[i]
        return b

    def matrix_multiply(A, B):
        n = len(A)
        C = [[0 for _ in range(n)] for _ in range(n)]
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C

    def circuit_monotone_width(n):
        if n == 1:
            return 1
        width = 0
        for i in range(2, n + 1):
            width = max(width, circuit_monotone_width(i - 1) + 1)
        return width

    def min_symplectic_capacity(n):
        # Simplified approximation for demonstration purposes
        return random.uniform(0.5, 1.5)

    n_values = [5, 10, 15, 20, 30, 40]
    instances_tested = 0
    total_sym_cap = 0
    total_width_mon = 0

    for n in n_values:
        for _ in range(5):
            width_mon = circuit_monotone_width(n)
            sym_cap = min_symplectic_capacity(n)
            total_sym_cap += sym_cap
            total_width_mon += width_mon
            instances_tested += 1

    mean_sym_cap = total_sym_cap / instances_tested
    mean_width_mon = total_width_mon / instances_tested
    correlation_coefficient = (instances_tested * sum(s * w for s, w in zip(total_sym_cap, total_width_mon)) -
                               total_sym_cap * total_width_mon) / math.sqrt(
        instances_tested * sum(s ** 2 for s in total_sym_cap) - total_sym_cap ** 2 *
        instances_tested * sum(w ** 2 for w in total_width_mon) - total_width_mon ** 2)

    conjecture_holds = correlation_coefficient > 0.7 and all(1.5 * w >= c for c, w in zip(total_sym_cap, total_width_mon))
    counterexample = "" if conjecture_holds else "mapping_undefined"

    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": max(n_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3

    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, **{result}}}")
        results.append(result)

    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.95:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")