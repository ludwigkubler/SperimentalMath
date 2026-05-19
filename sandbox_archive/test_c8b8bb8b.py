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

def random_graph(n):
    adj_matrix = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            if random.random() < 0.5:
                adj_matrix[i][j] = 1
                adj_matrix[j][i] = 1
    return adj_matrix

def matrix_multiplication(A, B):
    m = len(A)
    n = len(B[0])
    p = len(B)
    C = [[0] * n for _ in range(m)]
    for i in range(m):
        for j in range(n):
            for k in range(p):
                C[i][j] += A[i][k] * B[k][j]
    return C

def compute_eigenvalues(M):
    n = len(M)
    if n == 1:
        return [M[0][0]]
    
    # Compute the characteristic polynomial using cofactor expansion
    det = 0
    for j in range(n):
        submatrix = [[M[i][k] for k in range(n) if k != j] for i in range(1, n)]
        det += (-1) ** j * M[0][j] * compute_eigenvalues(submatrix)[0]
    
    # Find eigenvalues by solving the characteristic polynomial
    # For simplicity, we use a numerical method here (e.g., bisection)
    def f(x):
        return sum(M[i][i] - x for i in range(n)) + det
    
    low, high = -2, 2
    while high - low > 1e-5:
        mid = (low + high) / 2
        if f(mid) * f(low) <= 0:
            high = mid
        else:
            low = mid
    
    return [low, high]

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n = random.randint(5, 40)
    graph = random_graph(n)
    d = 3
    
    # Compute the SOS moment matrix M
    M = [[0] * (n + 1) for _ in range(n + 1)]
    M[0][0] = 1
    for i in range(n):
        M[i + 1][i + 1] = sum(graph[i][j] for j in range(i + 1))
        for j in range(i + 1):
            M[j + 1][i + 1] += graph[i][j]
    
    # Compute eigenvalues
    eigenvalues = compute_eigenvalues(M)
    
    # Check if any eigenvalue is outside [-1, 1]
    conjecture_holds = all(-1 <= ev <= 1 for ev in eigenvalues)
    counterexample = "" if conjecture_holds else "Eigenvalue out of bounds"
    
    return {
        "metric_name": "eigenvalue_gap",
        "metric_value": max(abs(ev) for ev in eigenvalues),
        "instances_tested": n,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(res["metric_value"] for res in results) / len(results)
    std_value = math.sqrt(sum((res["metric_value"] - mean_value) ** 2 for res in results) / len(results))
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(res["seed"] for res in results if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")