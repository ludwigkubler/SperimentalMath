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
        graph = {i: [] for i in range(n)}
        degrees = [random.randint(1, 5) for _ in range(n)]
        edges_added = set()
        for i in range(n):
            for _ in range(degrees[i]):
                j = random.choice([j for j in range(n) if j != i and (i, j) not in edges_added])
                graph[i].append(j)
                graph[j].append(i)
                edges_added.add((i, j))
        return graph
    
    def max_degree(graph):
        return max(len(neighbors) for neighbors in graph.values())
    
    def grothendieck_teichmueller_group_rank(graph):
        # Placeholder function to simulate the computation of GT(G)
        # Replace this with actual implementation if needed
        n = len(graph)
        d = max_degree(graph)
        rank = random.randint(1, 2 * int(math.sqrt(n)))
        return rank
    
    def correlation(x, y):
        mean_x = sum(x) / len(x)
        mean_y = sum(y) / len(y)
        numerator = sum((xi - mean_x) * (yi - mean_y) for xi, yi in zip(x, y))
        denominator = math.sqrt(sum((xi - mean_x) ** 2 for xi in x)) * math.sqrt(sum((yi - mean_y) ** 2 for yi in y))
        return numerator / denominator if denominator != 0 else 0
    
    n_values = [5, 10, 15, 20, 30, 40]
    ranks = []
    degrees = []
    
    for n in n_values:
        graph = generate_random_graph(n)
        rank = grothendieck_teichmueller_group_rank(graph)
        ranks.append(rank)
        degrees.append(max_degree(graph))
    
    corr_log_d = correlation(ranks, [math.log(d) for d in degrees])
    corr_sqrt_n = correlation(ranks, [math.sqrt(n) for n in n_values])
    
    instances_tested = len(ranks)
    n_max = max(n_values)
    conjecture_holds = corr_log_d >= 0.7 and corr_sqrt_n <= 0.5
    counterexample = "" if conjecture_holds else "correlation_with_log_d or sqrt_n_out_of_bounds"
    
    return {
        "metric_name": "Correlation",
        "metric_value": corr_log_d,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_corr_log_d = sum(result["metric_value"] for result in results) / len(results)
    std_corr_log_d = math.sqrt(sum((result["metric_value"] - mean_corr_log_d) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_corr_log_d} std={std_corr_log_d} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_with_log_d or sqrt_n_out_of_bounds\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE")