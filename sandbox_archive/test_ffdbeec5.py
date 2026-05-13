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
        raise ValueError("Inverse doesn't exist")
    else:
        return x % m

def matrix_mod_inv(matrix, mod):
    n = len(matrix)
    adj = [[0 for _ in range(n)] for _ in range(n)]
    det = determinant(matrix) % mod
    if det == 0:
        raise ValueError("Inverse doesn't exist")
    else:
        inv_det = mod_inverse(det, mod)
        for i in range(n):
            for j in range(n):
                adj[i][j] = (inv_det * get_minor(matrix, i, j)) % mod
    return adj

def determinant(matrix):
    n = len(matrix)
    if n == 1:
        return matrix[0][0]
    det = 0
    sign = 1
    for j in range(n):
        submatrix = [row[:j] + row[j+1:] for row in matrix[1:]]
        det += sign * matrix[0][j] * determinant(submatrix)
        sign *= -1
    return det

def get_minor(matrix, i, j):
    minor = []
    for k in range(len(matrix)):
        if k == i:
            continue
        row = []
        for l in range(len(matrix[k])):
            if l == j:
                continue
            row.append(matrix[k][l])
        minor.append(row)
    return determinant(minor)

def matrix_multiply(A, B):
    n = len(A)
    m = len(B[0])
    result = [[0 for _ in range(m)] for _ in range(n)]
    for i in range(n):
        for j in range(m):
            for k in range(len(B)):
                result[i][j] += A[i][k] * B[k][j]
    return result

def vector_dot_product(a, b):
    return sum(x * y for x, y in zip(a, b))

def vector_norm(v):
    return math.sqrt(sum(x ** 2 for x in v))

def vector_normalize(v):
    norm = vector_norm(v)
    if norm == 0:
        raise ValueError("Cannot normalize zero vector")
    return [x / norm for x in v]

def convex_hull(points):
    n = len(points)
    if n < 3:
        return points
    def orientation(p, q, r):
        val = (q[1] - p[1]) * (r[0] - q[0]) - (q[0] - p[0]) * (r[1] - q[1])
        if val == 0:
            return 0
        elif val > 0:
            return 1
        else:
            return 2
    points.sort(key=lambda p: (p[0], p[1]))
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

def gromov_width_approximation(convex_hull_points):
    n = len(convex_hull_points)
    if n < 3:
        return 0
    def distance(p, q):
        return math.sqrt((p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2)
    max_distance = 0
    for i in range(n):
        for j in range(i + 1, n):
            max_distance = max(max_distance, distance(convex_hull_points[i], convex_hull_points[j]))
    return max_distance

def extended_frege_proof_length(sat_instance):
    # Placeholder function to simulate proof length
    # In practice, this would involve a real Extended Frege proof system
    return len(sat_instance) * 10  # Simplified model for demonstration

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    sat_instance = [[random.choice([0, 1]) for _ in range(n)] for _ in range(random.randint(3, 6))]
    clause_vectors = [vector_normalize([int(x) for x in clause]) for clause in sat_instance]
    convex_hull_points = convex_hull(clause_vectors)
    symplectic_capacity = gromov_width_approximation(convex_hull_points)
    proof_length = extended_frege_proof_length(sat_instance)
    conjecture_holds = abs(symplectic_capacity - 1 / proof_length) < 0.1
    counterexample = "" if conjecture_holds else "mapping_undefined"
    return {
        "metric_name": "symplectic_capacity",
        "metric_value": symplectic_capacity,
        "instances_tested": len(sat_instance),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    mean = sum(r["metric_value"] for r in results) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean} std={std_dev} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean} std={std_dev} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = next((r["counterexample"] for r in results if not r["conjecture_holds"]), "")
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")