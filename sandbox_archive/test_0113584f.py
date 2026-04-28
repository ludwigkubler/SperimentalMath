# auto-injected by SEC sandbox
import itertools
import collections
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
import json

def gaussian_elimination(A):
    m, n = len(A), len(A[0])
    for i in range(m):
        max_row = i
        for j in range(i+1, m):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        if A[i][i] == 0:
            return None
        for j in range(i+1, n):
            A[i][j] /= A[i][i]
        A[i][i] = 1
        for j in range(m):
            if j != i and A[j][i] != 0:
                factor = A[j][i]
                for k in range(n):
                    A[j][k] -= factor * A[i][k]
    return A

def matrix_multiply(A, B):
    m, n, p = len(A), len(B), len(B[0])
    C = [[0] * p for _ in range(m)]
    for i in range(m):
        for j in range(p):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

def nullity(matrix):
    rank = 0
    A = [row[:] for row in matrix]
    if not gaussian_elimination(A):
        return len(matrix[0])
    for row in A:
        if any(row):
            rank += 1
    return len(matrix[0]) - rank

def build_star_complex(G):
    n = len(G)
    edges = [(i, j) for i in range(n) for j in range(i+1, n) if G[i][j]]
    edge_pairs = []
    vertex_stars = []
    
    for e1, e2 in combinations(edges, 2):
        u, v = e1
        x, y = e2
        if u == x or u == y or v == x or v == y:
            edge_pairs.append((e1, e2))
    
    for i in range(n):
        star_edges = [e for e in edges if i in e]
        vertex_stars.append(star_edges)
    
    return edges, edge_pairs, vertex_stars

def meet_in_the_middle(G, c):
    n = len(G)
    m = sum(sum(row) for row in G)
    clauses = [(i, j) for i in range(n) for j in range(i+1, n) if G[i][j]]
    m = len(clauses)
    
    half = m // 2
    xor_dict = {}
    
    for subset in range(1 << half):
        xor_sum = (0, 0)
        for i in range(half):
            if subset & (1 << i):
                xor_sum = (xor_sum[0] ^ clauses[i][0], xor_sum[1] ^ clauses[i][1])
        xor_dict[xor_sum] = subset
    
    min_cost = float('inf')
    
    for subset in range(1 << half):
        xor_sum = (0, 0)
        for i in range(half, m):
            if subset & (1 << (i - half)):
                xor_sum = (xor_sum[0] ^ clauses[i][0], xor_sum[1] ^ clauses[i][1])
        if xor_sum in xor_dict:
            cost = bin(subset).count('1') + bin(xor_dict[xor_sum]).count('1')
            min_cost = min(min_cost, cost)
    
    return min_cost

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.choice([8, 10, 12, 14, 16])
    G = [[0] * n for _ in range(n)]
    degree_sum = 0
    while True:
        for i in range(n):
            neighbors = [j for j in range(i+1, n) if random.choice([True, False])]
            for j in neighbors:
                G[i][j] = G[j][i] = 1
                degree_sum += 2
        if degree_sum == n * (n - 1):
            break
    
    c = [random.choice([0, 1]) for _ in range(n)]
    
    edges, edge_pairs, vertex_stars = build_star_complex(G)
    L1 = [[0] * len(edges) for _ in range(len(edges))]
    L2 = [[0] * len(edge_pairs) for _ in range(len(vertex_stars))]
    
    for i, (u, v) in enumerate(edges):
        for j, (e1, e2) in enumerate(edge_pairs):
            if u == e1[0] and v == e1[1]:
                L1[i][j] = 1
            if u == e2[0] and v == e2[1]:
                L1[i][j] = 1
    
    for i, (u, v) in enumerate(edges):
        for j, star_edges in enumerate(vertex_stars):
            for k, (x, y) in enumerate(star_edges):
                if u == x and v == y:
                    L2[i][j] = 1
                if u == x or u == y or v == x or v == y:
                    L2[i][j] = 1
    
    h1 = nullity(matrix_multiply(L1, L1) + matrix_multiply(L2, L2))
    
    g_star = meet_in_the_middle(G, c)
    
    conjecture_holds = g_star >= math.ceil(h1 / (4 * 3)) + 1
    counterexample = "" if conjecture_holds else "g* < ceil(h1/(Δ*(Δ-1))) + 1"
    
    return {
        "metric_name": "g_star",
        "metric_value": g_star,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [11, 23, 37, 53, 71]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {json.dumps(result)}")
        results.append(result)
    
    mean_g_star = sum(r["metric_value"] for r in results) / len(results)
    std_g_star = math.sqrt(sum((r["metric_value"] - mean_g_star) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.95:
        print(f"RESULT: SUPPORTED mean={mean_g_star} std={std_g_star} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient evidence")