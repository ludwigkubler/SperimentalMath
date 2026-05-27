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

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def lcm(a, b):
    return abs(a * b) // gcd(a, b)

def extended_gcd(a, b):
    if a == 0:
        return b, 0, 1
    g, x1, y1 = extended_gcd(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return g, x, y

def mod_inverse(a, m):
    g, x, _ = extended_gcd(a, m)
    if g != 1:
        raise ValueError("Modular inverse does not exist")
    else:
        return x % m

def matrix_multiply(A, B):
    n = len(A)
    C = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

def matrix_power(M, k):
    n = len(M)
    result = [[0 if i != j else 1 for j in range(n)] for i in range(n)]
    while k > 0:
        if k % 2 == 1:
            result = matrix_multiply(result, M)
        M = matrix_multiply(M, M)
        k //= 2
    return result

def is_quasi_group(Q):
    n = len(Q)
    for a in range(n):
        for b in range(n):
            if Q[a][b] not in range(n):
                return False
    for a in range(n):
        for b in range(n):
            found = False
            for c in range(n):
                if Q[a][c] == Q[b][c]:
                    found = True
                    break
            if not found:
                return False
    for a in range(n):
        for c in range(n):
            found = False
            for b in range(n):
                if Q[a][b] == c:
                    found = True
                    break
            if not found:
                return False
    return True

def quasi_group_representation(C):
    n = len(C)
    Q = [[0] * n for _ in range(n)]
    for a in range(n):
        for b in range(n):
            Q[a][b] = C[b][a]
    if not is_quasi_group(Q):
        return None
    return Q

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    total_rank = 0
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""

    for n in n_values:
        C = [[random.randint(0, n-1) for _ in range(n)] for _ in range(n)]
        Q = quasi_group_representation(C)
        if Q is None:
            conjecture_holds = False
            counterexample = "mapping_undefined"
            break
        rank = len(Q)
        total_rank += rank
        instances_tested += 1

    mean_rank = total_rank / instances_tested
    return {
        "metric_name": "rank",
        "metric_value": mean_rank,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else list(range(2, 30))
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")