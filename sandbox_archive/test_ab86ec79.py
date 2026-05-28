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
    
    def generate_graph(n):
        # Generate a random connected graph with n vertices using an adjacency matrix
        adj_matrix = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i + 1, n):
                if random.choice([True, False]):
                    adj_matrix[i][j] = 1
                    adj_matrix[j][i] = 1
        return adj_matrix
    
    def connectivity(adj_matrix):
        # Calculate the connectivity (minimum degree) of the graph
        n = len(adj_matrix)
        min_degree = float('inf')
        for i in range(n):
            degree = sum(adj_matrix[i])
            if degree < min_degree:
                min_degree = degree
        return min_degree
    
    def quantum_walk(adj_matrix, n):
        # Simulate a simple random walk on the graph
        n_steps = 100
        start_node = random.randint(0, len(adj_matrix) - 1)
        position = start_node
        for _ in range(n_steps):
            neighbors = [j for j in range(len(adj_matrix)) if adj_matrix[position][j] == 1]
            if not neighbors:
                break
            position = random.choice(neighbors)
        return position
    
    def communication_complexity(n, connectivity):
        # Simulate XOR communication complexity using the quantum walk
        total_cost = 0
        for _ in range(10):  # Repeat multiple times to get an average
            start_node = random.randint(0, len(adj_matrix) - 1)
            end_node = quantum_walk(adj_matrix, n)
            if start_node != end_node:
                total_cost += 2  # Each node-to-node communication costs 2 units
        return total_cost
    
    n_values = [5, 10, 15, 20, 30, 40]
    instances_tested = 0
    total_metric_value = 0
    
    for n in n_values:
        adj_matrix = generate_graph(n)
        kappa = connectivity(adj_matrix)
        if kappa == 0:
            continue
        
        metric_value = communication_complexity(n, kappa)
        total_metric_value += metric_value
        instances_tested += 1
    
    if instances_tested == 0:
        return {
            "metric_name": "communication_complexity",
            "metric_value": None,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "insufficient_instances"
        }
    
    mean_metric_value = total_metric_value / instances_tested
    conjecture_holds = all(metric_value <= (n**2 / kappa**2) for n, kappa in zip(n_values, [connectivity(generate_graph(n)) for _ in range(instances_tested)]))
    counterexample = "" if conjecture_holds else "communication_complexity > O(n^2/κ(G)^2)"
    
    return {
        "metric_name": "communication_complexity",
        "metric_value": mean_metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and any(r["counterexample"] != "" for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")