# auto-injected by SEC sandbox
import math
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
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_bipartite_graph(n):
        A = [random.randint(0, 1) for _ in range(n)]
        B = [random.randint(0, 1) for _ in range(n)]
        G = [[A[i] == B[j] for j in range(n)] for i in range(n)]
        return G
    
    def matroid_representation(G):
        n = len(G)
        M = set()
        for i in range(n):
            for j in range(i+1, n):
                if all(G[i][k] == G[j][k] for k in range(n)):
                    M.add((i, j))
        return M
    
    def communication_complexity_rank_variance(G):
        n = len(G)
        ranks = [sum(row) for row in G]
        mean_rank = sum(ranks) / n
        variance = sum((r - mean_rank) ** 2 for r in ranks) / n
        return variance
    
    def pearson_correlation_coefficient(x, y):
        n = len(x)
        mean_x = sum(x) / n
        mean_y = sum(y) / n
        cov_xy = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n))
        std_x = (sum((x[i] - mean_x) ** 2 for i in range(n)) / n) ** 0.5
        std_y = (sum((y[i] - mean_y) ** 2 for i in range(n)) / n) ** 0.5
        return cov_xy / (std_x * std_y)
    
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):
            G = generate_bipartite_graph(n)
            M = matroid_representation(G)
            r_var = communication_complexity_rank_variance(G)
            results.append((n, len(M), r_var))
    
    if not results:
        return {
            "metric_name": "Pearson correlation coefficient",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "No valid graphs generated"
        }
    
    n_values = [r[0] for r in results]
    M_values = [r[1] for r in results]
    r_var_values = [r[2] for r in results]
    
    correlation_coefficient = pearson_correlation_coefficient(M_values, r_var_values)
    
    return {
        "metric_name": "Pearson correlation coefficient",
        "metric_value": abs(correlation_coefficient),
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": abs(correlation_coefficient) >= 0.8,
        "counterexample": "" if abs(correlation_coefficient) >= 0.8 else f"Correlation coefficient: {correlation_coefficient}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 1000003) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all(r["conjecture_holds"] for r in results):
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        std_value = (sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results)) ** 0.5
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] and abs(r["metric_value"]) < 0.6 for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"] and abs(result["metric_value"]) < 0.6)
        print(f"RESULT: FALSIFIED counterexample=\"Correlation coefficient too low\" first_failing_seed={first_failing_seed}")
    else:
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction}")