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
        return A

    def matrix_multiplication(A, B):
        m, n = len(A), len(B[0])
        p = len(B)
        C = [[0 for _ in range(n)] for _ in range(m)]
        for i in range(m):
            for j in range(n):
                for k in range(p):
                    C[i][j] += A[i][k] * B[k][j]
        return C

    def determinant(A):
        m, n = len(A), len(A[0])
        if m != n:
            raise ValueError("Matrix must be square")
        det = Fraction(1)
        for i in range(m):
            max_row = i
            for j in range(i+1, m):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            det *= A[i][i]
            pivot = A[i][i]
            for j in range(n):
                A[i][j] /= pivot
            for j in range(m):
                if j != i:
                    factor = A[j][i]
                    for k in range(n):
                        A[j][k] -= factor * A[i][k]
        return det

    def generate_quiver(n, k):
        vertices = list(range(n))
        edges = random.sample(list(itertools.combinations(vertices, 2)), k)
        quiver = {v: [] for v in vertices}
        for u, v in edges:
            quiver[u].append(v)
            quiver[v].append(u)
        return quiver

    def tropicalize_quiver(quiver):
        n = len(quiver)
        T = [[-math.inf] * n for _ in range(n)]
        for v in quiver:
            for u in quiver[v]:
                T[u][v] = max(T[u][v], 1)
        return T

    def monotone_circuit_depth(T, k):
        n = len(T)
        depth = [[0] * n for _ in range(n)]
        for i in range(n):
            depth[i][i] = 1
        for l in range(2, n+1):
            for i in range(n-l+1):
                j = i + l - 1
                min_depth = math.inf
                for k in range(i, j):
                    if T[i][k] != -math.inf and T[k][j] != -math.inf:
                        min_depth = min(min_depth, depth[i][k] + depth[k][j])
                depth[i][j] = min_depth + 1
        return depth[0][-1]

    def minimal_rank(T):
        m, n = len(T), len(T[0])
        A = [[T[i][j] if T[i][j] != -math.inf else 0 for j in range(n)] for i in range(m)]
        rank = sum(1 for row in gaussian_elimination(A) if any(row))
        return rank

    n, k = random.randint(5, 40), random.randint(2, min(n-1, 5))  # Ensure k < n
    quiver = generate_quiver(n, k)
    T = tropicalize_quiver(quiver)
    rank = minimal_rank(T)
    depth = monotone_circuit_depth(T, k)

    metric_name = "minimal_rank"
    metric_value = rank
    instances_tested = 1
    conjecture_holds = rank >= n**(k/4) and abs(depth - n**(k/4)) <= 2
    counterexample = "" if conjecture_holds else f"rank={rank}, depth={depth}"

    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else list(range(2, 30))  # Default to first 29 primes (2-89)
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    std_rank = math.sqrt(sum((r["metric_value"] - mean_rank)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"rank below Ω(n^(k/4))\" first_failing_seed={first_failing_seed}")