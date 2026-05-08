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

def dot_product(v1, v2):
    return sum(x * y for x, y in zip(v1, v2))

def norm(v):
    return math.sqrt(sum(x**2 for x in v))

def matrix_multiplication(A, B):
    return [[dot_product(row, col) for col in zip(*B)] for row in A]

def gaussian_elimination(A, b):
    n = len(b)
    M = [A[i] + [b[i]] for i in range(n)]
    for i in range(n):
        max_row = max(range(i, n), key=lambda x: abs(M[x][i]))
        M[i], M[max_row] = M[max_row], M[i]
        factor = M[i][i]
        for j in range(i, n + 1):
            M[i][j] /= factor
        for k in range(n):
            if k != i:
                factor = M[k][i]
                for j in range(i, n + 1):
                    M[k][j] -= factor * M[i][j]
    return [row[-1] for row in M]

def linear_independence(vectors):
    A = vectors
    b = [0] * len(vectors)
    try:
        gaussian_elimination(A, b)
        return True
    except ZeroDivisionError:
        return False

def convex_hull(points):
    def orientation(p, q, r):
        val = (q[1] - p[1]) * (r[0] - q[0]) - (q[0] - p[0]) * (r[1] - q[1])
        if val == 0:
            return 0
        elif val > 0:
            return 1
        else:
            return 2

    def distance(p, q):
        return math.sqrt((p[0] - q[0])**2 + (p[1] - q[1])**2)

    if len(points) < 3:
        return points

    lower = []
    for p in points:
        while len(lower) >= 2 and orientation(lower[-2], lower[-1], p) != 2:
            lower.pop()
        lower.append(p)

    upper = []
    for p in reversed(points):
        while len(upper) >= 2 and orientation(upper[-2], upper[-1], p) != 2:
            upper.pop()
        upper.append(p)

    return lower[:-1] + upper[:-1]

def covering_radius(n):
    # Approximate the covering radius using a Monte Carlo method
    points = [[random.gauss(0, 1) for _ in range(n)] for _ in range(1000)]
    hull = convex_hull(points)
    max_distance = 0
    for point in hull:
        distances = [distance(point, p) for p in points]
        max_distance = max(max_distance, min(distances))
    return max_distance

def discrepancy(S):
    n = len(S)
    characteristic_vectors = [[1 if i in subset else -1 for i in range(n)] for subset in S]
    A = matrix_multiplication(characteristic_vectors, characteristic_vectors)
    b = [sum(1 for subset in S if i in subset) for i in range(n)]
    try:
        solution = gaussian_elimination(A, b)
        return max(abs(x) for x in solution)
    except ZeroDivisionError:
        return float('inf')

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = 40
    S = [set(random.sample(range(n), k=random.randint(1, n))) for _ in range(100)]
    disc_S = discrepancy(S)
    Z_n_covering_radius = covering_radius(n)
    scaled_radius = Z_n_covering_radius * (2 ** (n / 2)) / math.sqrt(math.pi * n)

    return {
        "metric_name": "discrepancy_bound",
        "metric_value": disc_S,
        "instances_tested": len(S),
        "conjecture_holds": disc_S <= scaled_radius,
        "counterexample": "" if disc_S <= scaled_radius else f"Discrepancy {disc_S} exceeds bound {scaled_radius}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
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
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = next((r["counterexample"] for r in results if not r["conjecture_holds"]), "")
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")