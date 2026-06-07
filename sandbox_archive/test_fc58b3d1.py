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
            max_row = i + max(range(i, m), key=lambda r: abs(A[r][i]))
            A[i], A[max_row] = A[max_row], A[i]
            if A[i][i] == 0:
                continue
            for j in range(n):
                A[i][j] /= A[i][i]
            for k in range(m):
                if k != i and A[k][i] != 0:
                    factor = A[k][i]
                    for j in range(n):
                        A[k][j] -= factor * A[i][j]
        return A

    def matrix_multiply(A, B):
        m, n, p = len(A), len(B), len(B[0])
        C = [[0] * p for _ in range(m)]
        for i in range(m):
            for j in range(p):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C

    def determinant(A):
        if len(A) == 1:
            return A[0][0]
        det = 0
        for c in range(len(A)):
            det += ((-1) ** c) * A[0][c] * determinant([row[:c] + row[c+1:] for row in A[1:]])
        return det

    def local_cohomology_rank(n):
        # Example encoding of a Boolean formula to an algebraic variety
        # This is a placeholder implementation and should be replaced with actual computation
        # For simplicity, we use the rank of a random matrix as a proxy for local cohomology rank
        A = [[random.randint(0, 1) for _ in range(n)] for _ in range(n)]
        return abs(determinant(gaussian_elimination(A)))

    def resolution_width(n):
        # Example encoding of a Boolean formula to its resolution width
        # This is a placeholder implementation and should be replaced with actual computation
        # For simplicity, we use the rank of a random matrix as a proxy for resolution width
        A = [[random.randint(0, 1) for _ in range(n)] for _ in range(n)]
        return abs(determinant(gaussian_elimination(A)))

    n_max = 40
    instances_tested = 30
    metric_values = []
    conjecture_holds = True
    counterexample = ""

    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(instances_tested // len([5, 10, 15, 20, 30, 40])):
            h_1 = local_cohomology_rank(n)
            w_phi = resolution_width(n)
            metric_values.append(w_phi / h_1)

    if len(metric_values) == 0:
        return {
            "metric_name": "resolution_width_over_local_cohomology",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }

    mean = sum(metric_values) / len(metric_values)
    std_dev = math.sqrt(sum((x - mean) ** 2 for x in metric_values) / len(metric_values))
    correlation_coefficient = sum((metric_values[i] - mean) * (i + 1 - mean) for i in range(len(metric_values))) / (len(metric_values) * std_dev * std_dev)

    if correlation_coefficient < 0.6:
        conjecture_holds = False
        counterexample = f"Correlation coefficient {correlation_coefficient} below threshold"

    return {
        "metric_name": "resolution_width_over_local_cohomology",
        "metric_value": mean,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys

    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []

    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")

    mean_metric_value = sum(result["metric_value"] for result in results if result["metric_value"] is not None) / len(results)
    std_dev_metric_value = math.sqrt(sum((result["metric_value"] - mean_metric_value) ** 2 for result in results if result["metric_value"] is not None) / len(results))
    support_fraction = sum(result["conjecture_holds"] for result in results) / len(results)

    if all("counterexample" in result and result["counterexample"] != "" for result in results):
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={seeds[0]}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_dev_metric_value} support_fraction={support_fraction}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction}")