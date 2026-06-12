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
            for j in range(i + 1, m):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            for j in range(i + 1, m):
                factor = A[j][i] / A[i][i]
                for k in range(n):
                    A[j][k] -= factor * A[i][k]
        return A

    def matrix_multiplication(A, B):
        m, n, p = len(A), len(B), len(B[0])
        C = [[0] * p for _ in range(m)]
        for i in range(m):
            for j in range(p):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C

    def laplacian_matrix(G):
        n = len(G)
        L = [[0] * n for _ in range(n)]
        for i in range(n):
            degree = sum(G[i])
            L[i][i] = -degree
            for j in range(i + 1, n):
                if G[i][j]:
                    L[i][j] = L[j][i] = 1
        return L

    def characteristic_polynomial(L):
        n = len(L)
        det = [[0] * (n + 1) for _ in range(n + 1)]
        for i in range(n):
            for j in range(n):
                det[i + 1][j + 1] = L[i][j]
        for k in range(1, n + 2):
            det[0][k] = (-1) ** (k - 1) * sum(det[k][i] for i in range(k))
        return det

    def hodge_bundle_metrics(G):
        L = laplacian_matrix(G)
        det_L = characteristic_polynomial(L)
        h = abs(det_L[0][-1])
        return h

    def communication_complexity_rank(G):
        n = len(G)
        rank = 0
        for i in range(n // 2):
            row_sum = sum(G[i][j] + G[j][i] for j in range(i, n))
            if row_sum > rank:
                rank = row_sum
        return rank

    def generate_bipartite_graph(n):
        G = [[0] * n for _ in range(n)]
        for i in range(n // 2):
            for j in range(n // 2, n):
                if random.choice([True, False]):
                    G[i][j] = G[j][i] = 1
        return G

    def pearson_correlation(X, Y):
        mean_X = sum(X) / len(X)
        mean_Y = sum(Y) / len(Y)
        cov = sum((X[i] - mean_X) * (Y[i] - mean_Y) for i in range(len(X))) / len(X)
        std_X = math.sqrt(sum((X[i] - mean_X) ** 2 for i in range(len(X))) / len(X))
        std_Y = math.sqrt(sum((Y[i] - mean_Y) ** 2 for i in range(len(Y))) / len(Y))
        return cov / (std_X * std_Y)

    n_values = [5, 10, 15, 20, 30, 40]
    h_values = []
    rank_values = []

    for n in n_values:
        G = generate_bipartite_graph(n)
        h_values.append(hodge_bundle_metrics(G))
        rank_values.append(communication_complexity_rank(G))

    correlation_coefficient = pearson_correlation(h_values, rank_values)
    mean_difference = abs(sum(h_values) - sum(rank_values)) / len(h_values)

    return {
        "metric_name": "Pearson Correlation Coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": 6,
        "n_max": max(n_values),
        "conjecture_holds": correlation_coefficient >= 0.8 and mean_difference <= 3,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []

    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and any(r["metric_value"] >= 0.8 and abs(sum(h_values) - sum(rank_values)) / len(h_values) <= 3 for r in results):
        print(f"RESULT: FALSIFIED counterexample=\"correlation_threshold_not_met\" first_failing_seed={seeds[results.index(next((r for r in results if not r['conjecture_holds']), None))]}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data_or_unexpected_behavior")