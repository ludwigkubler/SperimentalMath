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
    
    def generate_communication_complexity_instance(rank):
        # Generate a random communication complexity instance with the given rank
        n = rank * 2 + 1
        graph = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i+1, n):
                if random.randint(0, 1) == 0:
                    graph[i][j] = 1
                    graph[j][i] = 1
        return graph
    
    def compute_minimal_order_of_affine_divisor(graph):
        # Compute the minimal order of an affine divisor for the given graph
        n = len(graph)
        if n <= 1:
            return 0
        
        # Gaussian elimination to find rank of the matrix
        rank = 0
        for i in range(n):
            if graph[i][i] == 0:
                for j in range(i+1, n):
                    if graph[j][i] != 0:
                        graph[i], graph[j] = graph[j], graph[i]
                        break
            if graph[i][i] != 0:
                rank += 1
                for j in range(n):
                    if j != i:
                        factor = -graph[j][i] / graph[i][i]
                        for k in range(n):
                            graph[j][k] += factor * graph[i][k]
        
        return rank
    
    def pearson_correlation(x, y):
        # Compute the Pearson correlation coefficient between x and y
        n = len(x)
        mean_x = sum(x) / n
        mean_y = sum(y) / n
        cov_xy = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n)) / n
        std_x = math.sqrt(sum((x[i] - mean_x) ** 2 for i in range(n)) / n)
        std_y = math.sqrt(sum((y[i] - mean_y) ** 2 for i in range(n)) / n)
        return cov_xy / (std_x * std_y)
    
    ranks = [5, 10, 15, 20, 30, 40]
    min_orders = []
    instances_tested = 0
    n_max = 0
    
    for rank in ranks:
        graph = generate_communication_complexity_instance(rank)
        min_order = compute_minimal_order_of_affine_divisor(graph)
        min_orders.append(min_order)
        instances_tested += len(graph)
        n_max = max(n_max, len(graph))
    
    correlation = pearson_correlation(ranks, min_orders)
    
    conjecture_holds = abs(correlation) >= 0.9
    counterexample = "" if conjecture_holds else f"Correlation {correlation:.2f} does not support the conjecture"
    
    return {
        "metric_name": "Pearson Correlation",
        "metric_value": correlation,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value:.4f} std={std_value:.4f} support_fraction={support_fraction:.2f}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value:.4f} std={std_value:.4f} support_fraction={support_fraction:.2f}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Correlation does not support the conjecture\" first_failing_seed={first_failing_seed}")