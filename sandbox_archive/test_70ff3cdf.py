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
        if n * d % 2 != 0 or d < 1 or d >= n:
            raise ValueError("Invalid parameters for generating a d-regular graph")
        
        adjacency_matrix = [[0] * n for _ in range(n)]
        edges_added = set()
        
        def add_edge(u, v):
            if (u, v) not in edges_added and (v, u) not in edges_added:
                adjacency_matrix[u][v] = 1
                adjacency_matrix[v][u] = 1
                edges_added.add((u, v))
                edges_added.add((v, u))
        
        for i in range(n):
            neighbors = random.sample(range(n), d)
            for j in neighbors:
                if i < j:
                    add_edge(i, j)
        
        return adjacency_matrix
    
    def matrix_rank(matrix):
        m, n = len(matrix), len(matrix[0])
        rank = 0
        for i in range(m):
            max_nonzero = -1
            max_col = -1
            for j in range(n):
                if matrix[i][j] != 0 and (max_nonzero == -1 or abs(matrix[i][j]) > abs(matrix[max_nonzero][max_col])):
                    max_nonzero = i
                    max_col = j
            
            if max_nonzero == -1:
                continue
            
            rank += 1
            for k in range(n):
                matrix[max_nonzero][k] /= matrix[max_nonzero][max_col]
            
            for j in range(m):
                if j != max_nonzero and matrix[j][max_col] != 0:
                    for k in range(n):
                        matrix[j][k] -= matrix[max_nonzero][k] * matrix[j][max_col]
        
        return rank
    
    def automorphism_group_order(matrix):
        n = len(matrix)
        identity = [[1 if i == j else 0 for j in range(n)] for i in range(n)]
        
        def multiply_matrices(a, b):
            result = [[0] * n for _ in range(n)]
            for i in range(n):
                for j in range(n):
                    for k in range(n):
                        result[i][j] += a[i][k] * b[k][j]
            return result
        
        def is_permutation_matrix(matrix):
            if len(matrix) != len(matrix[0]):
                return False
            identity = [[1 if i == j else 0 for j in range(len(matrix))] for i in range(len(matrix))]
            for i in range(len(matrix)):
                row_sum = sum(matrix[i])
                col_sum = sum(matrix[j][i] for j in range(len(matrix)))
                if row_sum != 1 or col_sum != 1:
                    return False
            return True
        
        def is_group_element(matrix):
            if not is_permutation_matrix(matrix):
                return False
            result = multiply_matrices(matrix, matrix)
            for i in range(n):
                for j in range(n):
                    if result[i][j] != identity[i][j]:
                        return False
            return True
        
        order = 1
        current_element = identity
        while True:
            current_element = multiply_matrices(current_element, matrix)
            if is_group_element(current_element):
                order += 1
            else:
                break
        
        return order
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        graph = generate_d_regular_graph(n, 3)
        rank = matrix_rank(graph)
        order = automorphism_group_order(graph)
        
        results.append({
            "n": n,
            "rank": rank,
            "order": order
        })
    
    correlation_coefficient = 0.0
    if len(results) > 1:
        x_mean = sum(result["order"] for result in results) / len(results)
        y_mean = sum(result["rank"] for result in results) / len(results)
        
        numerator = sum((result["order"] - x_mean) * (result["rank"] - y_mean) for result in results)
        denominator = math.sqrt(sum((result["order"] - x_mean) ** 2 for result in results)) * math.sqrt(sum((result["rank"] - y_mean) ** 2 for result in results))
        
        correlation_coefficient = numerator / denominator
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(result["n"] for result in results),
        "conjecture_holds": correlation_coefficient >= 0.9,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")