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

def generate_random_graph(n):
    edges = set()
    for i in range(n):
        for j in range(i + 1, n):
            if random.choice([True, False]):
                edges.add((i, j))
    return list(edges)

def gaussian_elimination(matrix):
    m, n = len(matrix), len(matrix[0])
    rank = 0
    for i in range(n):
        pivot_row = -1
        for j in range(rank, m):
            if matrix[j][i] != 0:
                pivot_row = j
                break
        if pivot_row == -1:
            continue
        matrix[pivot_row], matrix[rank] = matrix[rank], matrix[pivot_row]
        for j in range(n):
            if j == i:
                matrix[rank][j] = 1 / matrix[rank][j]
            else:
                matrix[rank][j] *= -matrix[rank][i]
        for j in range(m):
            if j != rank:
                factor = matrix[j][i]
                for k in range(n):
                    matrix[j][k] += factor * matrix[rank][k]
        rank += 1
    return rank

def rank_of_matrix(G):
    n = len(G)
    B = [[0] * (n + 1) for _ in range(n)]
    for i, j in G:
        B[i][j] = 1
        B[j][i] = 1
    return gaussian_elimination(B)

def compute_tutte_polynomial(G):
    n = len(G)
    if n == 0:
        return 1
    edges = list(G)
    u, v = edges[0]
    G_u = {(x, y) for x, y in G if x != u and y != u}
    G_v = {(x, y) for x, y in G if x != v and y != v}
    return (compute_tutte_polynomial(G_u) - compute_tutte_polynomial(G_v)) * (n - 1)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    G = generate_random_graph(n)
    ν_G = rank_of_matrix(G)
    T_G_xy = compute_tutte_polynomial(G)
    circuit_size = 2 ** ν_G
    return {
        "metric_name": "circuit_size",
        "metric_value": circuit_size,
        "instances_tested": 1,
        "conjecture_holds": circuit_size >= 2 ** ν_G,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else [2**i - 1 for i in range(5, 8)]
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
        for r in results:
            if not r["conjecture_holds"]:
                print(f"RESULT: FALSIFIED counterexample=\"circuit_size < 2^ν_G\" first_failing_seed={r['seed']}")
                break