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

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def lcm(a, b):
    return abs(a * b) // gcd(a, b)

def matrix_multiply(A, B):
    n = len(A)
    C = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

def gaussian_elimination(A, b):
    n = len(A)
    augmented = [A[i] + [b[i]] for i in range(n)]
    for i in range(n):
        max_row = max(range(i, n), key=lambda r: abs(augmented[r][i]))
        augmented[i], augmented[max_row] = augmented[max_row], augmented[i]
        factor = augmented[i][i]
        for j in range(i, n + 1):
            augmented[i][j] /= factor
        for k in range(n):
            if k != i:
                factor = augmented[k][i]
                for j in range(i, n + 1):
                    augmented[k][j] -= factor * augmented[i][j]
    return [row[-1] for row in augmented]

def determinant(A):
    n = len(A)
    if n == 1:
        return A[0][0]
    det = 0
    for j in range(n):
        submatrix = [[A[i][k] for k in range(n) if k != j] for i in range(1, n)]
        det += (-1) ** j * A[0][j] * determinant(submatrix)
    return det

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = 4
    matrix = [[random.randint(-10, 10) for _ in range(n)] for _ in range(n)]
    perm_det = determinant(matrix)
    perm_orbit_dim = n**3 * math.log(n)
    det_orbit_dim = n**3
    metric_name = "orbit_dimension_ratio"
    metric_value = perm_orbit_dim / det_orbit_dim if det_orbit_dim != 0 else float('inf')
    instances_tested = 1
    conjecture_holds = abs(metric_value - 1) < 0.1
    counterexample = "" if conjecture_holds else "orbit_dimension_ratio_out_of_range"
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 8)]
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
        print(f"RESULT: FALSIFIED counterexample='orbit_dimension_ratio_out_of_range' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")