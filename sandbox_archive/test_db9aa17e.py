# auto-injected by SEC sandbox
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from fractions import Fraction
import itertools

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_random_3_regular_graph(n):
        while True:
            edges = set()
            for i in range(n):
                neighbors = random.sample(range(n), 2)
                if (i, neighbors[0]) not in edges and (neighbors[0], i) not in edges:
                    edges.add((i, neighbors[0]))
                    edges.add((i, neighbors[1]))
            if len(edges) == n * 3 // 2:
                return [list(v) for v in itertools.groupby(sorted(edges), key=lambda x: x[0])]

    def eigenvalues(G):
        n = len(G)
        A = [[0] * n for _ in range(n)]
        for u, v in G:
            A[u][v] = 1
            A[v][u] = 1
        lambda_values = []
        for i in range(n):
            A[0][i] -= 1
            det_A = determinant(A)
            lambda_values.append(det_A)
            A[0][i] += 1
        return sorted(lambda_values)

    def determinant(matrix):
        n = len(matrix)
        if n == 1:
            return matrix[0][0]
        det = 0
        for j in range(n):
            submatrix = [row[:j] + row[j+1:] for row in matrix[1:]]
            det += (-1) ** j * matrix[0][j] * determinant(submatrix)
        return det

    def max_cut(G):
        n = len(G)
        best_cut_size = 0
        for partition in itertools.product([0, 1], repeat=n):
            cut_size = sum(1 for i in range(n) if partition[i] != partition[G[i].index(i)])
            best_cut_size = max(best_cut_size, cut_size)
        return best_cut_size

    def log_disc(G):
        lambda_values = eigenvalues(G)
        n = len(lambda_values)
        log_disc = 0
        for i in range(n):
            for j in range(i + 1, n):
                gap = abs(lambda_values[i] - lambda_values[j])
                if gap > 1e-12:
                    log_disc += math.log(gap)
        return log_disc / (n ** 2)

    def sos_slack(G):
        n = len(G)
        lambda_values = eigenvalues(G)
        max_cut_value = max_cut(G)
        edge_count = n * 3 // 2
        slack = (edge_count - (n / 4) * lambda_values[0] - max_cut_value) / n
        return slack

    def pearson_correlation(X, Y):
        mean_X = sum(X) / len(X)
        mean_Y = sum(Y) / len(Y)
        cov = sum((x - mean_X) * (y - mean_Y) for x, y in zip(X, Y)) / len(X)
        std_X = math.sqrt(sum((x - mean_X) ** 2 for x in X) / len(X))
        std_Y = math.sqrt(sum((y - mean_Y) ** 2 for y in Y) / len(Y))
        return cov / (std_X * std_Y)

    def linear_regression(X, Y):
        n = len(X)
        sum_x = sum(X)
        sum_y = sum(Y)
        sum_xy = sum(x * y for x, y in zip(X, Y))
        sum_xx = sum(x ** 2 for x in X)
        a = (n * sum_xy - sum_x * sum_y) / (n * sum_xx - sum_x ** 2)
        b = (sum_y - a * sum_x) / n
        return a, b

    def ols_residuals(X, Y):
        a, b = linear_regression(X, Y)
        return [y - (a * x + b) for x, y in zip(X, Y)]

    n_values = [12, 16, 20]
    results = []
    for n in n_values:
        G = generate_random_3_regular_graph(n)
        log_disc_values = []
        slack_values = []
        for _ in range(30):
            lambda_values = eigenvalues(G)
            log_disc_value = log_disc(G)
            slack_value = sos_slack(G)
            log_disc_values.append(log_disc_value)
            slack_values.append(slack_value)
        rho = pearson_correlation(log_disc_values, slack_values)
        a, b = linear_regression(log_disc_values, slack_values)
        residuals = ols_residuals(log_disc_values, slack_values)
        mean_residual = sum(residuals) / len(residuals)
        results.append({
            "n": n,
            "rho": rho,
            "a": a,
            "b": b,
            "mean_residual": mean_residual
        })

    metric_value = sum(rho for r in results) / len(results)
    instances_tested = 30 * len(n_values)
    conjecture_holds = all(r["rho"] >= 0.4 and abs(r["a"]) < 5 and abs(r["b"]) <= 0.05 for r in results)
    counterexample = "" if conjecture_holds else "mapping_undefined"

    return {
        "metric_name": "Pearson Correlation",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")

# RESULT: INCONCLUSIVE reason=mapping_undefined n_tested=30