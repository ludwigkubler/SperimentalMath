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
                return [set() for _ in range(n)], list(edges)
    
    def adjacency_matrix_to_eigenvalues(A):
        n = len(A)
        eigenvalues = []
        for i in range(100):  # Max 100 iterations to avoid infinite loop
            v = [random.gauss(0, 1) for _ in range(n)]
            v /= math.sqrt(sum(x * x for x in v))
            Av = [sum(A[i][j] * v[j] for j in range(n)) for i in range(n)]
            lambda_i = sum(v[i] * Av[i] for i in range(n)) / sum(v[i] * v[i] for i in range(n))
            eigenvalues.append(lambda_i)
        return sorted(eigenvalues)
    
    def max_cut(G):
        n = len(G)
        best_cut_size = 0
        for mask in range(1 << n):
            cut_size = sum((mask >> i) & 1 for i in range(n))
            if cut_size > best_cut_size:
                left = [i for i in range(n) if (mask >> i) & 1]
                right = [i for i in range(n) if not (mask >> i) & 1]
                cut_size = sum(1 for u, v in G if ((u in left and v in right) or (v in left and u in right)))
                best_cut_size = cut_size
        return best_cut_size
    
    def log_disc(eigenvalues):
        n = len(eigenvalues)
        total = 0
        for i in range(n):
            for j in range(i + 1, n):
                gap = abs(eigenvalues[i] - eigenvalues[j])
                if gap > 1e-12:
                    total += math.log(gap)
        return total / (n * n)
    
    def ols_regression(x, y):
        n = len(x)
        sum_x = sum(x)
        sum_y = sum(y)
        sum_xy = sum(xi * yi for xi, yi in zip(x, y))
        sum_xx = sum(xi * xi for xi in x)
        a = (n * sum_xy - sum_x * sum_y) / (n * sum_xx - sum_x ** 2)
        b = (sum_y - a * sum_x) / n
        return a, b
    
    def pearson_correlation(x, y):
        n = len(x)
        mean_x = sum(x) / n
        mean_y = sum(y) / n
        cov_xy = sum((xi - mean_x) * (yi - mean_y) for xi, yi in zip(x, y)) / n
        std_x = math.sqrt(sum((xi - mean_x) ** 2 for xi in x) / n)
        std_y = math.sqrt(sum((yi - mean_y) ** 2 for yi in y) / n)
        return cov_xy / (std_x * std_y)
    
    n_values = [12, 16, 20]
    results = []
    
    for n in n_values:
        G, edges = generate_3regular_graph(n)
        A = [[0] * n for _ in range(n)]
        for u, v in edges:
            A[u][v] = A[v][u] = 1
        
        eigenvalues = adjacency_matrix_to_eigenvalues(A)
        max_cut_value = max_cut(G)
        log_disc_value = log_disc(eigenvalues)
        
        results.append({
            "n": n,
            "log_disc": log_disc_value,
            "max_cut": max_cut_value,
            "sos_slack": (len(edges) / 2 - (n / 4) * eigenvalues[0] - max_cut_value) / n
        })
    
    if any(result["sos_slack"] > 0.2 and result["log_disc"] <= -1 for result in results):
        return {
            "metric_name": "SOS Slack vs Log-Discriminant",
            "metric_value": None,
            "instances_tested": len(results),
            "conjecture_holds": False,
            "counterexample": "Found instance with SOS Slack > 0.2 and Log-Discriminant <= -1"
        }
    
    log_disc_values = [result["log_disc"] for result in results]
    sos_slack_values = [result["sos_slack"] for result in results]
    
    rho = pearson_correlation(log_disc_values, sos_slack_values)
    a, b = ols_regression(log_disc_values, sos_slack_values)
    
    return {
        "metric_name": "SOS Slack vs Log-Discriminant",
        "metric_value": rho,
        "instances_tested": len(results),
        "conjecture_holds": rho >= 0.4 and abs(a * Fraction(12) + b - Fraction(12, 1)) <= 0.05 and abs(a * Fraction(16) + b - Fraction(16, 1)) <= 0.05 and abs(a * Fraction(20) + b - Fraction(20, 1)) <= 0.05,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(2, 33)]
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
    
    log_disc_values = [run_trial(seed)["log_disc"] for seed in seeds]
    sos_slack_values = [run_trial(seed)["sos_slack"] for seed in seeds]
    
    rho = pearson_correlation(log_disc_values, sos_slack_values)
    a, b = ols_regression(log_disc_values, sos_slack_values)
    
    support_fraction = sum(1 for seed in seeds if run_trial(seed)["conjecture_holds"]) / len(seeds)
    
    if all(run_trial(seed)["conjecture_holds"] for seed in seeds):
        print(f"RESULT: SUPPORTED mean={rho} std={math.sqrt(sum((x - rho) ** 2 for x in log_disc_values) / len(log_disc_values))} support_fraction={support_fraction}")
    elif any(result["sos_slack"] > 0.2 and result["log_disc"] <= -1 for result in (run_trial(seed) for seed in seeds)):
        print(f"RESULT: FALSIFIED counterexample='Found instance with SOS Slack > 0.2 and Log-Discriminant <= -1' first_failing_seed={seeds[next(i for i, r in enumerate((run_trial(seed) for seed in seeds)) if r['sos_slack'] > 0.2 and r['log_disc'] <= -1)]}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_evidence support_fraction={support_fraction}")