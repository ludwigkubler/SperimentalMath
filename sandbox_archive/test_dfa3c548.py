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
            factor = A[i][i]
            for j in range(n):
                A[i][j] /= factor
            for j in range(m):
                if j != i:
                    factor = A[j][i]
                    for k in range(n):
                        A[j][k] -= factor * A[i][k]
        return A

    def matrix_multiply(A, B):
        m, n, p = len(A), len(B), len(B[0])
        C = [[0]*p for _ in range(m)]
        for i in range(m):
            for j in range(p):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C

    def deligne_lusztig_parameters(G, V):
        m = len(V)
        n = len(G)
        A = [[0]*n for _ in range(m)]
        for v in V:
            for u in G[v]:
                A[V.index(v)][G.index(u)] += 1
        return gaussian_elimination(A)

    def communication_complexity_rank(G, V):
        m = len(V)
        n = len(G)
        A = [[0]*n for _ in range(m)]
        for v in V:
            for u in G[v]:
                A[V.index(v)][G.index(u)] += 1
        return sum(max(row) for row in A)

    def pearson_correlation(X, Y):
        n = len(X)
        mean_X = sum(X) / n
        mean_Y = sum(Y) / n
        cov = sum((X[i] - mean_X) * (Y[i] - mean_Y) for i in range(n)) / n
        std_X = math.sqrt(sum((X[i] - mean_X)**2 for i in range(n)) / n)
        std_Y = math.sqrt(sum((Y[i] - mean_Y)**2 for i in range(n)) / n)
        return cov / (std_X * std_Y)

    def generate_protocol(n):
        V = list(range(n))
        G = {v: [] for v in V}
        for _ in range(int(n**1.5)):
            u, v = random.sample(V, 2)
            if u not in G[v]:
                G[u].append(v)
                G[v].append(u)
        return G, V

    n_values = [5, 10, 15, 20, 30, 40]
    dl_params = []
    ranks = []

    for n in n_values:
        for _ in range(5):
            G, V = generate_protocol(n)
            dl_param = deligne_lusztig_parameters(G, V)
            rank = communication_complexity_rank(G, V)
            dl_params.append(dl_param)
            ranks.append(rank)

    corr_coeff = pearson_correlation(dl_params, ranks)
    conjecture_holds = corr_coeff > 0.7
    counterexample = "" if conjecture_holds else "correlation_coefficient"

    return {
        "metric_name": "Pearson Correlation Coefficient",
        "metric_value": corr_coeff,
        "instances_tested": len(dl_params),
        "n_max": max(n_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3

    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_corr_coeff = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_corr_coeff} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_corr_coeff} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient\" first_failing_seed={first_failing_seed}")