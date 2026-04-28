# auto-injected by SEC sandbox
import itertools
import collections
import json
import os
import time
import re
from collections import defaultdict, Counter, deque
from itertools import product, combinations, permutations, chain
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import sys
import random
import math

def gaussian_elimination(A):
    n = len(A)
    for i in range(n):
        max_row = i
        for j in range(i+1, n):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        for j in range(i+1, n):
            factor = A[j][i] / A[i][i]
            for k in range(n):
                A[j][k] -= factor * A[i][k]
    return A

def matrix_rank(A, tol=1e-9):
    A = gaussian_elimination(A)
    rank = 0
    for row in A:
        if any(abs(x) > tol for x in row):
            rank += 1
    return rank

def build_star_complex(G):
    n = len(G)
    edges = []
    edge_pairs = []
    vertex_stars = []
    
    for i in range(n):
        for j in range(i+1, n):
            if G[i][j] == 1:
                edges.append((i, j))
                for k in range(j+1, n):
                    if G[j][k] == 1 and G[k][i] == 1:
                        edge_pairs.append(((i, j), (j, k)))
                        vertex_stars.append(((i, j), (j, k), (k, i)))
    
    return edges, edge_pairs, vertex_stars

def compute_h1(G):
    n = len(G)
    edges, _, _ = build_star_complex(G)
    A1 = [[0] * n for _ in range(n)]
    for u, v in edges:
        A1[u][v] = 1
        A1[v][u] = 1
    
    return matrix_rank(A1)

def meet_in_the_middle(clauses):
    m = len(clauses)
    half = m // 2
    xor_dict = {}
    
    for subset in range(1 << half):
        a_C, b_C = 0, 0
        for j in range(half):
            if subset & (1 << j):
                a_C ^= clauses[j][0]
                b_C ^= clauses[j][1]
        xor_dict[(a_C, b_C)] = subset
    
    min_size = float('inf')
    for i in range(1 << half):
        a_T1, b_T1 = 0, 0
        for j in range(half):
            if i & (1 << j):
                a_T1 ^= clauses[j][0]
                b_T1 ^= clauses[j][1]
        
        a_T2, b_T2 = 0, 0
        for j in range(half, m):
            if i & (1 << (j - half)):
                a_T2 ^= clauses[j][0]
                b_T2 ^= clauses[j][1]
        
        xor_key = (a_T1 ^ a_T2, b_T1 ^ b_T2)
        if xor_key in xor_dict:
            size = bin(i).count('1') + bin(xor_dict[xor_key]).count('1')
            min_size = min(min_size, size)
    
    return min_size

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n = random.choice([8, 10, 12, 14, 16])
    G = [[0] * n for _ in range(n)]
    degree_sum = 0
    while True:
        for i in range(n):
            for j in range(i+1, n):
                if random.random() < 3 / (n - 1):
                    G[i][j] = G[j][i] = 1
                    degree_sum += 2
    
    if degree_sum % 2 != 0:
        c = [random.choice([0, 1]) for _ in range(n)]
    else:
        return {
            "metric_name": "g*(T(G,c))",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    h1 = compute_h1(G)
    clauses = []
    for i in range(n):
        for j in range(i+1, n):
            if G[i][j] == 1:
                for k in range(j+1, n):
                    if G[j][k] == 1 and G[k][i] == 1:
                        clauses.append(((i, j), (j, k)))
    
    g_star = meet_in_the_middle(clauses)
    bound = math.ceil(h1 / (4 * 3)) + 1
    
    return {
        "metric_name": "g*(T(G,c))",
        "metric_value": g_star,
        "instances_tested": 1,
        "conjecture_holds": g_star >= bound,
        "counterexample": "" if g_star >= bound else f"g*={g_star} < {bound}"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [11, 23, 37, 53, 71]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    total_trials = sum(r["instances_tested"] for r in results)
    mean_value = sum(r["metric_value"] for r in results) / total_trials
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / total_trials)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE")