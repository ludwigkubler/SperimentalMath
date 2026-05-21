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

# Helper functions for linear algebra
def matrix_multiply(A, B):
    rows_A = len(A)
    cols_A = len(A[0])
    rows_B = len(B)
    cols_B = len(B[0])
    if cols_A != rows_B:
        raise ValueError("Incompatible dimensions for matrix multiplication")
    
    C = [[sum(A[i][k] * B[k][j] for k in range(cols_A)) for j in range(cols_B)] for i in range(rows_A)]
    return C

def transpose(M):
    return [list(row) for row in zip(*M)]

def identity_matrix(n):
    return [[1 if i == j else 0 for j in range(n)] for i in range(n)]

def qr_decomposition(A):
    rows = len(A)
    cols = len(A[0])
    Q = identity_matrix(rows)
    R = A.copy()
    
    for k in range(cols):
        norm = sum(R[i][k] ** 2 for i in range(k, rows)) ** 0.5
        if norm == 0:
            continue
        
        Q[k][k] = R[k][k] / norm
        R[k][k] /= norm
        
        for j in range(k + 1, cols):
            sum_k = sum(Q[i][k] * R[i][j] for i in range(k, rows))
            Q[j][k] = -sum_k / norm
            R[j][k] -= sum_k
        
        for i in range(k + 1, rows):
            sum_k = sum(Q[k][l] * R[i][l] for l in range(k, cols))
            R[i][j] -= sum_k
    
    return Q, R

def rank(matrix):
    Q, R = qr_decomposition(matrix)
    rank = sum(1 for row in R if any(val != 0 for val in row))
    return rank

# Function to generate a random Max-CUT instance
def generate_max_cut_instance(n):
    edges = set()
    while len(edges) < n:
        u, v = random.sample(range(n), 2)
        if (u, v) not in edges and (v, u) not in edges:
            edges.add((u, v))
    return list(edges)

# Function to construct the degree-d pseudoexpectation moment matrix
def construct_moment_matrix(instance, d):
    n = len(instance)
    M = [[0] * (n + 1) for _ in range(n + 1)]
    
    for u, v in instance:
        M[u][v] += 1
        M[v][u] += 1
    
    for i in range(n):
        M[i][i] += n - 2
    
    return M

# Function to run a single trial
def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n = 40
    d = Fraction(878, 1000) * math.log(n)
    if d < 3.5 * math.log(n):
        return {
            "metric_name": "rank",
            "metric_value": -1,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "d is less than 3.5 log n"
        }
    
    instance = generate_max_cut_instance(n)
    M = construct_moment_matrix(instance, d)
    
    rank_M = rank(M)
    
    return {
        "metric_name": "rank",
        "metric_value": rank_M,
        "instances_tested": 1,
        "conjecture_holds": rank_M >= 3.5 * math.log(n),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(2, 6)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(res["metric_value"] for res in results) / len(results)
    std_value = (sum((res["metric_value"] - mean_value) ** 2 for res in results) / len(results)) ** 0.5
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(res["seed"] for res in results if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='d < 3.5 log n' first_failing_seed={first_failing_seed}")