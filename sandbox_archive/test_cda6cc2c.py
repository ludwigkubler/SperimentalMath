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
    
    def generate_3regular_graph(n):
        while True:
            edges = set()
            for i in range(n):
                neighbors = random.sample(range(n), 2)
                if (i, neighbors[0]) not in edges and (neighbors[0], i) not in edges:
                    edges.add((i, neighbors[0]))
                    edges.add((i, neighbors[1]))
            if len(edges) == n * 3 // 2:
                return edges
    
    def adjacency_matrix(n, edges):
        A = [[0] * n for _ in range(n)]
        for u, v in edges:
            A[u][v] = 1
            A[v][u] = 1
        return A
    
    def eigenvalues(A):
        n = len(A)
        if n == 1:
            return [A[0][0]]
        elif n == 2:
            a, b, c, d = A[0][0], A[0][1], A[1][0], A[1][1]
            det = a * d - b * c
            trace = a + d
            lambda1 = (trace + math.sqrt(trace**2 - 4 * det)) / 2
            lambda2 = (trace - math.sqrt(trace**2 - 4 * det)) / 2
            return [lambda1, lambda2]
        else:
            A[0][0] -= 1
            for i in range(1, n):
                A[i][i-1] -= 1
                A[i-1][i] -= 1
            det = A[0][0]
            for i in range(1, n):
                det *= A[i][i]
            return [det]
    
    def log_disc(G):
        n = len(G)
        lambda_values = eigenvalues(G)
        log_disc = 0
        for i in range(n):
            for j in range(i + 1, n):
                gap = abs(lambda_values[i] - lambda_values[j])
                if gap > 1e-12:
                    log_disc += math.log(gap)
        return log_disc / (n * n)
    
    def max_cut(G):
        n = len(G)
        max_cut_value = 0
        for mask in range(1 << n):
            cut_size = sum((mask >> i) & 1 for i in range(n))
            if cut_size > n // 2:
                continue
            cut_edges = sum((G[i][j] and ((mask >> i) & 1 != (mask >> j) & 1)) for i in range(n) for j in range(i + 1, n))
            max_cut_value = max(max_cut_value, cut_edges)
        return max_cut_value
    
    def sos_slack(G):
        n = len(G)
        lambda_values = eigenvalues(G)
        max_cut_value = max_cut(G)
        edge_count = sum(G[i][j] for i in range(n) for j in range(i + 1, n))
        return (edge_count / 2 - (n / 4) * lambda_values[0] - max_cut_value) / n
    
    def pearson_correlation(X, Y):
        mean_X = sum(X) / len(X)
        mean_Y = sum(Y) / len(Y)
        cov = sum((x - mean_X) * (y - mean_Y) for x, y in zip(X, Y)) / len(X)
        std_X = math.sqrt(sum((x - mean_X)**2 for x in X) / len(X))
        std_Y = math.sqrt(sum((y - mean_Y)**2 for y in Y) / len(Y))
        return cov / (std_X * std_Y)
    
    def linear_regression(X, Y):
        n = len(X)
        sum_x = sum(X)
        sum_y = sum(Y)
        sum_xy = sum(x * y for x, y in zip(X, Y))
        sum_xx = sum(x**2 for x in X)
        a = (n * sum_xy - sum_x * sum_y) / (n * sum_xx - sum_x**2)
        b = (sum_y - a * sum_x) / n
        return a, b
    
    def mean(lst):
        return sum(lst) / len(lst)
    
    def std(lst):
        m = mean(lst)
        return math.sqrt(sum((x - m)**2 for x in lst) / len(lst))
    
    results = []
    for _ in range(30):
        n = random.choice([12, 16, 20])
        G = generate_3regular_graph(n)
        S = sos_slack(G)
        log_disc_value = log_disc(G)
        results.append((S, log_disc_value))
    
    if not results:
        return {
            "metric_name": "SOS Slack vs Log-Discriminant",
            "metric_value": None,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    S_values, log_disc_values = zip(*results)
    rho = pearson_correlation(S_values, log_disc_values)
    a, b = linear_regression(S_values, log_disc_values)
    
    return {
        "metric_name": "SOS Slack vs Log-Discriminant",
        "metric_value": rho,
        "instances_tested": len(results),
        "conjecture_holds": rho >= 0.4 and abs(mean(S_values) - a * mean(log_disc_values) - b) <= 0.05,
        "counterexample": "" if results[0][1] > -1 else f"S={results[0][0]}, LogDisc={results[0][1]}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2**i + 3**j for i in range(5) for j in range(5)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all(result["conjecture_holds"] for result in results):
        mean_rho = mean([result["metric_value"] for result in results])
        std_rho = std([result["metric_value"] for result in results])
        support_fraction = len(results) / len(seeds)
        print(f"RESULT: SUPPORTED mean={mean_rho} std={std_rho} support_fraction={support_fraction}")
    elif any(result["counterexample"] and result["counterexample"].startswith("S=") for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if result["counterexample"])
        print(f"RESULT: FALSIFIED counterexample=\"{next(result['counterexample'] for result in results if result['counterexample'])}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")