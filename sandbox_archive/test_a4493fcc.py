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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_max_cut_instance(n):
        edges = []
        for i in range(n):
            for j in range(i + 1, n):
                if random.random() < 0.5:
                    edges.append((i, j))
        return edges
    
    def degree_2_moment_matrix(edges, n):
        M = [[0] * n for _ in range(n)]
        for u, v in edges:
            M[u][v] += 1
            M[v][u] += 1
        return M
    
    def is_positive_semidefinite(M):
        n = len(M)
        for i in range(n):
            if not is_positive_definite(submatrix(M, i)):
                return False
        return True
    
    def submatrix(M, i):
        return [row[:i] + row[i+1:] for row in M[:i] + M[i+1:]]
    
    def is_positive_definite(M):
        n = len(M)
        for k in range(1, n + 1):
            A_k = submatrix(M, k - 1)
            if not is_positive_definite(A_k):
                return False
        return True
    
    def eigenvalues(M):
        n = len(M)
        if n == 1:
            return [M[0][0]]
        if n == 2:
            a, b, c = M[0][0], M[0][1], M[1][1]
            det = a * c - b * b
            trace = a + c
            lambda1 = (trace + math.sqrt(trace**2 - 4 * det)) / 2
            lambda2 = (trace - math.sqrt(trace**2 - 4 * det)) / 2
            return [lambda1, lambda2]
        else:
            for i in range(n):
                A_i = submatrix(M, i)
                if not is_positive_definite(A_i):
                    continue
                lambda_i = M[i][i] - sum(M[i][j] * M[j][i] / M[j][j] for j in range(i) if j != i)
                return eigenvalues([[M[i][i]]])
    
    def is_real_stable(P):
        n = len(P)
        for k in range(1, n + 1):
            A_k = submatrix(P, k - 1)
            if not is_positive_definite(A_k):
                continue
            lambda_i = P[k - 1][k - 1] - sum(P[k - 1][j] * P[j][k - 1] / P[j][j] for j in range(k - 1) if j != k - 1)
            return is_real_stable([[P[i][i]]])
        return all(lambda_i >= 0 for lambda_i in eigenvalues(P))
    
    def sos_refutation_threshold(M):
        n = len(M)
        A = [[M[i][j] + M[j][i] for j in range(n)] for i in range(n)]
        b = [1 if i == 0 else 0 for i in range(n)]
        x = gaussian_elimination(A, b)
        return sum(x[i] * x[i] for i in range(n))
    
    def gaussian_elimination(A, b):
        n = len(A)
        M = [[A[i][j] for j in range(n)] + [b[i]] for i in range(n)]
        for i in range(n):
            max_row = i
            for j in range(i + 1, n):
                if abs(M[j][i]) > abs(M[max_row][i]):
                    max_row = j
            M[i], M[max_row] = M[max_row], M[i]
            denom = M[i][i]
            for j in range(i, n + 1):
                M[i][j] /= denom
            for j in range(n):
                if j != i:
                    factor = M[j][i]
                    for k in range(i, n + 1):
                        M[j][k] -= factor * M[i][k]
        x = [0] * n
        for i in range(n - 1, -1, -1):
            x[i] = M[i][-1]
            for j in range(i + 1, n):
                x[i] -= M[i][j] * x[j]
        return x
    
    def degree_d_minor(M, d):
        n = len(M)
        if d == 0:
            return True
        if d == 1:
            return any(all(M[i][j] >= 0 for j in range(n)) for i in range(n))
        minors = []
        for i in range(n):
            for j in range(i + 1, n):
                minor = submatrix(M, i)
                minor = [row[:j] + row[j+1:] for row in minor]
                minors.append(minor)
        return any(degree_d_minor(minor, d - 1) for minor in minors)
    
    def degree_2_sdp_relaxation(M):
        n = len(M)
        A = [[M[i][j] + M[j][i] for j in range(n)] for i in range(n)]
        b = [1 if i == 0 else 0 for i in range(n)]
        x = gaussian_elimination(A, b)
        return sum(x[i] * x[i] for i in range(n))
    
    n = random.randint(5, 40)
    edges = generate_max_cut_instance(n)
    M = degree_2_moment_matrix(edges, n)
    
    if not is_positive_semidefinite(M):
        return {
            "metric_name": "sos_refutation_threshold",
            "metric_value": float('inf'),
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "Non-positive semidefinite moment matrix"
        }
    
    d = 0
    while degree_d_minor(M, d):
        d += 1
    
    threshold = sos_refutation_threshold(M)
    if threshold < d * math.log(n):
        return {
            "metric_name": "sos_refutation_threshold",
            "metric_value": threshold,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": f"SOS refutation threshold {threshold} is less than Ω({d} log {n})"
        }
    
    return {
        "metric_name": "sos_refutation_threshold",
        "metric_value": threshold,
        "instances_tested": 1,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [random.getrandbits(32) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='SOS refutation threshold less than Ω(d log n)' first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_evidence")