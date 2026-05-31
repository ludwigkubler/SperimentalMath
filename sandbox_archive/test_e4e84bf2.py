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

# Helper functions for matrix operations and Gaussian elimination
def matrix_multiplication(A, B):
    if len(A[0]) != len(B):
        raise ValueError("Incompatible dimensions for matrix multiplication")
    result = [[sum(a * b for a, b in zip(row_a, col_b)) for col_b in zip(*B)] for row_a in A]
    return result

def gaussian_elimination(A):
    n = len(A)
    for i in range(n):
        # Find the pivot
        max_row = i + max(range(i, n), key=lambda k: abs(A[k][i]))
        A[i], A[max_row] = A[max_row], A[i]
        
        # Eliminate below the pivot
        for j in range(i + 1, n):
            factor = -A[j][i] / A[i][i]
            A[j] = [factor * a + b for a, b in zip(A[i], A[j])]
    
    # Back-substitute to get the solution
    x = [0] * n
    for i in range(n-1, -1, -1):
        x[i] = (A[i][-1] - sum(A[i][j] * x[j] for j in range(i+1, n))) / A[i][i]
    return x

def rank_of_matrix(matrix):
    augmented_matrix = [row + [0] for row in matrix]
    reduced_row_echelon_form = gaussian_elimination(augmented_matrix)
    rank = sum(1 for row in reduced_row_echelon_form if any(row))
    return rank

# Function to generate a random communication graph with bounded degree
def generate_communication_graph(n, max_degree):
    G = [[] for _ in range(n)]
    degrees = [0] * n
    edges_added = 0
    
    while edges_added < (n - 1) and any(d < max_degree for d in degrees):
        u = random.randint(0, n-1)
        v = random.randint(0, n-1)
        if u != v and len(G[u]) < max_degree and len(G[v]) < max_degree:
            G[u].append(v)
            G[v].append(u)
            degrees[u] += 1
            degrees[v] += 1
            edges_added += 1
    
    return G

# Function to compute the minimal local system rank of an algebraic variety associated with a communication graph
def minimal_local_system_rank(G):
    n = len(G)
    neighbors = [set() for _ in range(n)]
    
    for u, v in [(u, v) for u in range(n) for v in G[u]]:
        neighbors[u].add(v)
        neighbors[v].add(u)
    
    A = [[0] * (n + len(neighbors)) for _ in range(n)]
    for i in range(n):
        A[i][i] = 1
        for j in neighbors[i]:
            A[j][i + len(neighbors)] = 1
    
    return rank_of_matrix(A)

# Function to compute the communication complexity of a communication graph
def communication_complexity(G):
    n = len(G)
    max_degree = max(len(neighbors) for neighbors in G)
    return sum(max_degree * (n - len(neighbors)) for neighbors in G) / 2

# Main function to run one trial with a given seed
def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        G = generate_communication_graph(n, max_degree=3)
        mls_G = minimal_local_system_rank(G)
        c_G = communication_complexity(G)
        
        results.append({
            "n": n,
            "mls_G": mls_G,
            "c_G": c_G
        })
    
    if not results:
        return {
            "metric_name": "minimal_local_system_rank",
            "metric_value": 0.0,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "no_graphs_generated"
        }
    
    mean_ranks = sum(result["mls_G"] for result in results) / len(results)
    mean_complexities = sum(result["c_G"] for result in results) / len(results)
    correlation_coefficient = 0.0
    
    if mean_complexities != 0:
        numerator = sum((result["mls_G"] - mean_ranks) * (result["c_G"] - mean_complexities) for result in results)
        denominator = math.sqrt(sum((result["mls_G"] - mean_ranks)**2 for result in results)) * math.sqrt(sum((result["c_G"] - mean_complexities)**2 for result in results))
        correlation_coefficient = numerator / denominator
    
    return {
        "metric_name": "minimal_local_system_rank",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(result["n"] for result in results),
        "conjecture_holds": correlation_coefficient >= 0.7,
        "counterexample": ""
    }

# Main block to run trials with given seeds
if __name__ == "__main__":
    import sys
    
    if not sys.argv[1:]:
        seeds = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    else:
        seeds = [int(seed) for seed in sys.argv[1:]]
    
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"n_max\": {result['n_max']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    if all("conjecture_holds" in result and result["conjecture_holds"] for result in results):
        mean_value = sum(result["metric_value"] for result in results) / len(results)
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_value} std=0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not ("conjecture_holds" in result and result["conjecture_holds"]))
        counterexample = "first failing seed"
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")