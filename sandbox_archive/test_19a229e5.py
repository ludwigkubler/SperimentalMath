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
        return [row[:n-1] for row in A]

    def matrix_multiply(A, B):
        m, n, p = len(A), len(B[0]), len(B)
        C = [[0] * n for _ in range(m)]
        for i in range(m):
            for j in range(n):
                for k in range(p):
                    C[i][j] += A[i][k] * B[k][j]
        return C

    def laplacian_eigenvalues(n, adj):
        D = [[0] * n for _ in range(n)]
        for i in range(n):
            degree = sum(adj[i])
            D[i][i] = degree
        L = matrix_multiply(D, adj)
        L = matrix_multiply(L, adj)
        eigenvalues = gaussian_elimination(L)
        return sorted(eigenvalues, reverse=True)

    def max_cut(G):
        n = len(G)
        best_cut_value = 0
        for i in range(1 << (n-1)):
            cut_value = 0
            for j in range(n):
                for k in range(j+1, n):
                    if (i >> j) & 1 and (i >> k) & 1:
                        cut_value += G[j][k]
                    elif not ((i >> j) & 1) and not ((i >> k) & 1):
                        cut_value += G[j][k]
            best_cut_value = max(best_cut_value, cut_value)
        return best_cut_value

    def hankel_rank(n, adj):
        H = [[0] * (2*n+1) for _ in range(2*n+1)]
        for i in range(2*n+1):
            for j in range(i+1):
                if 0 <= i-j < n:
                    H[i][j] = sum(adj[k][(i-k+j)%n] for k in range(n))
                else:
                    H[i][j] = 0
        H = gaussian_elimination(H)
        rank = sum(1 for row in H if any(row))
        return rank

    n_values = [8, 10, 12, 14, 16]
    k_values = [3, 4]
    results = []

    for n in n_values:
        for k in k_values:
            G = [[0] * n for _ in range(n)]
            degree_sum = 0
            while True:
                edges = random.sample(range(n), k)
                for u, v in zip(edges, edges[1:] + [edges[0]]):
                    if G[u][v] == 0:
                        G[u][v] = G[v][u] = 1
                        degree_sum += 2
                if degree_sum == n * k and len(set(sum(row) for row in G)) == 1:
                    break

            eigenvalues = laplacian_eigenvalues(n, G)
            hankel_rank_value = hankel_rank(n, G)
            max_cut_value = max_cut(G)
            rho = n * max(eigenvalues[0]) / (4 * max_cut_value) - 1
            r = n * rho / (hankel_rank_value * math.log2(n+1))
            results.append(r)

    mean_r = sum(results) / len(results)
    max_r = max(results)
    conjecture_holds = max_r < 2 and mean_r <= 0.75
    counterexample = "" if conjecture_holds else f"max r={max_r:.4f} > 2"

    return {
        "metric_name": "r",
        "metric_value": mean_r,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []

    for seed in seeds:
        trial = run_trial(seed)
        print(f"TRIAL: {trial}")

        if "conjecture_holds" in trial and not trial["conjecture_holds"]:
            break

    mean_r = sum(trial["metric_value"] for trial in results) / len(results)
    max_r = max(trial["metric_value"] for trial in results)
    support_fraction = sum(1 for trial in results if trial["conjecture_holds"]) / len(results)

    if all(trial["conjecture_holds"] for trial in results):
        print(f"RESULT: SUPPORTED mean={mean_r:.4f} std=0.0000 support_fraction={support_fraction:.2%}")
    elif max_r >= 2:
        first_failing_seed = next(seed for seed, trial in enumerate(results) if not trial["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='max r={max_r:.4f} > 2' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")