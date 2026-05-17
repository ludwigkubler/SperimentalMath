# auto-injected by SEC sandbox
import itertools
import collections
import os
import time
import re
from collections import defaultdict, Counter, deque
from itertools import product, combinations, permutations, chain
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import sys
import random
import math
import json

def matrix_multiply(A, B):
    w = len(A)
    result = [[0 for _ in range(w)] for _ in range(w)]
    for i in range(w):
        for j in range(w):
            for k in range(w):
                result[i][j] += A[i][k] * B[k][j]
    return result

def matrix_subtract(A, B):
    w = len(A)
    return [[A[i][j] - B[i][j] for j in range(w)] for i in range(w)]

def matrix_transpose(A):
    w = len(A)
    return [[A[j][i] for j in range(w)] for i in range(w)]

def frobenius_inner_product(A, B):
    w = len(A)
    product = matrix_multiply(A, matrix_transpose(B))
    trace = sum(product[i][i] for i in range(w))
    return trace

def generate_bp(w, n, seed):
    random.seed(seed)
    M = [random.choice([0, 1]) for _ in range(2*n)]
    N = [matrix_subtract(M[j], M[j-1]) if j > 0 else M[j] for j in range(2*n)]
    return N

def compute_rho(P, w):
    n = len(P) // 2
    max_inner = 0
    for u in range(n):
        for v in range(u+1, n):
            inner = abs(frobenius_inner_product(P[u], P[v]))
            if inner > max_inner:
                max_inner = inner
    if max_inner == 0:
        return 0.0
    return math.log2(max_inner) - 2 * math.log2(w)

def run_trial(seed):
    n_values = [6, 10, 16, 24, 32, 40]
    w_values = [2, 4, 8]
    metric_values = []
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""

    for n in n_values:
        for w in w_values:
            N = generate_bp(w, n, seed)
            P = [matrix_multiply(N[2*i], N[2*i+1]) for i in range(n)]
            rho = compute_rho(P, w)

            if rho > 2 * math.log2(w) + 2:
                conjecture_holds = False
                counterexample = f"Upper bound violated for n={n}, w={w}, rho={rho}"
                break

            metric_values.append(rho)
            instances_tested += 1

        if not conjecture_holds:
            break

    if conjecture_holds:
        for n in [4, 6, 8, 10]:
            w = 2 ** n
            N = generate_bp(w, n, seed)
            P = [matrix_multiply(N[2*i], N[2*i+1]) for i in range(n)]
            rho = compute_rho(P, w)

            lower_bound = n / 16 - 4 * math.log2(n)
            if rho < lower_bound:
                conjecture_holds = False
                counterexample = f"Lower bound violated for n={n}, w={w}, rho={rho}"
                break

            metric_values.append(rho)
            instances_tested += 1

    return {
        "metric_name": "operator-SoS 4-trace gap",
        "metric_value": sum(metric_values) / len(metric_values) if metric_values else 0.0,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []

    for seed in seeds:
        result = run_trial(seed)
        result["seed"] = seed
        print(f"TRIAL: {json.dumps(result)}")
        results.append(result)

    metric_values = [r["metric_value"] for r in results if "metric_value" in r]
    support_fraction = sum(r["conjecture_holds"] for r in results) / len(results) if results else 0.0

    if all(r["conjecture_holds"] for r in results):
        mean = sum(metric_values) / len(metric_values) if metric_values else 0.0
        std = (sum((x - mean) ** 2 for x in metric_values) / len(metric_values)) ** 0.5 if metric_values else 0.0
        print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        counterexample = next(r["counterexample"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")