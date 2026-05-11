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

def generate_disjointness_instance(n):
    A = [random.randint(0, 1) for _ in range(n)]
    B = [random.randint(0, 1) for _ in range(n)]
    return A, B

def matrix_multiplication(A, B):
    m, k = len(A), len(B[0])
    n = len(B)
    C = [[0] * k for _ in range(m)]
    for i in range(m):
        for j in range(k):
            for l in range(n):
                C[i][j] += A[i][l] * B[l][j]
    return C

def transpose(A):
    m, n = len(A), len(A[0])
    B = [[0] * m for _ in range(n)]
    for i in range(m):
        for j in range(n):
            B[j][i] = A[i][j]
    return B

def singular_value_decomposition(A):
    U, S, Vt = [], [], []
    if len(A) == len(A[0]):
        n = len(A)
        Q, R = gram_schmidt(A)
        for i in range(n):
            s = sum(R[i][j] ** 2 for j in range(i, n)) ** 0.5
            S.append(s)
            Vt.append([R[i][j] / s if j == k else 0 for j in range(n) for k in range(n)])
        U = transpose(Q)
    return U, S, Vt

def gram_schmidt(A):
    m, n = len(A), len(A[0])
    Q, R = [], []
    for i in range(n):
        v = [A[j][i] for j in range(m)]
        for j in range(i):
            u = Q[j]
            r = sum(u[k] * v[k] for k in range(m))
            v = [v[k] - r * u[k] for k in range(m)]
        s = sum(v[k] ** 2 for k in range(m)) ** 0.5
        Q.append([v[k] / s for k in range(m)])
        R.append([sum(Q[j][k] * A[l][k] for j in range(i + 1)) if j == i else 0 for k in range(n)])
    return Q, R

def schatten_p_norm(S, p):
    if p == float('inf'):
        return max(S)
    elif p == 2:
        return sum(s ** 2 for s in S) ** 0.5
    else:
        return (sum(s ** p for s in S)) ** (1 / p)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        instances_tested = 30
        total_norm = 0
        
        for _ in range(instances_tested):
            A, B = generate_disjointness_instance(n)
            communication_matrix = [[A[i] ^ B[j] for j in range(n)] for i in range(n)]
            U, S, Vt = singular_value_decomposition(communication_matrix)
            norm = schatten_p_norm(S, 2)  # Using p=2 for simplicity
            total_norm += norm
        
        average_norm = total_norm / instances_tested
        results.append({
            "n": n,
            "average_norm": average_norm
        })
    
    metric_name = "Schatten_2-Norm"
    metric_value = sum(result["average_norm"] * len(n_values) for result in results)
    conjecture_holds = all(result["average_norm"] >= n for result in results)
    counterexample = "" if conjecture_holds else f"Disjointness problem not scaling linearly with n"
    
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested * len(n_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i + 17 for i in range(5, 35)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = (sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results)) ** 0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Disjointness problem not scaling linearly with n\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient evidence")