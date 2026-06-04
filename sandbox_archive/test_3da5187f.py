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
    
    def generate_graph(n):
        edges = set()
        for i in range(n):
            for j in range(i + 1, n):
                if random.random() < 0.5:
                    edges.add((i, j))
        return edges
    
    def adjacency_matrix(edges, n):
        adj_matrix = [[0] * n for _ in range(n)]
        for u, v in edges:
            adj_matrix[u][v] = 1
            adj_matrix[v][u] = 1
        return adj_matrix
    
    def minimal_local_indeterminacy(adj_matrix):
        n = len(adj_matrix)
        mli = 0
        for i in range(n):
            row_sum = sum(adj_matrix[i])
            if row_sum > 0:
                mli += 1
        return mli
    
    def communication_complexity_rank(adj_matrix):
        n = len(adj_matrix)
        rank = 0
        for i in range(n):
            for j in range(i + 1, n):
                if adj_matrix[i][j] == 1:
                    rank += 1
        return rank
    
    def polynomial_estimate(mli):
        # Simple polynomial estimate (e.g., mli^2)
        return mli ** 2
    
    def correlation_test(ratios):
        n = len(ratios)
        mean_ratio = sum(ratios) / n
        variance = sum((x - mean_ratio) ** 2 for x in ratios) / n
        std_dev = math.sqrt(variance)
        return mean_ratio, std_dev
    
    def run_test(n):
        edges = generate_graph(n)
        adj_matrix = adjacency_matrix(edges, n)
        mli = minimal_local_indeterminacy(adj_matrix)
        ccr = communication_complexity_rank(adj_matrix)
        polynomial = polynomial_estimate(mli)
        ratio = ccr / polynomial
        return ratio
    
    n_values = [5, 10, 15, 20, 30, 40]
    ratios = []
    
    for n in n_values:
        for _ in range(5):  # Test each size with 5 instances
            ratios.append(run_test(n))
    
    mean_ratio, std_dev = correlation_test(ratios)
    support_fraction = sum(1 for r in ratios if r <= 1.5) / len(ratios)
    
    conjecture_holds = support_fraction >= 0.9 and p_value < 0.05
    counterexample = "" if conjecture_holds else "support_fraction<0.9 or p_value>=0.05"
    
    return {
        "metric_name": "Ratio of ccr to polynomial estimate",
        "metric_value": mean_ratio,
        "instances_tested": len(ratios),
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
    
    mean_ratio = sum(r["metric_value"] for r in results) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean_ratio) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std={std_dev} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"support_fraction<0.9 or p_value>=0.05\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE support_fraction<0.8")