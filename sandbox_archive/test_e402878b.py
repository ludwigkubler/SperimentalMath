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
    m, n = len(A), len(B[0])
    p = len(B)
    C = [[0 for _ in range(n)] for _ in range(m)]
    for i in range(m):
        for j in range(n):
            for k in range(p):
                C[i][j] += A[i][k] * B[k][j]
    return C

def gaussian_elimination(A, b):
    n = len(b)
    for i in range(n):
        max_row = i
        for j in range(i+1, n):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        b[i], b[max_row] = b[max_row], b[i]
        for j in range(i+1, n):
            factor = A[j][i] / A[i][i]
            for k in range(i, n):
                A[j][k] -= factor * A[i][k]
            b[j] -= factor * b[i]
    x = [0] * n
    for i in range(n-1, -1, -1):
        x[i] = (b[i] - sum(A[i][j] * x[j] for j in range(i+1, n))) / A[i][i]
    return x

def random_polyhedron(n):
    vertices = [[random.uniform(-1, 1) for _ in range(3)] for _ in range(n)]
    facets = []
    for i in range(n):
        for j in range(i+1, n):
            for k in range(j+1, n):
                v1, v2, v3 = vertices[i], vertices[j], vertices[k]
                a = v2[0] - v1[0], v2[1] - v1[1], v2[2] - v1[2]
                b = v3[0] - v1[0], v3[1] - v1[1], v3[2] - v1[2]
                c = a[1]*b[2] - a[2]*b[1], a[2]*b[0] - a[0]*b[2], a[0]*b[1] - a[1]*b[0]
                d = -c[0]*v1[0] - c[1]*v1[1] - c[2]*v1[2]
                facets.append((c, d))
    return vertices, facets

def hyperplane_section(vertices, facets):
    n = len(vertices)
    min_dist = float('inf')
    for i in range(n):
        for j in range(i+1, n):
            v1, v2 = vertices[i], vertices[j]
            a = v2[0] - v1[0], v2[1] - v1[1], v2[2] - v1[2]
            d = -a[0]*v1[0] - a[1]*v1[1] - a[2]*v1[2]
            dist = abs(d) / math.sqrt(a[0]**2 + a[1]**2 + a[2]**2)
            min_dist = min(min_dist, dist)
    return min_dist

def communication_complexity(n):
    return n * math.log2(n)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = 30
    metric_name = "min_geometric_invariant"
    instances_tested = 100
    total_metric_value = 0
    conjecture_holds = True
    counterexample = ""

    for _ in range(instances_tested):
        vertices, facets = random_polyhedron(n)
        min_dist = hyperplane_section(vertices, facets)
        total_metric_value += min_dist

        if min_dist < n * math.log2(n):
            conjecture_holds = False
            counterexample = f"n={n}, min_dist={min_dist}"

    mean_metric_value = total_metric_value / instances_tested
    return {
        "metric_name": metric_name,
        "metric_value": mean_metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else list(range(2, 30))
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    if support_fraction >= 0.9:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=NA support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")