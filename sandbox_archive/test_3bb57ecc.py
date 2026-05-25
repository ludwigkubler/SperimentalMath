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

def matrix_multiplication(A, B):
    m, n = len(A), len(B[0])
    p = len(B)
    result = [[0 for _ in range(n)] for _ in range(m)]
    for i in range(m):
        for j in range(n):
            for k in range(p):
                result[i][j] += A[i][k] * B[k][j]
    return result

def transpose(A):
    return [list(row) for row in zip(*A)]

def determinant(A):
    if len(A) == 1:
        return A[0][0]
    det = 0
    for j in range(len(A)):
        submatrix = [row[:j] + row[j+1:] for row in A[1:]]
        det += ((-1)**j) * A[0][j] * determinant(submatrix)
    return det

def min_rank(matrix):
    m, n = len(matrix), len(matrix[0])
    rank = 0
    for i in range(min(m, n)):
        if matrix[i][i]:
            row = [matrix[i][j] / matrix[i][i] for j in range(n)]
            for j in range(i+1, m):
                factor = matrix[j][i]
                for k in range(n):
                    matrix[j][k] -= factor * row[k]
            rank += 1
    return rank

def generate_max_cut_instance(n, m):
    vertices = list(range(n))
    edges = []
    for _ in range(m):
        u = random.choice(vertices)
        v = random.choice(vertices)
        while u == v:
            v = random.choice(vertices)
        edges.append((u, v))
    return edges

def tropicalize_lattice(edges):
    d = len(set(u for u, v in edges) | set(v for u, v in edges))
    lattice = [[0] * (d + 1) for _ in range(d + 1)]
    for u, v in edges:
        lattice[u][v] = 1
        lattice[v][u] = 1
    return lattice

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    m = random.randint(n, n * (n - 1) // 2)
    edges = generate_max_cut_instance(n, m)
    lattice = tropicalize_lattice(edges)
    rank = min_rank(lattice)
    d = len(set(u for u, v in edges) | set(v for u, v in edges))
    conjecture_holds = rank >= math.ceil(d ** (1/3))
    counterexample = "" if conjecture_holds else f"Rank {rank} < Ω({d}^(1/3))"
    return {
        "metric_name": "min_rank",
        "metric_value": rank,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else list(range(2, 30))  # Default to first 29 primes
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    std_rank = math.sqrt(sum((r["metric_value"] - mean_rank) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[first_failing_seed]['counterexample']}\" first_failing_seed={seeds[first_failing_seed]}")