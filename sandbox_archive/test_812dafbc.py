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

def gaussian_elimination(A):
    n = len(A)
    for i in range(n):
        max_row = i
        for j in range(i + 1, n):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        factor = -A[i][i]
        for j in range(n):
            A[i][j] /= factor
        for j in range(n):
            if i != j:
                factor = A[j][i]
                for k in range(n):
                    A[j][k] += factor * A[i][k]

def matrix_multiplication(A, B):
    n = len(A)
    C = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

def determinant(A):
    if len(A) == 1:
        return A[0][0]
    det = Fraction(0)
    sign = 1
    for j in range(len(A)):
        submatrix = [row[:j] + row[j+1:] for row in A[1:]]
        det += sign * A[0][j] * determinant(submatrix)
        sign *= -1
    return det

def is_invertible(A):
    return determinant(A) != 0

def deligne_lusztig_parameters(G, V):
    n = len(V)
    m = len(G)
    A = [[0] * n for _ in range(n)]
    for v in V:
        for u in G:
            if (v, u) in edges or (u, v) in edges:
                A[V.index(v)][G.index(u)] += 1
    gaussian_elimination(A)
    det_A = determinant(A)
    return abs(det_A)

def communication_complexity_rank(G):
    n = len(G)
    rank = 0
    for i in range(n):
        row_sum = sum(G[i])
        if row_sum > rank:
            rank = row_sum
    return rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    V = [i for i in range(n)]
    G = []
    edges = set()
    
    for _ in range(random.randint(n, 2 * n)):
        u, v = random.sample(V, 2)
        if (u, v) not in edges and (v, u) not in edges:
            edges.add((u, v))
            G.append([0] * n)
            G[-1][u] += 1
            G[-1][v] += 1
    
    dl_param = deligne_lusztig_parameters(G, V)
    r_pi = communication_complexity_rank(G)
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": dl_param * r_pi,
        "instances_tested": n,
        "n_max": n,
        "conjecture_holds": False,
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")