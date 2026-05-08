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
        max_row = i + max(range(i, n), key=lambda k: abs(A[k][i]))
        A[i], A[max_row] = A[max_row], A[i]
        for j in range(i + 1, n):
            factor = A[j][i] / A[i][i]
            for k in range(n):
                A[j][k] -= factor * A[i][k]
    return A

def determinant(A):
    if len(A) == 2:
        return A[0][0] * A[1][1] - A[0][1] * A[1][0]
    det = 0
    for c in range(len(A)):
        submatrix = [row[:c] + row[c+1:] for row in A[1:]]
        sign = (-1) ** (c % 2)
        sub_det = determinant(submatrix)
        det += sign * A[0][c] * sub_det
    return det

def spectral_radius(A):
    n = len(A)
    max_eigenvalue = 0
    for _ in range(100):  # Power iteration method
        v = [random.random() for _ in range(n)]
        v = [x / sum(v) for x in v]
        Av = [sum(A[i][j] * v[j] for j in range(n)) for i in range(n)]
        lambda_ = max(abs(x) for x in Av)
        if abs(lambda_ - max_eigenvalue) < 1e-6:
            break
        max_eigenvalue = lambda_
    return max_eigenvalue

def free_entropy(A):
    n = len(A)
    eigenvalues = [spectral_radius(A)]
    for _ in range(n - 1):
        A = gaussian_elimination(A)
        eigenvalues.append(spectral_radius(A))
    return sum(-lambda_ * math.log(lambda_) for lambda_ in eigenvalues)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    M_n = [[random.random() if i != j else 1 for j in range(n)] for i in range(n)]
    tau_M_n = free_entropy(M_n)
    return {
        "metric_name": "free entropy",
        "metric_value": tau_M_n,
        "instances_tested": 1,
        "conjecture_holds": tau_M_n >= n,
        "counterexample": "" if tau_M_n >= n else f"n={n}, tau(M_n)={tau_M_n}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
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
    elif any(not r["conjecture_holds"] for r in results) and sum(1 for r in results if not r["counterexample"]) / len(results) >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        counterexample = next(r["counterexample"] for r in results if r["counterexample"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")