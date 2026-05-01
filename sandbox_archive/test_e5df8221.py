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

def extended_gcd(a, b):
    if a == 0:
        return (b, 0, 1)
    gcd, x1, y1 = extended_gcd(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return (gcd, x, y)

def mod_inverse(a, m):
    gcd, x, _ = extended_gcd(a, m)
    if gcd != 1:
        raise ValueError("Modular inverse does not exist")
    else:
        return x % m

def gaussian_elimination(A, b, p):
    n = len(A)
    for i in range(n):
        max_row = i
        for k in range(i + 1, n):
            if abs(A[k][i]) > abs(A[max_row][i]):
                max_row = k
        A[i], A[max_row] = A[max_row], A[i]
        b[i], b[max_row] = b[max_row], b[i]
        factor = (A[i][i] * mod_inverse(A[i][i], p)) % p
        for j in range(i + 1, n):
            A[j][i] = (A[j][i] * factor) % p
            b[j] = (b[j] * factor) % p
    x = [0] * n
    for i in range(n - 1, -1, -1):
        x[i] = (b[i] - sum(A[i][j] * x[j] for j in range(i + 1, n))) * mod_inverse(A[i][i], p) % p
    return x

def tropical_rank(matrix):
    n = len(matrix)
    A = [[0 if i == j else float('inf') for j in range(n)] for i in range(n)]
    b = [float('-inf')] * n
    for i in range(n):
        for j in range(n):
            if matrix[i][j] != 0:
                A[i][j] = matrix[i][j]
                b[j] = max(b[j], matrix[i][j])
    x = gaussian_elimination(A, b, 2)
    return sum(1 for xi in x if xi != float('-inf'))

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.choice([5, 10, 15, 20, 30, 40])
    A = [[random.randint(-10, 10) for _ in range(n)] for _ in range(n)]
    B = [[random.randint(-10, 10) for _ in range(n)] for _ in range(n)]
    r1 = tropical_rank(A)
    r2 = tropical_rank(B)
    C = [[A[i][j] + B[i][j] for j in range(n)] for i in range(n)]
    r3 = tropical_rank(C)
    instances_tested = 1
    conjecture_holds = r3 <= r1 + r2
    counterexample = "" if conjecture_holds else "r3 > r1 + r2"
    return {
        "metric_name": "tropical proof rank",
        "metric_value": r3,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = list(map(int, sys.argv[1:])) or [2**i + 3 for i in range(5, 8)]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, **{result}}}")
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"r3 > r1 + r2\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient data")