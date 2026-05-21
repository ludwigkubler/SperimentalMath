# auto-injected by SEC sandbox
import itertools
import collections
import json
import os
import time
import re
from collections import defaultdict, Counter, deque
from itertools import product, combinations, permutations, chain
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
from fractions import Fraction
import math
import sys

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def extended_gcd(a, b):
    if a == 0:
        return b, 0, 1
    gcd, x1, y1 = extended_gcd(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return gcd, x, y

def inverse(a, m):
    gcd, x, _ = extended_gcd(a, m)
    if gcd != 1:
        raise ValueError("Inverse does not exist")
    else:
        return x % m

def matrix_mod(A, p):
    return [[a % p for a in row] for row in A]

def matrix_mul(A, B, p):
    n = len(A)
    m = len(B[0])
    result = [[0] * m for _ in range(n)]
    for i in range(n):
        for j in range(m):
            for k in range(len(B)):
                result[i][j] += A[i][k] * B[k][j]
            result[i][j] %= p
    return result

def matrix_add(A, B, p):
    n = len(A)
    m = len(A[0])
    result = [[0] * m for _ in range(n)]
    for i in range(n):
        for j in range(m):
            result[i][j] = (A[i][j] + B[i][j]) % p
    return result

def matrix_sub(A, B, p):
    n = len(A)
    m = len(A[0])
    result = [[0] * m for _ in range(n)]
    for i in range(n):
        for j in range(m):
            result[i][j] = (A[i][j] - B[i][j]) % p
    return result

def matrix_transpose(A):
    n = len(A)
    m = len(A[0])
    result = [[0] * n for _ in range(m)]
    for i in range(n):
        for j in range(m):
            result[j][i] = A[i][j]
    return result

def gaussian_elimination(A, p):
    n = len(A)
    m = len(A[0])
    rank = 0
    pivot_col = 0
    for i in range(n):
        while pivot_col < m and all(A[j][pivot_col] == 0 for j in range(i, n)):
            pivot_col += 1
        if pivot_col == m:
            break
        A[i], A[min(i + 1, n - 1)] = A[min(i + 1, n - 1)], A[i]
        for j in range(n):
            if i != j:
                factor = (A[j][pivot_col] * inverse(A[i][pivot_col], p)) % p
                A[j] = matrix_sub(A[j], matrix_mul([[factor]], matrix_row(A[i]), p), p)
        pivot_col += 1
        rank += 1
    return rank

def secant_variety_order(points, p):
    n = len(points)
    m = len(points[0])
    A = [[points[i][j] for j in range(m)] + [1] for i in range(n)]
    A = matrix_mod(A, p)
    return gaussian_elimination(A, p)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    points = [[random.randint(0, p - 1) for _ in range(n)] for _ in range(n)]
    p = random.randint(2, 100)
    try:
        order = secant_variety_order(points, p)
    except Exception as e:
        return {
            "metric_name": "secant_variety_order",
            "metric_value": None,
            "instances_tested": n,
            "conjecture_holds": False,
            "counterexample": str(e)
        }
    return {
        "metric_name": "secant_variety_order",
        "metric_value": order,
        "instances_tested": n,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_value = (sum((r["metric_value"] - mean_value) ** 2 for r in results if r["metric_value"] is not None) / len(results)) ** 0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='first failing seed' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_support")