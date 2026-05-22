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
    
    def generate_k_clique(n, k):
        edges = []
        for i in range(k):
            for j in range(i + 1, k):
                edges.append((i, j))
        for _ in range(n - k):
            u = random.randint(0, n - 1)
            v = random.randint(0, n - 1)
            while (u, v) in edges or (v, u) in edges:
                u = random.randint(0, n - 1)
                v = random.randint(0, n - 1)
            edges.append((u, v))
        return edges
    
    def tropicalize(edges):
        n = max(max(u, v) for u, v in edges) + 1
        T = [[-math.inf] * n for _ in range(n)]
        for u, v in edges:
            T[u][v] = 0
            T[v][u] = 0
        return T
    
    def rank(T):
        n = len(T)
        M = [row[:] for row in T]
        pivot_row = 0
        for col in range(n):
            max_row = pivot_row
            for i in range(pivot_row, n):
                if abs(M[i][col]) > abs(M[max_row][col]):
                    max_row = i
            M[pivot_row], M[max_row] = M[max_row], M[pivot_row]
            if M[pivot_row][col] == 0:
                continue
            for i in range(n):
                if i != pivot_row and M[i][col] != 0:
                    factor = -M[i][col] / M[pivot_row][col]
                    for j in range(col, n):
                        M[i][j] += factor * M[pivot_row][j]
            pivot_row += 1
        rank = sum(1 for row in M if any(x != 0 for x in row))
        return rank
    
    def gaussian_elimination(A):
        n = len(A)
        m = len(A[0])
        for i in range(n):
            max_row = i
            for j in range(i + 1, n):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            if A[i][i] == 0:
                return None
            for j in range(m):
                A[i][j] /= A[i][i]
            for j in range(n):
                if j != i and A[j][i] != 0:
                    factor = -A[j][i]
                    for k in range(m):
                        A[j][k] += factor * A[i][k]
        return A
    
    def matrix_multiplication(A, B):
        n = len(A)
        m = len(B[0])
        p = len(B)
        C = [[0] * m for _ in range(n)]
        for i in range(n):
            for j in range(m):
                for k in range(p):
                    C[i][j] += A[i][k] * B[k][j]
        return C
    
    def determinant(A):
        n = len(A)
        if n == 1:
            return A[0][0]
        det = 0
        sign = 1
        for j in range(n):
            submatrix = [row[:j] + row[j+1:] for row in A[1:]]
            det += sign * A[0][j] * determinant(submatrix)
            sign *= -1
        return det
    
    def is_invertible(A):
        return determinant(A) != 0
    
    def find_counterexample(n, k):
        edges = generate_k_clique(n, k)
        T = tropicalize(edges)
        rank_T = rank(T)
        if rank_T < n ** (1/4):
            return "Tropicalized affine scheme has rank less than Θ(n^{1/4})"
        return ""
    
    n = random.randint(5, 40)
    k = random.randint(2, min(n - 1, 10))
    counterexample = find_counterexample(n, k)
    conjecture_holds = len(counterexample) == 0
    metric_value = rank_T if not counterexample else None
    
    return {
        "metric_name": "Minimal Rank of Tropicalized Affine Scheme",
        "metric_value": metric_value,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all("conjecture_holds" in r and r["conjecture_holds"] for r in results):
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any("counterexample" in r and r["counterexample"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if "counterexample" in r and r["counterexample"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE")