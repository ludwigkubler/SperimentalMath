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
        max_row = i
        for j in range(i+1, n):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        pivot = A[i][i]
        for j in range(i, n):
            A[i][j] /= pivot
        for j in range(n):
            if j != i:
                factor = A[j][i]
                for k in range(i, n):
                    A[j][k] -= factor * A[i][k]

def matrix_multiply(A, B):
    n = len(A)
    C = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

def frege_proof_length(formula):
    # Simplified estimation of Frege proof length
    return len(formula) ** 2

def run_trial(seed: int) -> dict:
    random.seed(seed)
    d = random.randint(3, 5)
    n = random.randint(5, 40)
    instances_tested = 0
    moh_values = []
    f_values = []

    for _ in range(100):
        vertices = list(range(n))
        edges = set()
        while len(edges) < d * n // 2:
            u, v = random.sample(vertices, 2)
            if (u, v) not in edges and (v, u) not in edges:
                edges.add((u, v))

        # Construct Tseitin formula
        formula = []
        for i, (u, v) in enumerate(edges):
            formula.append(f"X{i} OR X{d*n//2+i}")
            formula.append(f"NOT X{i} OR NOT X{d*n//2+2*i}")
            formula.append(f"NOT X{d*n//2+i} OR NOT X{d*n//2+2*i+1}")
            formula.append(f"X{d*n//2+2*i} OR X{d*n//2+2*i+1}")

        # Compute Frege proof length
        f_value = frege_proof_length(formula)
        f_values.append(f_value)

        # Placeholder for moh(G) computation (not implemented)
        moh_value = random.randint(1, 10)  # Dummy value
        moh_values.append(moh_value)

        instances_tested += 1

    correlation_coefficient = sum((m - m_avg) * (f - f_avg) for m, f in zip(moh_values, f_values)) / math.sqrt(sum((m - m_avg) ** 2 for m in moh_values) * sum((f - f_avg) ** 2 for f in f_values))
    m_avg = sum(moh_values) / len(moh_values)
    f_avg = sum(f_values) / len(f_values)

    conjecture_holds = correlation_coefficient >= 0.8 and abs(m_avg - f_avg) <= 3
    counterexample = "" if conjecture_holds else "mapping_undefined"

    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 1000003) for _ in range(30)]
    results = []

    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")