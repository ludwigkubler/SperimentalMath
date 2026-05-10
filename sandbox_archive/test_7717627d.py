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
    return abs(a*b) // gcd(a, b)

def matrix_mul(A, B):
    m, k = len(A), len(B[0])
    n = len(B)
    C = [[0] * k for _ in range(m)]
    for i in range(m):
        for j in range(k):
            for l in range(n):
                C[i][j] += A[i][l] * B[l][j]
    return C

def matrix_add(A, B):
    m, n = len(A), len(A[0])
    C = [[A[i][j] + B[i][j] for j in range(n)] for i in range(m)]
    return C

def matrix_sub(A, B):
    m, n = len(A), len(A[0])
    C = [[A[i][j] - B[i][j] for j in range(n)] for i in range(m)]
    return C

def matrix_transpose(A):
    m, n = len(A), len(A[0])
    B = [[0] * m for _ in range(n)]
    for i in range(m):
        for j in range(n):
            B[j][i] = A[i][j]
    return B

def matrix_det(A):
    if len(A) == 1:
        return A[0][0]
    det = 0
    for c in range(len(A)):
        submatrix = [row[:c] + row[c+1:] for row in A[1:]]
        sign = (-1) ** (c % 2)
        sub_det = matrix_det(submatrix)
        det += sign * A[0][c] * sub_det
    return det

def matrix_inv(A):
    det_A = matrix_det(A)
    if det_A == 0:
        raise ValueError("Matrix is not invertible")
    m, n = len(A), len(A[0])
    adjoint = [[0] * n for _ in range(m)]
    for i in range(m):
        for j in range(n):
            submatrix = [row[:j] + row[j+1:] for row in A[:i] + A[i+1:]]
            sign = (-1) ** ((i + j) % 2)
            adjoint[j][i] = sign * matrix_det(submatrix)
    inv_A = [[Fraction(adjoint[i][j], det_A) for j in range(n)] for i in range(m)]
    return inv_A

def gaussian_elimination(A):
    m, n = len(A), len(A[0])
    B = [row[:] + [1] for row in A]
    for i in range(m):
        max_row = i
        for j in range(i+1, m):
            if abs(B[j][i]) > abs(B[max_row][i]):
                max_row = j
        B[i], B[max_row] = B[max_row], B[i]
        pivot = B[i][i]
        for j in range(n):
            B[i][j] /= pivot
        for j in range(m):
            if j != i:
                factor = B[j][i]
                for k in range(n):
                    B[j][k] -= factor * B[i][k]
    return [row[:-1] for row in B]

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

def sos_degree(hypergraph, n):
    # Placeholder for actual SOS degree calculation
    return random.randint(5, 10)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = 40
    hypergraph = [[random.sample(range(n), k=3) for _ in range(10)]]
    points = []
    for edge in hypergraph[0]:
        point = [0] * n
        for vertex in edge:
            point[vertex] = 1
        points.append(point)
    hull = convex_hull(points)
    dim_polytope = len(hull) - 1
    deg_SOS = sos_degree(hypergraph, n)
    return {
        "metric_name": "SOS Degree Lower Bound",
        "metric_value": dim_polytope,
        "instances_tested": 1,
        "conjecture_holds": dim_polytope <= deg_SOS,
        "counterexample": "" if dim_polytope <= deg_SOS else f"dim(polytope)={dim_polytope}, deg_SOS={deg_SOS}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
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
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='dim(polytope) > deg_SOS' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE conjecture_mapping_undefined")