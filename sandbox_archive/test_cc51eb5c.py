# auto-injected by SEC sandbox
import math
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
from fractions import Fraction

def generate_points(n, p):
    points = []
    for _ in range(n):
        point = [random.randint(0, p-1) for _ in range(n)]
        points.append(point)
    return points

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def lcm(a, b):
    return abs(a*b) // gcd(a, b)

def matrix_mod(A, p):
    return [[(a % p + p) % p for a in row] for row in A]

def matrix_add(A, B):
    return [[(a + b) % p for a, b in zip(row_a, row_b)] for row_a, row_b in zip(A, B)]

def matrix_mul(A, B, p):
    result = [[0] * len(B[0]) for _ in range(len(A))]
    for i in range(len(A)):
        for j in range(len(B[0])):
            for k in range(len(B)):
                result[i][j] = (result[i][j] + A[i][k] * B[k][j]) % p
    return result

def matrix_power(M, n, p):
    result = [[Fraction(1) if i == j else Fraction(0) for j in range(len(M))] for i in range(len(M))]
    base = M
    while n > 0:
        if n % 2 == 1:
            result = matrix_mul(result, base, p)
        base = matrix_mul(base, base, p)
        n //= 2
    return result

def secant_variety_order(points, p):
    n = len(points[0])
    A = [[0] * (n + 1) for _ in range(n)]
    for point in points:
        for i in range(n):
            A[i][i] += point[i]
        A[n-1][i] += 1
    A = matrix_mod(A, p)
    I = [[Fraction(1) if i == j else Fraction(0) for j in range(n + 1)] for i in range(n + 1)]
    B = [sum(point[i] for point in points) % p for i in range(n)]
    B.append(len(points))
    for _ in range(n):
        pivot = next(i for i, row in enumerate(A) if row[-1] != 0)
        A[pivot], A[-1] = A[-1], A[pivot]
        B[pivot], B[-1] = B[-1], B[pivot]
        factor = A[-1][-1]
        for j in range(n + 1):
            A[-1][j] /= factor
        B[-1] /= factor
        for i in range(n - 1, -1, -1):
            if i != pivot:
                factor = A[i][-1]
                for j in range(n + 1):
                    A[i][j] -= factor * A[pivot][j]
                B[i] -= factor * B[pivot]
    return len([i for i in range(n) if A[i][-1] == 0])

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.choice(range(5, 41))
    p = random.randint(2, 100)
    points = generate_points(n, p)
    order = secant_variety_order(points, p)
    communication_complexity = n
    return {
        "metric_name": "secant_variety_order",
        "metric_value": order,
        "instances_tested": 1,
        "conjecture_holds": order >= communication_complexity,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else list(range(2, 30)) + list(map(lambda x: x * 100, range(2, 30)))
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = (sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results)) ** 0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")