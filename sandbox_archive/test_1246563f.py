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
    
    def gaussian_elimination(A):
        m, n = len(A), len(A[0])
        for i in range(m):
            max_row = i + max(range(i, m), key=lambda k: abs(A[k][i]))
            A[i], A[max_row] = A[max_row], A[i]
            factor = 1 / A[i][i]
            for j in range(n):
                A[i][j] *= factor
            for k in range(m):
                if k != i:
                    factor = A[k][i]
                    for j in range(n):
                        A[k][j] -= factor * A[i][j]
        return [row[:n-1] for row in A]

    def matrix_mult(A, B):
        m, n, p = len(A), len(B), len(B[0])
        C = [[0] * p for _ in range(m)]
        for i in range(m):
            for j in range(p):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C

    def determinant(A):
        m, n = len(A), len(A[0])
        if m != n:
            raise ValueError("Matrix must be square")
        if m == 1:
            return A[0][0]
        det = 0
        for i in range(n):
            submatrix = [row[:i] + row[i+1:] for row in A[1:]]
            det += (-1) ** i * A[0][i] * determinant(submatrix)
        return det

    def rank(A):
        rref = gaussian_elimination(A)
        return sum(1 for row in rref if any(row))

    def generate_monotone_k_clique(n, k):
        vertices = list(range(n))
        edges = []
        for i in range(n):
            for j in range(i+1, n):
                if random.random() < 0.5:
                    edges.append((i, j))
        return vertices, edges

    def arakelov_geometric_loci(vertices, edges):
        m = len(vertices)
        A = [[0] * (m + 1) for _ in range(m + 1)]
        for i in range(m):
            A[i][i] = 1
        for u, v in edges:
            A[u][v], A[v][u] = 1, 1
        return A

    def minimal_rank(n, k):
        vertices, edges = generate_monotone_k_clique(n, k)
        loci = arakelov_geometric_loci(vertices, edges)
        return rank(loci)

    n_values = [5, 10, 15, 20, 30, 40]
    total_rank = 0
    instances_tested = 0

    for n in n_values:
        for _ in range(5):  # Ensure at least 30 instances per seed
            rank_value = minimal_rank(n, k=3)
            total_rank += rank_value
            instances_tested += 1

    mean_rank = total_rank / instances_tested
    conjecture_holds = mean_rank >= 2 * n**(3/4)  # Using α = 2 for simplicity
    counterexample = "" if conjecture_holds else f"mean_rank={mean_rank}, expected_min={2 * n**(3/4)}"

    return {
        "metric_name": "Minimal Rank",
        "metric_value": mean_rank,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys

    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []

    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, **result}}")
        results.append(result)

    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std=NA support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"First failing seed\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")