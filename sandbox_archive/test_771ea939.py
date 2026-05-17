# auto-injected by SEC sandbox
import collections
import json
import os
import time
import re
from collections import defaultdict, Counter, deque
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import sys
import random
import math
import itertools
from fractions import Fraction

def generate_random_monotone_function(n, num_minterms, seed):
    random.seed(seed)
    minterms = []
    for _ in range(num_minterms):
        m = tuple(random.randint(0, 1) for _ in range(n))
        minterms.append(m)
    M = set(minterms)
    K = set()
    for m in M:
        for k in itertools.product([0, 1], repeat=n):
            if all(m[i] <= k[i] for i in range(n)):
                K.add(k)
    return M, K

def build_bipartite_graph(M, K):
    n = len(next(iter(M))) if M else 0
    ground_vertex = tuple([2] * n)
    vertices = list(M) + list(K) + [ground_vertex]
    edges = {}
    for m in M:
        for k in K:
            if all(m[i] <= k[i] for i in range(n)):
                edges[(m, k)] = edges.get((m, k), 0) + 1
        edges[(k, ground_vertex)] = edges.get((k, ground_vertex), 0) + 1
    return vertices, edges

def matrix_mult(A, B):
    result = [[0 for _ in range(len(B[0]))] for _ in range(len(A))]
    for i in range(len(A)):
        for j in range(len(B[0])):
            for k in range(len(B)):
                result[i][j] += A[i][k] * B[k][j]
    return result

def matrix_sub(A, B):
    return [[A[i][j] - B[i][j] for j in range(len(A[0]))] for i in range(len(A))]

def matrix_transpose(A):
    return [[A[j][i] for j in range(len(A))] for i in range(len(A[0]))]

def matrix_minor(A, i, j):
    return [row[:j] + row[j+1:] for row in (A[:i] + A[i+1:])]

def matrix_determinant(A):
    n = len(A)
    if n == 1:
        return A[0][0]
    if n == 2:
        return A[0][0] * A[1][1] - A[0][1] * A[1][0]
    det = 0
    for j in range(n):
        det += ((-1) ** j) * A[0][j] * matrix_determinant(matrix_minor(A, 0, j))
    return det

def compute_spanning_trees(vertices, edges):
    n = len(vertices)
    if n <= 1:
        return 1
    laplacian = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if i == j:
                laplacian[i][j] = sum(edges.get((vertices[i], vertices[k]), 0) for k in range(n) if k != i)
            else:
                laplacian[i][j] = -edges.get((vertices[i], vertices[j]), 0)
    reduced_laplacian = [row[1:] for row in laplacian[1:]]
    det = matrix_determinant(reduced_laplacian)
    return det

def compute_sigma(M, K):
    vertices, edges = build_bipartite_graph(M, K)
    tau = compute_spanning_trees(vertices, edges)
    sigma = math.log2(1 + tau)
    return sigma

def compute_dkw(M, K):
    n = len(next(iter(M))) if M else 0
    if not M or not K:
        return 0
    min_depth = float('inf')
    for m in M:
        for k in K:
            if all(m[i] <= k[i] for i in range(n)):
                depth = sum(1 for i in range(n) if m[i] != k[i])
                if depth < min_depth:
                    min_depth = depth
    return min_depth

def run_trial(seed):
    random.seed(seed)
    n = random.choice([4, 5, 6, 7, 8])
    num_minterms = random.randint(2, 6)
    M, K = generate_random_monotone_function(n, num_minterms, seed)
    sigma = compute_sigma(M, K)
    dkw = compute_dkw(M, K)
    bound = dkw * (len(M) + len(K) + 1) * math.log2(n + 2)
    conjecture_holds = sigma <= bound
    counterexample = "" if conjecture_holds else f"sigma={sigma} > bound={bound}"
    return {
        "metric_name": "sigma",
        "metric_value": sigma,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

def main():
    seeds = [int(arg) for arg in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        result["seed"] = seed
        print(f"TRIAL: {result}")
        results.append(result)
    metric_values = [r["metric_value"] for r in results]
    mean = sum(metric_values) / len(metric_values)
    std = math.sqrt(sum((x - mean) ** 2 for x in metric_values) / len(metric_values))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
    else:
        failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        counterexample = next(r["counterexample"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={failing_seed}")

if __name__ == "__main__":
    main()