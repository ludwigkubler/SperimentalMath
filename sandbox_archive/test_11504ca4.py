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

# Helper functions for linear algebra
def gaussian_elimination(matrix):
    n = len(matrix)
    for i in range(n):
        # Find pivot row
        max_row = i
        for j in range(i+1, n):
            if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                max_row = j
        matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
        
        # Eliminate non-pivot elements
        pivot = matrix[i][i]
        for k in range(n):
            matrix[i][k] /= pivot
        
        for j in range(n):
            if i != j:
                factor = matrix[j][i]
                for k in range(n):
                    if k < i:  # Avoid modifying the pivot row
                        matrix[j][k] -= factor * matrix[i][k]

def rank(matrix):
    n, m = len(matrix), len(matrix[0])
    gaussian_elimination(matrix)
    rank = 0
    for i in range(n):
        if any(matrix[i][j] != 0 for j in range(m)):
            rank += 1
    return rank

# Function to generate a random graph as an adjacency matrix
def generate_graph(n):
    graph = [[0]*n for _ in range(n)]
    edges = set()
    while len(edges) < n*(n-1)//2:
        u, v = random.sample(range(n), 2)
        if u != v and (u, v) not in edges and (v, u) not in edges:
            graph[u][v] = 1
            graph[v][u] = 1
            edges.add((u, v))
    return graph

# Function to compute the BP ReadTwice circuit threshold for a graph
def bp_read_twice(graph):
    n = len(graph)
    max_k = 0
    for k in range(1, n+1):
        if all(sum(graph[u][v] for u in range(k) if v >= k) == sum(graph[u][v] for u in range(n-k) if v < n-k) for v in range(n)):
            max_k = k
    return max_k

# Function to run a single trial with a given seed
def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    # Generate a random graph
    n = random.randint(5, 40)
    graph = generate_graph(n)
    
    # Compute the BP ReadTwice circuit threshold
    k = bp_read_twice(graph)
    
    # Estimate the Hodge structure rank (simplified for testing purposes)
    matrix = [[graph[i][j] for j in range(n)] for i in range(n)]
    rank_value = rank(matrix)
    
    # Check if the conjecture holds
    conjecture_holds = abs(rank_value - k) <= 3 * k**2
    
    return {
        "metric_name": "Rank vs DPLL Heig",
        "metric_value": rank_value,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"Graph with n={n}, k={k}, rank={rank_value}"
    }

# Main function to run multiple trials
if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    # Compute mean and standard deviation of metric_value
    total_metric_value = sum(result["metric_value"] for result in results)
    mean_metric_value = total_metric_value / len(results)
    variance = sum((result["metric_value"] - mean_metric_value) ** 2 for result in results) / len(results)
    std_metric_value = math.sqrt(variance)
    
    # Compute fraction of seeds where conjecture holds
    support_fraction = sum(result["conjecture_holds"] for result in results) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")