# auto-injected by SEC sandbox
import itertools
import json
import sys
import os
import time
import re
from itertools import product, combinations, permutations, chain
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from fractions import Fraction
from collections import defaultdict

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_3_regular_graph(n):
        while True:
            edges = set()
            for i in range(n):
                neighbors = random.sample(range(n), 2)
                if neighbors[0] < neighbors[1]:
                    edges.add((neighbors[0], neighbors[1]))
            if len(edges) == (n * 3) // 2:
                return {i: [j for j in range(n) if (i, j) in edges or (j, i) in edges] for i in range(n)}
    
    def eigenvalues(G):
        n = len(G)
        A = [[0] * n for _ in range(n)]
        for u in G:
            for v in G[u]:
                A[u][v] = 1
        D = [sum(A[i]) for i in range(n)]
        Q = [[D[i] - (A[i][j] if j in G[i] else 0) for j in range(n)] for i in range(n)]
        eigenvals = []
        for i in range(n):
            q_i = [Q[i][j] / D[j] for j in range(n)]
            q_i[i] -= 1
            q_i = sorted(q_i)
            lambda_val = math.exp(-sum(math.log(abs(q_i[j])) for j in range(1, n)))
            eigenvals.append(lambda_val)
        return sorted(eigenvals)
    
    def max_cut(G):
        n = len(G)
        best_cut_value = 0
        for i in range(1 << n):
            cut_value = sum(len(G[u]) - sum(1 for v in G[u] if (i >> v) & 1 == 0) for u in range(n))
            best_cut_value = max(best_cut_value, cut_value)
        return best_cut_value
    
    def log_disc(eigenvals):
        n = len(eigenvals)
        log_disc_val = sum(math.log(abs(eigenvals[i] - eigenvals[j])) for i in range(n) for j in range(i + 1, n)) / (n * n)
        return log_disc_val
    
    def pearson_correlation(x, y):
        mean_x = sum(x) / len(x)
        mean_y = sum(y) / len(y)
        cov_xy = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(len(x))) / len(x)
        std_x = math.sqrt(sum((x[i] - mean_x) ** 2 for i in range(len(x))) / len(x))
        std_y = math.sqrt(sum((y[i] - mean_y) ** 2 for i in range(len(y))) / len(y))
        return cov_xy / (std_x * std_y)
    
    def linear_regression(x, y):
        n = len(x)
        mean_x = sum(x) / n
        mean_y = sum(y) / n
        slope = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n)) / sum((x[i] - mean_x) ** 2 for i in range(n))
        intercept = mean_y - slope * mean_x
        return slope, intercept
    
    n_values = [12, 16, 20]
    results = []
    
    for n in n_values:
        G = generate_3_regular_graph(n)
        lambda_values = eigenvalues(G)
        max_cut_val = max_cut(G)
        log_disc_val = log_disc(lambda_values)
        
        if log_disc_val <= -1 and max_cut_val / (n * 4) + log_disc_val > 0.2:
            return {
                "metric_name": "S",
                "metric_value": float('inf'),
                "instances_tested": 1,
                "conjecture_holds": False,
                "counterexample": f"S(G) = {max_cut_val / (n * 4) + log_disc_val}, LogDisc(G) = {log_disc_val}"
            }
        
        results.append({
            "metric_name": "S",
            "metric_value": max_cut_val / (n * 4) + log_disc_val,
            "instances_tested": 1
        })
    
    S_values = [result["metric_value"] for result in results]
    LogDisc_values = [log_disc(eigenvalues(generate_3_regular_graph(n))) for n in n_values]
    
    rho = pearson_correlation(S_values, LogDisc_values)
    slope, intercept = linear_regression(LogDisc_values, S_values)
    
    return {
        "metric_name": "S",
        "metric_value": rho,
        "instances_tested": len(results),
        "conjecture_holds": rho >= 0.4 and all(abs(slope * log_disc_val + intercept - S_val) <= 0.05 for S_val, log_disc_val in zip(S_values, LogDisc_values)),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] if sys.argv[1:] else [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_rho = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_rho} std=0.0 support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"S(G) > 0.2 while LogDisc(G) <= -1\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unreachable")