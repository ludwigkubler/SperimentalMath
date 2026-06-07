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

# Constants
MAX_N = 40
NUM_TRIALS = 30
DEGREES = [2, 3]  # Example degrees for d-regular circuits
DEFAULT_SEEDS = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]

def generate_d_regular_circuit(d, n):
    if d < 2 or n <= 0:
        raise ValueError("Invalid d-regular circuit parameters")
    
    # Generate a random d-regular graph using the configuration model
    degree_sequence = [d] * n
    adjacency_matrix = [[0 for _ in range(n)] for _ in range(n)]
    
    while True:
        # Shuffle the degree sequence to create a random permutation
        random.shuffle(degree_sequence)
        
        # Create an adjacency matrix from the shuffled degree sequence
        for i in range(n):
            neighbors = random.sample(range(i + 1, n), degree_sequence[i] // 2)
            for neighbor in neighbors:
                adjacency_matrix[i][neighbor] = 1
                adjacency_matrix[neighbor][i] = 1
        
        # Check if the resulting graph is d-regular
        if all(sum(row) == d for row in adjacency_matrix):
            break
    
    return adjacency_matrix

def compute_minimal_index(adjacency_matrix):
    n = len(adjacency_matrix)
    min_index = float('inf')
    
    # Compute the minimal index using a simple heuristic (this is a placeholder)
    for i in range(n):
        for j in range(i + 1, n):
            if adjacency_matrix[i][j] == 0:
                continue
            distance = abs(i - j)  # Placeholder distance calculation
            min_index = min(min_index, distance)
    
    return min_index

def compute_entanglement_complexity(adjacency_matrix):
    n = len(adjacency_matrix)
    complexity = 0
    
    # Compute the entanglement complexity using a simple heuristic (this is a placeholder)
    for i in range(n):
        for j in range(i + 1, n):
            if adjacency_matrix[i][j] == 1:
                complexity += abs(i - j)  # Placeholder complexity calculation
    
    return complexity

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    metric_name = "PearsonCorrelation"
    instances_tested = 0
    n_max = 0
    min_indices = []
    entanglement_complexities = []
    
    for d in DEGREES:
        for n in range(5, MAX_N + 1, 5):
            adjacency_matrix = generate_d_regular_circuit(d, n)
            if adjacency_matrix is None:
                continue
            
            min_index = compute_minimal_index(adjacency_matrix)
            entanglement_complexity = compute_entanglement_complexity(adjacency_matrix)
            
            min_indices.append(min_index)
            entanglement_complexities.append(entanglement_complexity)
            instances_tested += 1
            n_max = max(n_max, n)
    
    if not min_indices or not entanglement_complexities:
        return {
            "metric_name": metric_name,
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "No valid circuits generated"
        }
    
    # Compute Pearson correlation coefficient
    mean_min_index = sum(min_indices) / len(min_indices)
    mean_entanglement_complexity = sum(entanglement_complexities) / len(entanglement_complexities)
    
    covariance = sum((min_indices[i] - mean_min_index) * (entanglement_complexities[i] - mean_entanglement_complexity) for i in range(len(min_indices)))
    variance_min_index = sum((min_indices[i] - mean_min_index) ** 2 for i in range(len(min_indices)))
    variance_entanglement_complexity = sum((entanglement_complexities[i] - mean_entanglement_complexity) ** 2 for i in range(len(entanglement_complexities)))
    
    if variance_min_index == 0 or variance_entanglement_complexity == 0:
        return {
            "metric_name": metric_name,
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "Variance is zero"
        }
    
    pearson_correlation = covariance / math.sqrt(variance_min_index * variance_entanglement_complexity)
    
    return {
        "metric_name": metric_name,
        "metric_value": pearson_correlation,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": abs(pearson_correlation) >= 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(seed) for seed in sys.argv[1:]] or DEFAULT_SEEDS
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all("conjecture_holds" in r and r["conjecture_holds"] for r in results):
        mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not ("conjecture_holds" in result and result["conjecture_holds"]))
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")