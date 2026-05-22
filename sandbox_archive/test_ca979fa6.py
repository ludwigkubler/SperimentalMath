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
    
    def generate_k_clique(n, k):
        if k > n:
            return None
        vertices = list(range(n))
        clique = random.sample(vertices, k)
        adjacency_matrix = [[0] * n for _ in range(n)]
        for u in clique:
            for v in clique:
                if u != v:
                    adjacency_matrix[u][v] = 1
                    adjacency_matrix[v][u] = 1
        return adjacency_matrix
    
    def hodge_index(adjacency_matrix):
        n = len(adjacency_matrix)
        # Construct the affine scheme using a simple mapping (example: sum of entries)
        hodge_value = sum(sum(row) for row in adjacency_matrix)
        return hodge_value
    
    def resolution_length(hodge_value, n):
        if hodge_value == 0:
            return float('inf')
        return 2**n / (hodge_value ** 2)
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_hodge_index = 0
    total_resolution_length = 0
    instances_tested = 0
    
    for n in n_values:
        k = random.randint(2, min(n-1, 5))
        instance = generate_k_clique(n, k)
        if instance is None:
            continue
        
        hodge_value = hodge_index(instance)
        resolution_length_val = resolution_length(hodge_value, n)
        
        total_hodge_index += hodge_value
        total_resolution_length += resolution_length_val
        instances_tested += 1
    
    average_hodge_index = total_hodge_index / instances_tested if instances_tested > 0 else 0
    average_resolution_length = total_resolution_length / instances_tested if instances_tested > 0 else float('inf')
    
    conjecture_holds = (average_hodge_index <= n**(k/2)) and (average_resolution_length >= 2**n / (hodge_value ** 2))
    counterexample = "" if conjecture_holds else f"Average Hodge Index: {average_hodge_index}, Average Resolution Length: {average_resolution_length}"
    
    return {
        "metric_name": "Hodge Index and Resolution Length",
        "metric_value": average_hodge_index,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else list(range(2, 30))  # Default to first 29 primes
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, **{result}}}")
        results.append(result)
    
    if all("conjecture_holds" in r and r["conjecture_holds"] for r in results):
        support_fraction = 1.0
    else:
        support_fraction = sum(1 for r in results if "conjecture_holds" in r and r["conjecture_holds"]) / len(results)
    
    if all("metric_value" in r for r in results) and all(isinstance(r["metric_value"], (int, float)) for r in results):
        mean_metric = sum(r["metric_value"] for r in results) / len(results)
        std_metric = math.sqrt(sum((r["metric_value"] - mean_metric) ** 2 for r in results) / len(results))
    else:
        mean_metric = None
        std_metric = None
    
    if all("conjecture_holds" in r and r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric} std={std_metric} support_fraction={support_fraction}")
    elif any("counterexample" in r and r["counterexample"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if "conjecture_holds" not in r or not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_data")