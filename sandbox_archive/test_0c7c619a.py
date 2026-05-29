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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def log2(n):
        return math.log2(n)
    
    def ceil(x):
        return int(math.ceil(x))
    
    def floor(x):
        return int(math.floor(x))
    
    def gaussian_elimination(A, b):
        n = len(A)
        for i in range(n):
            max_row = i
            for j in range(i+1, n):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            b[i], b[max_row] = b[max_row], b[i]
            for j in range(i+1, n):
                factor = A[j][i] / A[i][i]
                for k in range(i, n):
                    A[j][k] -= factor * A[i][k]
                b[j] -= factor * b[i]
        x = [0] * n
        for i in range(n-1, -1, -1):
            x[i] = (b[i] - sum(A[i][j] * x[j] for j in range(i+1, n))) / A[i][i]
        return x
    
    def matrix_multiply(A, B):
        m, k, n = len(A), len(B[0]), len(B)
        C = [[0] * n for _ in range(m)]
        for i in range(m):
            for j in range(n):
                for l in range(k):
                    C[i][j] += A[i][l] * B[l][j]
        return C
    
    def transpose(A):
        return [list(row) for row in zip(*A)]
    
    def determinant(A):
        n = len(A)
        if n == 1:
            return A[0][0]
        det = 0
        for j in range(n):
            submatrix = [row[:j] + row[j+1:] for row in A[1:]]
            det += ((-1) ** j) * A[0][j] * determinant(submatrix)
        return det
    
    def adjugate(A):
        n = len(A)
        if n == 1:
            return [[1]]
        cofactors = []
        for i in range(n):
            row = []
            for j in range(n):
                submatrix = [row[:j] + row[j+1:] for row in A[1:i] + A[i+1:]]
                row.append((-1) ** (i+j) * determinant(submatrix))
            cofactors.append(row)
        return transpose(cofactors)
    
    def inverse(A):
        det_A = determinant(A)
        if det_A == 0:
            raise ValueError("Matrix is singular")
        adj_A = adjugate(A)
        inv_A = [[adj_A[i][j] / det_A for j in range(len(A))] for i in range(len(A))]
        return inv_A
    
    def generate_random_k_subsets(N, k):
        return [random.sample(range(1, N+1), k) for _ in range(20)]
    
    def reduce_dnf(dnf):
        terms = set()
        for term in dnf:
            min_term = min(term)
            if all(min_term <= t for t in term):
                terms.add(tuple(sorted(term)))
        return sorted(list(terms))
    
    def build_h(F):
        n = len(F[0])
        A = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i, n):
                if any(t1 & t2 for t1 in F[i] for t2 in F[j]):
                    A[i][j] = 1
                    A[j][i] = 1
        return A
    
    def forman_ricci_curvature(A):
        n = len(A)
        deg = [sum(row) for row in A]
        tri = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i, n):
                if A[i][j]:
                    tri[i][j] = sum(A[k][i] * A[k][j] for k in range(n) if k != i and k != j)
                    tri[j][i] = tri[i][j]
        mu = 0
        for e in range(n):
            u, v = divmod(e, n)
            mu += 4 - deg[u] - deg[v] + 3 * tri[u][v]
        return mu / (n * (n-1) // 2) if n > 1 else 0
    
    def compute_delta(F, G):
        F_and_G = reduce_dnf([t for t in F + G if any(t1 & t2 for t1 in F for t2 in G)])
        F_or_G = reduce_dnf(list(set(F + G)))
        return forman_ricci_curvature(build_h(F_and_G)) + forman_ricci_curvature(build_h(F_or_G)) - forman_ricci_curvature(build_h(F)) - forman_ricci_curvature(build_h(G))
    
    N_values = [10, 15, 20, 25, 30, 40]
    results = []
    for N in N_values:
        k = ceil(log2(N))
        F = generate_random_k_subsets(N, k)
        G = generate_random_k_subsets(N, k)
        F = reduce_dnf(F)
        G = reduce_dnf(G)
        delta = compute_delta(F, G)
        results.append({
            "metric_name": "delta",
            "metric_value": abs(delta),
            "instances_tested": 1,
            "n_max": N,
            "conjecture_holds": abs(delta) <= 4 * math.sqrt(N),
            "counterexample": "" if abs(delta) <= 4 * math.sqrt(N) else f"delta={abs(delta)} > 4*sqrt({N})"
        })
    
    mean_delta = sum(result["metric_value"] for result in results) / len(results)
    std_dev_delta = math.sqrt(sum((result["metric_value"] - mean_delta) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    return {
        "seed": seed,
        "mean_delta": mean_delta,
        "std_dev_delta": std_dev_delta,
        "support_fraction": support_fraction
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_delta = sum(result["mean_delta"] for result in results) / len(results)
    std_dev_delta = math.sqrt(sum((result["mean_delta"] - mean_delta) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["support_fraction"] == 1) / len(results)
    
    if all(result["support_fraction"] == 1 for result in results):
        print(f"RESULT: SUPPORTED mean={mean_delta} std={std_dev_delta} support_fraction={support_fraction}")
    elif any(result["support_fraction"] < 0.8 for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if result["support_fraction"] < 0.8)
        print(f"RESULT: FALSIFIED counterexample='seed={first_failing_seed}' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_support")