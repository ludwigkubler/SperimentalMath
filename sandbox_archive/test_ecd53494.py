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

def generate_random_d_regular_graph(n, d):
    if n % d != 0:
        raise ValueError("Graph size must be a multiple of the degree")
    
    graph = {i: [] for i in range(n)}
    degree_count = [0] * n
    
    for node in range(n):
        available_neighbors = [i for i in range(n) if i != node and len(graph[i]) < d]
        neighbors_to_add = random.sample(available_neighbors, min(d - degree_count[node], len(available_neighbors)))
        
        for neighbor in neighbors_to_add:
            graph[node].append(neighbor)
            graph[neighbor].append(node)
            degree_count[node] += 1
            degree_count[neighbor] += 1
    
    return graph

def compute_local_induction_dimension(graph):
    n = len(graph)
    adjacency_matrix = [[0 for _ in range(n)] for _ in range(n)]
    
    for node, neighbors in graph.items():
        for neighbor in neighbors:
            adjacency_matrix[node][neighbor] = 1
            adjacency_matrix[neighbor][node] = 1
    
    # Gaussian elimination to find the rank of the adjacency matrix
    rank = 0
    for i in range(n):
        if adjacency_matrix[i][i] == 0:
            found_pivot = False
            for j in range(i + 1, n):
                if adjacency_matrix[j][i] != 0:
                    for k in range(n):
                        adjacency_matrix[i][k], adjacency_matrix[j][k] = adjacency_matrix[j][k], adjacency_matrix[i][k]
                    found_pivot = True
                    break
            if not found_pivot:
                continue
        
        rank += 1
        denom = Fraction(adjacency_matrix[i][i])
        for j in range(n):
            adjacency_matrix[i][j] /= denom
        
        for j in range(n):
            if i != j:
                factor = Fraction(adjacency_matrix[j][i])
                for k in range(n):
                    adjacency_matrix[j][k] -= factor * adjacency_matrix[i][k]
    
    return rank

def compute_clause_subset_entropy(clauses):
    n = len(clauses)
    total_clauses = sum(len(c) for c in clauses)
    entropy = 0
    for clause in clauses:
        p = Fraction(1, total_clauses)
        entropy -= p * math.log2(p)
    
    return entropy

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        graph = generate_random_d_regular_graph(n, 3)
        clauses = []  # Placeholder for SAT formula generation
        for node in range(n):
            clause = [node + 1] * (len(graph[node]) - 1)  # Simplified clause representation
            clauses.append(clause)
        
        ltd = compute_local_induction_dimension(graph)
        entropy = compute_clause_subset_entropy(clauses)
        
        results.append({
            "n": n,
            "ltd": ltd,
            "entropy": entropy
        })
    
    correlation_coefficient = 0
    for i in range(len(results)):
        for j in range(i + 1, len(results)):
            correlation_coefficient += (results[i]["ltd"] - results[0]["ltd"]) * (results[j]["entropy"] - results[0]["entropy"])
    
    correlation_coefficient /= (len(results) * (len(results) - 1))
    
    return {
        "metric_name": "Correlation Coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(r["n"] for r in results),
        "conjecture_holds": abs(correlation_coefficient) >= 0.5,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")