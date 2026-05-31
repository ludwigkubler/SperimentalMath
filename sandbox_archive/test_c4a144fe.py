# auto-injected by SEC sandbox
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from itertools import combinations

# Helper functions for linear algebra
def matrix_multiplication(A, B):
    if len(A[0]) != len(B):
        raise ValueError("Incompatible dimensions for matrix multiplication")
    result = [[sum(a * b for a, b in zip(row_a, col_b)) for col_b in zip(*B)] for row_a in A]
    return result

def gaussian_elimination(matrix):
    augmented_matrix = [row[:] + [0] for row in matrix]
    n = len(matrix)
    m = len(matrix[0])
    
    for i in range(n):
        # Find the pivot
        max_row = i
        for j in range(i+1, n):
            if abs(augmented_matrix[j][i]) > abs(augmented_matrix[max_row][i]):
                max_row = j
        
        # Swap rows
        augmented_matrix[i], augmented_matrix[max_row] = augmented_matrix[max_row], augmented_matrix[i]
        
        # Eliminate below the pivot
        for j in range(i+1, n):
            factor = -augmented_matrix[j][i] / augmented_matrix[i][i]
            for k in range(m):
                augmented_matrix[j][k] += factor * augmented_matrix[i][k]
    
    return augmented_matrix

def rank_of_matrix(matrix):
    rref = gaussian_elimination(matrix)
    rank = 0
    for row in rref:
        if any(row):
            rank += 1
    return rank

# Function to generate a random communication graph with bounded degree
def generate_communication_graph(n, max_degree):
    G = {i: [] for i in range(n)}
    edges_added = 0
    while edges_added < n * max_degree // 2:
        u, v = random.sample(range(n), 2)
        if u != v and v not in G[u]:
            G[u].append(v)
            G[v].append(u)
            edges_added += 1
    return G

# Function to compute communication complexity of a graph
def communication_complexity(G):
    n = len(G)
    total_edges = sum(len(neighbors) for neighbors in G.values()) // 2
    return total_edges * (n - 1)

# Function to map a communication graph to an algebraic variety and compute mls(G)
def minimal_local_system_rank(G):
    n = len(G)
    A = [[0] * n for _ in range(n)]
    
    # Create the adjacency matrix with weights
    for u, neighbors in G.items():
        for v in neighbors:
            A[u][v] += 1
    
    return rank_of_matrix(A)

# Function to run a single trial
def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_max = 40
    instances_tested = 0
    metric_values = []
    counterexample = ""
    
    for n in range(5, n_max + 1):
        G = generate_communication_graph(n, max_degree=3)
        mls_G = minimal_local_system_rank(G)
        c_G = communication_complexity(G)
        
        instances_tested += len(G)
        metric_values.append(mls_G / c_G)
    
    if instances_tested < 30:
        return {
            "metric_name": "mls(G) / c(G)",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "insufficient_instances"
        }
    
    mean_rank = sum(metric_values) / len(metric_values)
    std_dev = math.sqrt(sum((x - mean_rank) ** 2 for x in metric_values) / len(metric_values))
    
    return {
        "metric_name": "mls(G) / c(G)",
        "metric_value": mean_rank,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": mean_rank >= 0.7,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    elif support_fraction >= 0.95:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample='low_correlation' first_failing_seed={first_failing_seed}")