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

def matrix_multiply(A, B):
    n = len(A)
    C = [[0 for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

def spectral_norm(A):
    n = len(A)
    v = [1.0] * n
    for _ in range(100):  # Power iteration method
        v = matrix_multiply(A, v)
        v = [x / math.sqrt(sum(x**2 for x in v)) for x in v]
    return max(abs(v[i]) for i in range(n))

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = 40
    read_twice_matrix = [[random.choice([-1, 1]) if i != j else 0 for j in range(n)] for i in range(n)]
    general_matrix = [[random.choice([-1, 1]) for _ in range(n)] for _ in range(n)]

    read_twice_norm = spectral_norm(read_twice_matrix)
    general_norm = spectral_norm(general_matrix)

    return {
        "metric_name": "Noncommutative Operator Norm",
        "metric_value": read_twice_norm / general_norm,
        "instances_tested": 1,
        "conjecture_holds": read_twice_norm <= math.log(n) and general_norm >= n,
        "counterexample": "" if read_twice_norm <= math.log(n) and general_norm >= n else "mapping_undefined"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 35)]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")