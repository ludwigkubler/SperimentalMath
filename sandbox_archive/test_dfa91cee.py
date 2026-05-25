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
    
    def generate_random_graph(n):
        edges = set()
        for i in range(n):
            for j in range(i + 1, n):
                if random.random() < 0.5:
                    edges.add((i, j))
        return (n, edges)
    
    def compute_minimal_rank(graph):
        n, edges = graph
        adjacency_matrix = [[0] * n for _ in range(n)]
        for u, v in edges:
            adjacency_matrix[u][v] = 1
            adjacency_matrix[v][u] = 1
        
        rank = 0
        while True:
            found_zero_row = False
            for i in range(n):
                if all(adjacency_matrix[i][j] == 0 for j in range(n)):
                    found_zero_row = True
                    break
            if not found_zero_row:
                break
            
            rank += 1
            for i in range(n):
                if adjacency_matrix[i][i] != 0:
                    for j in range(n):
                        if adjacency_matrix[j][j] == 0 and any(adjacency_matrix[j][k] * adjacency_matrix[k][i] != 0 for k in range(n) if k != j):
                            adjacency_matrix[j][j] = 1
                            break
        
        return rank
    
    def is_isomorphic(graph1, graph2):
        n1, edges1 = graph1
        n2, edges2 = graph2
        if n1 != n2:
            return False
        
        for perm in itertools.permutations(range(n1)):
            permuted_edges = {(perm[u], perm[v]) for u, v in edges1}
            if permuted_edges == edges2:
                return True
        return False
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        instances_tested = 0
        total_rank_sum = 0
        
        for _ in range(5):  # Ensure at least 30 instances per seed
            graph1 = generate_random_graph(n)
            graph2 = generate_random_graph(n)
            
            if is_isomorphic(graph1, graph2):
                rank = compute_minimal_rank(graph1)
                total_rank_sum += rank
                instances_tested += 1
        
        if instances_tested == 0:
            return {
                "metric_name": "minimal_rank",
                "metric_value": None,
                "instances_tested": instances_tested,
                "conjecture_holds": False,
                "counterexample": "no_isomorphic_instances"
            }
        
        mean_rank = total_rank_sum / instances_tested
        results.append(mean_rank)
    
    correlation_coefficient = calculate_correlation(n_values, results)
    
    return {
        "metric_name": "minimal_rank",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "conjecture_holds": correlation_coefficient >= 0.9,
        "counterexample": ""
    }

def calculate_correlation(x, y):
    n = len(x)
    if n != len(y):
        raise ValueError("x and y must have the same length")
    
    mean_x = sum(x) / n
    mean_y = sum(y) / n
    
    numerator = sum((xi - mean_x) * (yi - mean_y) for xi, yi in zip(x, y))
    denominator = math.sqrt(sum((xi - mean_x) ** 2 for xi in x)) * math.sqrt(sum((yi - mean_y) ** 2 for yi in y))
    
    if denominator == 0:
        return None
    
    return numerator / denominator

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(1, 1000000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        
        if "metric_value" not in trial_result or trial_result["metric_value"] is None:
            continue
        
        results.append(trial_result["metric_value"])
    
    mean_value = sum(results) / len(results)
    std_value = math.sqrt(sum((x - mean_value) ** 2 for x in results) / len(results))
    support_fraction = sum(1 for r in results if r >= 0.9) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(r < 0.9 for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if result < 0.9)
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient_below_0.9\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE support_fraction_below_threshold")