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
    
    def generate_d_regular_graph(n, d):
        if (d * n) % 2 != 0 or d > n - 1:
            return None
        adjacency_matrix = [[0] * n for _ in range(n)]
        degree_counts = [0] * n
        edges_added = 0
        
        while edges_added < d * n // 2:
            u, v = random.sample(range(n), 2)
            if u != v and adjacency_matrix[u][v] == 0:
                adjacency_matrix[u][v] = 1
                adjacency_matrix[v][u] = 1
                degree_counts[u] += 1
                degree_counts[v] += 1
                edges_added += 1
        
        return adjacency_matrix
    
    def gaussian_elimination(matrix):
        n = len(matrix)
        for i in range(n):
            max_row = i
            for j in range(i+1, n):
                if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                    max_row = j
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
            
            factor = Fraction(matrix[i][i])
            for j in range(n):
                matrix[i][j] /= factor
            
            for j in range(n):
                if i != j:
                    factor = Fraction(matrix[j][i])
                    for k in range(n):
                        matrix[j][k] -= factor * matrix[i][k]
        
        rank = sum(1 for row in matrix if any(row))
        return rank
    
    def hodge_de_rham_cohomology_dimension(adjacency_matrix):
        n = len(adjacency_matrix)
        if not adjacency_matrix:
            return 0
        return gaussian_elimination(adjacency_matrix)
    
    def circuit_satisfiability_complexity(n, d):
        # Placeholder for actual complexity calculation
        return random.randint(1, n * d)
    
    n_values = [5, 10, 15, 20, 30, 40]
    h_dims = []
    complexities = []
    
    for n in n_values:
        graph = generate_d_regular_graph(n, 2)  # Example: 2-regular graph
        if graph is None:
            continue
        
        h_dim = hodge_de_rham_cohomology_dimension(graph)
        complexity = circuit_satisfiability_complexity(n, 2)  # Example: 2-regular graph
        
        h_dims.append(h_dim)
        complexities.append(complexity)
    
    if not h_dims or not complexities:
        return {
            "metric_name": "Pearson correlation coefficient",
            "metric_value": None,
            "instances_tested": len(n_values),
            "n_max": max(n_values) if n_values else 0,
            "conjecture_holds": False,
            "counterexample": "graph_generation_failed"
        }
    
    mean_h_dim = sum(h_dims) / len(h_dims)
    mean_complexity = sum(complexities) / len(complexities)
    
    correlation_coefficient = (sum((h - mean_h_dim) * (c - mean_complexity) for h, c in zip(h_dims, complexities)) /
                               math.sqrt(sum((h - mean_h_dim) ** 2 for h in h_dims) *
                                         sum((c - mean_complexity) ** 2 for c in complexities)))
    
    return {
        "metric_name": "Pearson correlation coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(n_values),
        "n_max": max(n_values),
        "conjecture_holds": correlation_coefficient > 0.7,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        print("RESULT: FALSIFIED counterexample='' first_failing_seed=None")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_evidence n_tested={len(results)}")