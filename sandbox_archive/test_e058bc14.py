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
            factor = 1 / A[i][i]
            for j in range(n):
                A[i][j] *= factor
            for j in range(m):
                if i != j:
                    factor = -A[j][i]
                    for k in range(n):
                        A[j][k] += factor * A[i][k]
        return A

    def matrix_multiplication(A, B):
        m, n, p = len(A), len(B), len(B[0])
        C = [[0] * p for _ in range(m)]
        for i in range(m):
            for j in range(p):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C

    def rank_variance(A):
        m, n = len(A), len(A[0])
        U, S, Vt = gaussian_elimination(A)
        rank = sum(1 for s in S if abs(s) > 1e-10)
        variance = sum((s**2 for s in S if abs(s) > 1e-10)) / rank
        return variance

    def minimal_representation_length(mrep):
        # Placeholder function to simulate mrep calculation
        return mrep

    instances_tested = 0
    n_max = 5
    metric_values = []
    conjecture_holds = True
    counterexample = ""

    for n in range(5, 41, 5):  # Sweep through sizes 5, 10, 15, 20, 30, 40
        for _ in range(5):  # Sample 5 instances per size
            A = [[random.randint(-10, 10) for _ in range(n)] for _ in range(n)]
            r = rank_variance(A)
            mrep = minimal_representation_length(r * math.log2(n))
            if mrep > 1.5 * r:
                conjecture_holds = False
                counterexample = f"n={n}, r={r}, mrep={mrep}"
                break
            instances_tested += 1
            n_max = max(n_max, n)
        if not conjecture_holds:
            break

    return {
        "metric_name": "minimal_representation_length",
        "metric_value": sum(metric_values) / len(metric_values),
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=unknown")