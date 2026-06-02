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
    
    def gaussian_elimination(matrix):
        n = len(matrix)
        for i in range(n):
            # Find the maximum element in this column
            max_idx = i + max(range(i, n), key=lambda j: abs(matrix[j][i]))
            # Swap rows to move the max element to the diagonal
            matrix[i], matrix[max_idx] = matrix[max_idx], matrix[i]
            # Eliminate all other elements in this column
            for j in range(n):
                if i != j:
                    factor = Fraction(matrix[j][i], matrix[i][i])
                    for k in range(n + 1):
                        matrix[j][k] -= factor * matrix[i][k]
        return matrix
    
    def hodge_dimension(graph, n):
        # Construct the adjacency matrix
        adj_matrix = [[0] * n for _ in range(n)]
        for u, v in graph:
            adj_matrix[u][v] = 1
            adj_matrix[v][u] = 1
        
        # Perform Gaussian elimination to find the rank of the matrix
        reduced_matrix = gaussian_elimination(adj_matrix)
        
        # The Hodge dimension is the number of non-zero rows in the reduced matrix
        return sum(1 for row in reduced_matrix if any(row))
    
    def tseitin_formula(graph, n):
        clauses = []
        literals = {}
        literal_count = 0
        
        for u in range(n):
            literals[u] = literal_count
            literal_count += 1
            literals[-u] = literal_count
            literal_count += 1
        
        for u, v in graph:
            clauses.append([literals[u], -literals[v]])
            clauses.append([-literals[u], literals[v]])
        
        return clauses
    
    def entropy(clauses):
        n = len(clauses)
        if n == 0: return 0
        p = Fraction(1, n)
        return -p * math.log2(p) * n
    
    d = 3  # Degree of the regular graph
    n_values = [10, 20, 30, 40]
    results = []
    
    for n in n_values:
        if n % d != 0: continue
        
        instances_tested = 0
        total_hd = 0
        total_entropy = 0
        
        for _ in range(30):
            # Generate a random d-regular graph
            edges = set()
            while len(edges) < n * d // 2:
                u, v = random.sample(range(n), 2)
                if (u, v) not in edges and (v, u) not in edges:
                    edges.add((u, v))
            
            graph = list(edges)
            instances_tested += 1
            
            # Calculate the Hodge dimension
            hd = hodge_dimension(graph, n)
            total_hd += hd
            
            # Calculate the Tseitin formula and entropy
            clauses = tseitin_formula(graph, n)
            clause_entropy = entropy(clauses)
            total_entropy += clause_entropy
        
        if instances_tested == 0: continue
        
        avg_hd = total_hd / instances_tested
        avg_entropy = total_entropy / instances_tested
        correlation_coefficient = (instances_tested * avg_hd * avg_entropy - 
                                   sum(hd * entropy for hd, entropy in zip(results, results))) / \
                                  math.sqrt(instances_tested * (avg_hd ** 2) * (avg_entropy ** 2))
        
        if correlation_coefficient < 0.5:
            return {
                "metric_name": "Correlation Coefficient",
                "metric_value": correlation_coefficient,
                "instances_tested": instances_tested,
                "n_max": n,
                "conjecture_holds": False,
                "counterexample": "Low correlation coefficient"
            }
        
        results.append(correlation_coefficient)
    
    if not results:
        return {
            "metric_name": "Correlation Coefficient",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "No data collected"
        }
    
    mean = sum(results) / len(results)
    std_dev = math.sqrt(sum((x - mean) ** 2 for x in results) / len(results))
    support_fraction = len([r for r in results if r >= 0.5]) / len(results)
    
    return {
        "metric_name": "Correlation Coefficient",
        "metric_value": mean,
        "instances_tested": sum(len(results) for n in n_values),
        "n_max": max(n_values),
        "conjecture_holds": support_fraction >= 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        
        if "conjecture_holds" not in trial_result:
            continue
        
        if trial_result["conjecture_holds"]:
            support_fraction = sum(1 for r in results if r >= 0.5) / len(results)
            if support_fraction >= 0.8:
                print(f"RESULT: SUPPORTED mean={trial_result['metric_value']:.2f} std={std_dev:.2f} support_fraction={support_fraction:.2f}")
                break
        else:
            first_failing_seed = seed
            counterexample = trial_result["counterexample"]
            print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")
            break

    if "conjecture_holds" not in locals():
        print("RESULT: INCONCLUSIVE insufficient_data")