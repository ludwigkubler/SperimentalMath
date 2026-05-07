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
        pivot = A[i][i]
        for j in range(i, n + 1):
            A[i][j] /= pivot
        for k in range(n):
            if k != i:
                factor = A[k][i]
                for j in range(i, n + 1):
                    A[k][j] -= factor * A[i][j]
    return [row[n] for row in A]

def matrix_multiplication(A, B):
    m, p, q = len(A), len(B), len(B[0])
    C = [[0] * q for _ in range(m)]
    for i in range(m):
        for j in range(q):
            for k in range(p):
                C[i][j] += A[i][k] * B[k][j]
    return C

def qr_decomposition(A):
    m, n = len(A), len(A[0])
    Q = [[0] * n for _ in range(m)]
    R = [[A[i][j] if i <= j else 0 for j in range(n)] for i in range(m)]
    for k in range(n):
        norm = sum(A[i][k]**2 for i in range(k, m))**0.5
        Q[k][k] = A[k][k] / norm
        R[k][k] = norm
        for j in range(k + 1, n):
            R[k][j] = sum(Q[i][k] * A[i][j] for i in range(k, m))
            Q[j][k] = sum(Q[i][k] * A[i][j] for i in range(k, m)) / norm
    return Q, R

def real_radical_rank(A):
    _, r = qr_decomposition(A)
    return len([x for x in r if abs(x) > 1e-9])

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    d = math.isqrt(n)
    instances_tested = 30
    support_count = 0
    counterexample = ""

    for _ in range(instances_tested):
        A = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
        M_d = [row[:] + [sum(row[i] * row[j] for i in range(n)) if j == n else 0 for j in range(n + 1)] for row in A]
        rank = real_radical_rank(M_d)
        if rank < 0.7 * math.sqrt(n):
            counterexample = f"n={n}, d={d}, rank={rank}"
            break
    else:
        support_count += 1

    return {
        "metric_name": "real_radical_rank",
        "metric_value": 0.7 * math.sqrt(n),
        "instances_tested": instances_tested,
        "conjecture_holds": support_count >= 24,  # 80% of seeds
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or list(range(2, 53))  # Default to first 30 primes

    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, **{result}}}")
        results.append(result)

    mean_metric_value = sum(res["metric_value"] for res in results) / len(results)
    std_metric_value = (sum((res["metric_value"] - mean_metric_value)**2 for res in results) / len(results))**0.5
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)

    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not res["conjecture_holds"] for res in results):
        first_failing_seed = next(seed for seed, res in zip(seeds, results) if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")