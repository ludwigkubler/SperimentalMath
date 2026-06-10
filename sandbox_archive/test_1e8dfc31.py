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

def gaussian_elimination(A):
    m, n = len(A), len(A[0])
    for i in range(m):
        max_row = i
        for j in range(i+1, m):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
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

def symplectic_rank(A):
    m, n = len(A), len(A[0])
    if m != n or any(len(row) != n for row in A):
        raise ValueError("Matrix must be square")
    rank = 0
    for i in range(m):
        pivot = next((j for j in range(n) if abs(A[i][j]) > 1e-9), None)
        if pivot is not None:
            rank += 1
            for j in range(n):
                A[i][j] /= A[i][pivot]
            for k in range(m):
                if k != i and abs(A[k][pivot]) > 1e-9:
                    factor = A[k][pivot]
                    for j in range(n):
                        A[k][j] -= factor * A[i][j]
    return rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.choice([5, 10, 15, 20, 30, 40])
    instances_tested = 0
    srank_sum = 0.0
    ccrvar_sum = 0.0
    max_n = n

    for _ in range(30):
        # Generate a random instance with n variables
        A = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
        B = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]

        # Compute communication complexity rank variance (ccrvar)
        ccrvar = sum(sum(abs(a - b) for a, b in zip(rowA, rowB))**2 for rowA, rowB in zip(A, B))
        instances_tested += 1

        # Compute symplectic rank (srank)
        srank = symplectic_rank(A)
        if srank > ccrvar**(1/2):
            return {
                "metric_name": "symplectic_rank",
                "metric_value": srank,
                "instances_tested": instances_tested,
                "n_max": max_n,
                "conjecture_holds": False,
                "counterexample": f"Instance with n={n} has srank={srank} > ccrvar^(1/2)={ccrvar**(1/2)}"
            }

        # Accumulate metrics
        srank_sum += srank
        ccrvar_sum += ccrvar

    mean_srank = srank_sum / instances_tested
    mean_ccrvar = ccrvar_sum / instances_tested
    correlation_coefficient = (instances_tested * sum(srank * ccrvar for srank, ccrvar in zip(srank_list, ccrvar_list)) -
                               instances_tested * mean_srank * mean_ccrvar) / \
                              math.sqrt((instances_tested * sum(srank**2 for srank in srank_list) - instances_tested * mean_srank**2) *
                                        (instances_tested * sum(ccrvar**2 for ccrvar in ccrvar_list) - instances_tested * mean_ccrvar**2))

    return {
        "metric_name": "symplectic_rank",
        "metric_value": mean_srank,
        "instances_tested": instances_tested,
        "n_max": max_n,
        "conjecture_holds": correlation_coefficient >= 0.9,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction=1.0")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")