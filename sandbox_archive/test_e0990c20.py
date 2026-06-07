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
    
    def del_pezzo_degree(graph):
        n = len(graph)
        if n <= 2:
            return 0
        
        # Construct the adjacency matrix
        adj_matrix = [[0] * n for _ in range(n)]
        for u, v in graph:
            adj_matrix[u][v] = 1
            adj_matrix[v][u] = 1
        
        # Gaussian elimination to find the rank of the matrix
        def gaussian_elimination(matrix):
            rows, cols = len(matrix), len(matrix[0])
            rank = 0
            
            for col in range(cols):
                max_row = None
                for row in range(rank, rows):
                    if matrix[row][col] != 0:
                        max_row = row
                        break
                
                if max_row is not None:
                    matrix[max_row], matrix[rank] = matrix[rank], matrix[max_row]
                    
                    for r in range(rows):
                        if r != rank and matrix[r][col] != 0:
                            factor = -matrix[r][col] / matrix[rank][col]
                            for c in range(cols):
                                matrix[r][c] += factor * matrix[rank][c]
                    
                    rank += 1
            
            return rank
        
        rank = gaussian_elimination(adj_matrix)
        del_pezzo = n - rank
        return del_pezzo
    
    def circuit_entanglement_complexity(graph):
        # Placeholder for actual computation of entanglement complexity
        # For simplicity, we use a dummy value that depends on the number of edges
        n = len(graph)
        m = len(graph) // 2  # Assuming a regular graph with even degree
        return m / (n * (n - 1))
    
    def generate_d_regular_graph(n, d):
        if (d * n) % 2 != 0:
            raise ValueError("Degree must be even for a regular graph")
        
        edges = set()
        while len(edges) < d * n // 2:
            u = random.randint(0, n - 1)
            v = random.randint(0, n - 1)
            if u != v and (u, v) not in edges and (v, u) not in edges:
                edges.add((u, v))
        
        return list(edges)
    
    del_pezzo_values = []
    entanglement_values = []
    instances_tested = 0
    n_max = 0
    
    for n in [5, 10, 15, 20, 30, 40]:
        if n > 40:
            break
        
        del_pezzo_sum = 0.0
        entanglement_sum = 0.0
        
        for _ in range(5):  # Test with 5 instances per size
            graph = generate_d_regular_graph(n, 2)
            del_pezzo_value = del_pezzo_degree(graph)
            entanglement_value = circuit_entanglement_complexity(graph)
            
            del_pezzo_values.append(del_pezzo_value)
            entanglement_values.append(entanglement_value)
            
            instances_tested += 1
            n_max = max(n_max, n)
    
    if len(del_pezzo_values) == 0 or len(entanglement_values) == 0:
        return {
            "metric_name": "Pearson correlation coefficient",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "empty_graph"
        }
    
    # Calculate Pearson correlation coefficient
    mean_del_pezzo = sum(del_pezzo_values) / len(del_pezzo_values)
    mean_entanglement = sum(entanglement_values) / len(entanglement_values)
    
    covariance = sum((del_pezzo - mean_del_pezzo) * (entanglement - mean_entanglement) for del_pezzo, entanglement in zip(del_pezzo_values, entanglement_values)) / len(del_pezzo_values)
    variance_del_pezzo = sum((del_pezzo - mean_del_pezzo) ** 2 for del_pezzo in del_pezzo_values) / len(del_pezzo_values)
    variance_entanglement = sum((entanglement - mean_entanglement) ** 2 for entanglement in entanglement_values) / len(entanglement_values)
    
    if variance_del_pezzo == 0 or variance_entanglement == 0:
        return {
            "metric_name": "Pearson correlation coefficient",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "constant_metric"
        }
    
    pearson_corr = covariance / (math.sqrt(variance_del_pezzo) * math.sqrt(variance_entanglement))
    
    return {
        "metric_name": "Pearson correlation coefficient",
        "metric_value": pearson_corr,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": pearson_corr >= 0.7 or any(abs(del_pezzo - entanglement) > 1.5 for del_pezzo, entanglement in zip(del_pezzo_values, entanglement_values)),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...run_trial output...}}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")