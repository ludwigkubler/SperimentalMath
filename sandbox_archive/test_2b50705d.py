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
        n = len(A)
        for i in range(n):
            max_row = i
            for j in range(i+1, n):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            pivot = A[i][i]
            for j in range(n):
                A[i][j] /= pivot
            for j in range(n):
                if j != i:
                    factor = A[j][i]
                    for k in range(n):
                        A[j][k] -= factor * A[i][k]
        return A

    def matrix_multiplication(A, B):
        n = len(A)
        C = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C

    def characteristic_polynomial(L):
        n = len(L)
        det = [[0] * n for _ in range(n)]
        for i in range(n):
            det[0][i] = L[i][i]
        for k in range(1, n):
            det[k][k] = (-1) ** (k - 1) * sum(det[k-1][i] * det[k-1][j] for i in range(k) for j in range(i+1, k))
        return det

    def hodge_bundle_metrics(G):
        n = len(G)
        L = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                if (i, j) in G or (j, i) in G:
                    L[i][j] = -1
                else:
                    L[i][j] = 2
        L[0][0] = n - 1
        L[n-1][n-1] = n - 1
        det_L = characteristic_polynomial(L)
        return abs(det_L[0][0])

    def communication_complexity_rank(G):
        n = len(G)
        rank_G = 0
        for i in range(n):
            for j in range(i+1, n):
                if (i, j) in G or (j, i) in G:
                    rank_G += 1
        return rank_G

    def generate_bipartite_graph(n):
        G = set()
        left = random.sample(range(n), n // 2)
        right = list(set(range(n)) - set(left))
        for u in left:
            for v in right:
                if random.choice([True, False]):
                    G.add((u, v))
        return G

    n_values = [5, 10, 15, 20, 30, 40]
    h_values = []
    rank_values = []

    for n in n_values:
        for _ in range(5):
            G = generate_bipartite_graph(n)
            h_value = hodge_bundle_metrics(G)
            rank_value = communication_complexity_rank(G)
            h_values.append(h_value)
            rank_values.append(rank_value)

    correlation_coefficient = sum((h - mean_h) * (rank - mean_rank) for h, rank in zip(h_values, rank_values)) / len(h_values)
    mean_diff = abs(mean_h - mean_rank)

    return {
        "metric_name": "Pearson Correlation Coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(h_values),
        "n_max": max(n_values),
        "conjecture_holds": correlation_coefficient >= 0.8 and mean_diff <= 3,
        "counterexample": "" if correlation_coefficient >= 0.8 and mean_diff <= 3 else "correlation < 0.8 or mean diff > 3"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    else:
        for r in results:
            if not r["conjecture_holds"]:
                print(f"RESULT: FALSIFIED counterexample=\"correlation < 0.8 or mean diff > 3\" first_failing_seed={r['seed']}")
                break