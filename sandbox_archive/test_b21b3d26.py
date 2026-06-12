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

def generate_boolean_function(n):
    return [random.choice([0, 1]) for _ in range(2**n)]

def matrix_add(A, B):
    return [[A[i][j] + B[i][j] for j in range(len(A[0]))] for i in range(len(A))]

def matrix_sub(A, B):
    return [[A[i][j] - B[i][j] for j in range(len(A[0]))] for i in range(len(A))]

def matrix_mul(A, B, mod):
    return [[sum((A[i][k] * B[k][j]) % mod for k in range(len(B))) % mod for j in range(len(B[0]))] for i in range(len(A))]

def identity_matrix(n, mod):
    return [[1 if i == j else 0 for j in range(n)] for i in range(n)]

def matrix_power(M, k, mod):
    result = identity_matrix(len(M), mod)
    base = M
    while k > 0:
        if k % 2 == 1:
            result = matrix_mul(result, base, mod)
        base = matrix_mul(base, base, mod)
        k //= 2
    return result

def minimal_order_brauer_group(f, n):
    I = identity_matrix(2**n, 2)
    B = [[f[i] if i == j else 0 for j in range(2**n)] for i in range(2**n)]
    A = matrix_sub(B, [I[i] for i in range(2**n)])
    order = 1
    while True:
        A = matrix_mul(A, A, 2)
        order += 1
        if all(matrix_add(A[i], B[i]) == I[i] for i in range(2**n)):
            return order

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_max = 40
    instances_tested = 0
    metric_value = 0.0
    conjecture_holds = True
    counterexample = ""

    for n in [5, 10, 15, 20, 30, 40]:
        f = generate_boolean_function(n)
        rank = minimal_order_brauer_group(f, n)
        instances_tested += 1
        metric_value += rank / (n**2 * math.log2(n))
        if rank > n**2 * math.log2(n):
            conjecture_holds = False
            counterexample = f"Function with n={n} has rank {rank}, which exceeds the expected bound."

    return {
        "metric_name": "Rank Variance",
        "metric_value": metric_value / instances_tested,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i + 3 for i in range(5, 8)]
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
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")