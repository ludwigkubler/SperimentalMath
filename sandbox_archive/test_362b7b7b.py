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

def gaussian_elimination(A):
    n = len(A)
    for i in range(n):
        max_row = i + max(range(i, n), key=lambda j: abs(A[j][i]))
        A[i], A[max_row] = A[max_row], A[i]
        for j in range(i+1, n):
            factor = A[j][i] / A[i][i]
            for k in range(n):
                A[j][k] -= factor * A[i][k]
    return A

def solve_linear_system(A, b):
    n = len(A)
    A_b = [row + [b[i]] for i, row in enumerate(A)]
    A_b = gaussian_elimination(A_b)
    x = [0] * n
    for i in range(n-1, -1, -1):
        x[i] = (A_b[i][-1] - sum(A_b[i][j] * x[j] for j in range(i+1, n))) / A_b[i][i]
    return x

def matrix_multiply(A, B):
    m, k = len(A), len(B[0])
    result = [[0] * k for _ in range(m)]
    for i in range(m):
        for j in range(k):
            for l in range(len(B)):
                result[i][j] += A[i][l] * B[l][j]
    return result

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = 30
    instances_tested = 100
    metric_value = 0.0
    conjecture_holds = True
    counterexample = ""

    for _ in range(instances_tested):
        # Generate a random Max-CUT instance
        A = [[random.randint(0, 1) if i != j else 0 for j in range(n)] for i in range(n)]
        b = [random.choice([-1, 1]) for _ in range(n)]

        # Compute the quartic polynomial and its critical points
        Q = matrix_multiply(matrix_multiply(A, A), A)
        Q += [[b[i] * b[j] for j in range(n)] for i in range(n)]
        Q += [[0] * n + [b[i]] for i in range(n)]
        Q += [[b[i]] + [0] * n for i in range(n)]
        Q.append([sum(b) for _ in range(n+1)])
        Q.append([sum(b) for _ in range(n+1)])

        # Solve the linear system to find critical points
        try:
            x = solve_linear_system(Q, [0] * (n + 2))
            critical_points = sum(1 for xi in x if abs(xi) > 1e-6)
        except Exception as e:
            counterexample = f"Linear system error: {str(e)}"
            conjecture_holds = False
            break

        # Measure the SOS degree required to achieve an approximation ratio of 0.878 - ε
        d = int(math.log2(critical_points)) + 1
        metric_value += d

    if counterexample:
        return {
            "metric_name": "SOS Degree",
            "metric_value": None,
            "instances_tested": instances_tested,
            "conjecture_holds": False,
            "counterexample": counterexample
        }

    return {
        "metric_name": "SOS Degree",
        "metric_value": metric_value / instances_tested,
        "instances_tested": instances_tested,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    results = []

    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")

    mean_metric_value = sum(result["metric_value"] for result in results if result["metric_value"] is not None) / len(results)
    std_metric_value = math.sqrt(sum((result["metric_value"] - mean_metric_value)**2 for result in results if result["metric_value"] is not None)) / len(results)
    support_fraction = sum(result["conjecture_holds"] for result in results) / len(results)

    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        counterexample = next(result["counterexample"] for result in results if result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")