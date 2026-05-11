# auto-injected by SEC sandbox
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from itertools import combinations

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def lcm(a, b):
    return abs(a * b) // gcd(a, b)

def extended_gcd(a, b):
    if a == 0:
        return b, 0, 1
    gcd, x1, y1 = extended_gcd(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return gcd, x, y

def mod_inverse(a, m):
    gcd, x, _ = extended_gcd(a, m)
    if gcd != 1:
        raise ValueError("Modular inverse does not exist")
    return x % m

def matrix_mod_inv(matrix, mod):
    n = len(matrix)
    det = 0
    for i in range(n):
        det += matrix[0][i] * sum(matrix[j][(i + j) % n] for j in range(1, n)) * (-1) ** (i + 2)
    det %= mod
    inv_det = mod_inverse(det, mod)
    adjugate = [[sum(matrix[(i + k) % n][(j + l) % n] * (-1) ** ((i + j) % 2) for k in range(n - 1) for l in range(n - 1)) for j in range(n)] for i in range(n)]
    inv_matrix = [[(adjugate[i][j] * inv_det) % mod for j in range(n)] for i in range(n)]
    return inv_matrix

def matrix_mul(A, B):
    n = len(A)
    m = len(B[0])
    result = [[sum(A[i][k] * B[k][j] for k in range(n)) for j in range(m)] for i in range(n)]
    return result

def gaussian_elimination(matrix):
    n = len(matrix)
    for i in range(n):
        max_row = i
        for j in range(i + 1, n):
            if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                max_row = j
        matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
        factor = matrix[i][i]
        for j in range(n):
            matrix[i][j] /= factor
        for j in range(n):
            if i != j:
                factor = matrix[j][i]
                for k in range(n):
                    matrix[j][k] -= factor * matrix[i][k]
    return matrix

def determinant(matrix):
    n = len(matrix)
    det = 0
    if n == 1:
        return matrix[0][0]
    elif n == 2:
        return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
    else:
        for i in range(n):
            det += (-1) ** i * matrix[0][i] * determinant([row[:i] + row[i+1:] for row in matrix[1:]])
    return det

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
        return math.sqrt((p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2)

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

def generate_max_cut_instance(n, density):
    edges = []
    for i in range(n):
        for j in range(i + 1, n):
            if random.random() < density:
                edges.append((i, j))
    return edges

def map_clauses_to_monomials(edges, n):
    monomials = set()
    for u, v in edges:
        monomials.add(f"x{u} * x{v}")
        monomials.add(f"x{u} + x{v}")
        monomials.add(f"1 - x{u} - x{v}")
    return list(monomials)

def compute_newton_polytope_volume(monomials):
    n = len(monomials)
    vertices = []
    for i in range(n):
        vertex = [0] * n
        vertex[i] = 1
        vertices.append(vertex)
    vertices = convex_hull(vertices)
    volume = determinant([[sum(v[j] * v[k] for j, v in enumerate(row)) for k in range(len(row))] for row in vertices])
    return abs(volume)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = 20
    density = random.uniform(0.1, 0.5)
    edges = generate_max_cut_instance(n, density)
    monomials = map_clauses_to_monomials(edges, n)
    if not monomials:
        return {
            "metric_name": "volume",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    volume = compute_newton_polytope_volume(monomials)
    d = len(edges) // n
    if d == 0:
        return {
            "metric_name": "volume",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "degree_zero"
        }
    expected_volume = 1 / (d ** 2)
    if volume is not None and abs(volume - expected_volume) < 0.01:
        return {
            "metric_name": "volume",
            "metric_value": volume,
            "instances_tested": 1,
            "conjecture_holds": True,
            "counterexample": ""
        }
    else:
        return {
            "metric_name": "volume",
            "metric_value": volume,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": f"expected {expected_volume}, got {volume}"
        }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_volume = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_volume = math.sqrt(sum((r["metric_value"] - mean_volume) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_volume} std={std_volume} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_volume} std={std_volume} support_fraction={support_fraction}")
    else:
        for r in results:
            if not r["conjecture_holds"]:
                print(f"RESULT: FALSIFIED counterexample=\"{r['counterexample']}\" first_failing_seed={seed}")
                break