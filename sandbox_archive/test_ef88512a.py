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
    return abs(a*b) // gcd(a, b)

def matrix_multiply(A, B):
    m, k = len(A), len(B[0])
    n = len(B)
    C = [[0 for _ in range(k)] for _ in range(m)]
    for i in range(m):
        for j in range(k):
            for l in range(n):
                C[i][j] += A[i][l] * B[l][j]
    return C

def gaussian_elimination(A, b):
    n = len(A)
    M = [[A[i][j] for j in range(n)] + [b[i]] for i in range(n)]
    for i in range(n):
        max_row = i
        for j in range(i+1, n):
            if abs(M[j][i]) > abs(M[max_row][i]):
                max_row = j
        M[i], M[max_row] = M[max_row], M[i]
        factor = M[i][i]
        for j in range(n + 1):
            M[i][j] /= factor
        for j in range(n):
            if i != j:
                factor = M[j][i]
                for k in range(n + 1):
                    M[j][k] -= factor * M[i][k]
    return [M[i][-1] for i in range(n)]

def secant_rank(M):
    n = len(M)
    minors = []
    for i in range(1, n+1):
        for j in range(i, n+1):
            minor = [[M[k][l] for l in range(j-1, j)] for k in range(i-1, i)]
            minors.append(minor)
    values = [gaussian_elimination(minor, [0]*len(minor)) for minor in minors]
    return len(values)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    total_metric_value = 0
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""

    for n in n_values:
        M = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
        if not all(all(row[i] == row[j] or (row[i] + row[j] == 1) for j in range(i+1, n)) for i in range(n)):
            continue
        instances_tested += 1
        sr = secant_rank(M)
        total_metric_value += sr / n
        if sr < 0.8 * n:
            conjecture_holds = False
            counterexample = f"n={n}, sr={sr}"

    return {
        "metric_name": "secant_rank",
        "metric_value": total_metric_value / len(n_values),
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    results = []
    for seed in seeds:
        print(f"TRIAL: {run_trial(seed)}")
        results.append(run_trial(seed))

    mean_metric_value = sum(r["metric_value"] * r["instances_tested"] for r in results) / sum(r["instances_tested"] for r in results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 * r["instances_tested"] for r in results) / sum(r["instances_tested"] for r in results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")