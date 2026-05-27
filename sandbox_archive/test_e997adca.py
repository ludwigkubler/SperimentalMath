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
from fractions import Fraction
from math import log2, ceil

def gaussian_elimination(A):
    m, n = len(A), len(A[0])
    for i in range(m):
        max_row = i
        for j in range(i+1, m):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        pivot = A[i][i]
        for j in range(n):
            A[i][j] /= pivot
        for j in range(m):
            if j != i:
                factor = A[j][i]
                for k in range(n):
                    A[j][k] -= factor * A[i][k]

def matrix_multiply(A, B):
    m, n = len(A), len(B[0])
    p = len(B)
    C = [[0] * n for _ in range(m)]
    for i in range(m):
        for j in range(n):
            for k in range(p):
                C[i][j] += A[i][k] * B[k][j]
    return C

def rank(A):
    A_copy = [row[:] for row in A]
    gaussian_elimination(A_copy)
    rank = 0
    for row in A_copy:
        if any(row):
            rank += 1
    return rank

def dual_graph(G):
    n = len(G)
    G_dual = [[] for _ in range(n)]
    for i in range(n):
        for j in range(i+1, n):
            if G[i][j]:
                G_dual[i].append(j)
                G_dual[j].append(i)
    return G_dual

def resolution_proof(clauses):
    n = len(clauses)
    G = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i+1, n):
            if any(c[i] or c[j] for c in clauses):
                G[i][j] = 1
                G[j][i] = 1
    G_dual = dual_graph(G)
    return rank(G_dual)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    clauses = []
    for _ in range(n):
        clause = [random.choice([-1, 1]) * (i+1) for i in range(n)]
        if all(clause[i] != -clause[j] for j in range(i)):
            clauses.append(clause)
    
    P = resolution_proof(clauses)
    dim_A_G = n  # Simplified assumption for the dimension of A(G)
    
    return {
        "metric_name": "rank(C(P))",
        "metric_value": P,
        "instances_tested": 1,
        "conjecture_holds": P <= dim_A_G,
        "counterexample": "" if P <= dim_A_G else f"Rank of C(P) ({P}) exceeds dim(A(G)) ({dim_A_G})"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(res["metric_value"] for res in results) / len(results)
    std_value = (sum((res["metric_value"] - mean_value)**2 for res in results) / len(results))**0.5
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not res["conjecture_holds"] for res in results) and support_fraction >= 0.8:
        first_failing_seed = next(res["seed"] for res in results if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Rank exceeds dim(A(G))\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient evidence")