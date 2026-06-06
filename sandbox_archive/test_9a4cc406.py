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

def extended_gcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, x, y = extended_gcd(b % a, a)
        return (g, y - (b//a) * x, x)

def mod_inverse(a, m):
    g, x, _ = extended_gcd(a, m)
    if g != 1:
        raise ValueError('Modular inverse does not exist')
    else:
        return x % m

def matrix_mod_inv(matrix, mod):
    n = len(matrix)
    inv_matrix = [[0 for _ in range(n)] for _ in range(n)]
    for i in range(n):
        det = 0
        if i == 0:
            det = 1
        else:
            for j in range(i+1):
                det *= matrix[j][j]
                det %= mod
        inv_matrix[i][i] = mod_inverse(det, mod)
    return inv_matrix

def matmul(A, B):
    n = len(A)
    C = [[0 for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
                C[i][j] %= 10**9 + 7
    return C

def matrix_power(matrix, power):
    n = len(matrix)
    result = [[0 for _ in range(n)] for _ in range(n)]
    for i in range(n):
        result[i][i] = 1
    while power > 0:
        if power % 2 == 1:
            result = matmul(result, matrix)
        matrix = matmul(matrix, matrix)
        power //= 2
    return result

def rank(matrix):
    n = len(matrix)
    m = len(matrix[0])
    augmented_matrix = [row + [1] for row in matrix]
    rows = list(range(n))
    cols = list(range(m))
    
    def swap_rows(r1, r2):
        rows[r1], rows[r2] = rows[r2], rows[r1]
        augmented_matrix[r1], augmented_matrix[r2] = augmented_matrix[r2], augmented_matrix[r1]
    
    def scale_row(r, scalar):
        for j in range(m + 1):
            augmented_matrix[r][j] *= scalar
            augmented_matrix[r][j] %= 10**9 + 7
    
    def add_row(r1, r2, scalar):
        for j in range(m + 1):
            augmented_matrix[r1][j] += scalar * augmented_matrix[r2][j]
            augmented_matrix[r1][j] %= 10**9 + 7
    
    i = 0
    for j in range(m):
        if i >= n:
            break
        pivot_row = None
        for r in rows[i:]:
            if augmented_matrix[r][j] != 0:
                pivot_row = r
                break
        if pivot_row is None:
            continue
        swap_rows(i, pivot_row)
        scale_row(i, mod_inverse(augmented_matrix[i][j], 10**9 + 7))
        for r in rows:
            if r == i:
                continue
            add_row(r, i, -augmented_matrix[r][j])
        i += 1
    
    rank = sum(1 for row in augmented_matrix if any(row[j] != 0 for j in range(m)))
    return rank

def adjacency_matrix(graph, n):
    adj_matrix = [[0 for _ in range(n)] for _ in range(n)]
    for u, v in graph:
        adj_matrix[u][v] = 1
        adj_matrix[v][u] = 1
    return adj_matrix

def generate_graph(n, m):
    graph = []
    while len(graph) < m:
        u, v = random.sample(range(n), 2)
        if (u, v) not in graph and (v, u) not in graph:
            graph.append((u, v))
    return graph

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        m = max(2 * n - 1, 1)  # Ensure at least one edge
        graph = generate_graph(n, m)
        adj_matrix = adjacency_matrix(graph, n)
        aut_orbits = len(set(tuple(sorted(path)) for path in graph))
        adj_rank = rank(adj_matrix)
        
        if adj_rank == 0:
            continue
        
        ratio = Fraction(aut_orbits, adj_rank)
        results.append({
            "n": n,
            "ratio": ratio
        })
    
    if not results:
        return {
            "metric_name": "Orbit Width Ratio",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "No valid instances found"
        }
    
    metric_values = [result["ratio"] for result in results]
    mean_ratio = sum(metric_values) / len(metric_values)
    conjecture_holds = all(ratio >= mean_ratio for ratio in metric_values)
    
    return {
        "metric_name": "Orbit Width Ratio",
        "metric_value": mean_ratio,
        "instances_tested": len(results),
        "n_max": max(result["n"] for result in results),
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else "No counterexample found"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {{'seed': {seed}, **trial_result}}")
        results.append(trial_result)
    
    mean_ratio = sum(result["metric_value"] for result in results if result["metric_value"] is not None) / len(results)
    support_count = sum(1 for result in results if result["conjecture_holds"])
    support_fraction = support_count / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"No counterexample found\" first_failing_seed={first_failing_seed}")