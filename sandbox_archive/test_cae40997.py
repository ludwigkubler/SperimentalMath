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
    
    def generate_k_regular_graph(n, k):
        if (n * k) % 2 != 0 or k < 1 or n < k:
            return None
        adj_matrix = [[0] * n for _ in range(n)]
        edges_added = 0
        
        while edges_added < n * k // 2:
            u, v = random.sample(range(n), 2)
            if adj_matrix[u][v] == 0 and u != v:
                adj_matrix[u][v] = 1
                adj_matrix[v][u] = 1
                edges_added += 1
        
        return adj_matrix
    
    def gaussian_elimination(matrix):
        n = len(matrix)
        rank = 0
        
        for i in range(n):
            if matrix[i][i] == 0:
                for j in range(i + 1, n):
                    if matrix[j][i] != 0:
                        matrix[i], matrix[j] = matrix[j], matrix[i]
                        break
                else:
                    continue
            
            pivot = matrix[i][i]
            for j in range(n):
                matrix[i][j] /= pivot
            
            for j in range(n):
                if i != j:
                    factor = matrix[j][i]
                    for k in range(n):
                        matrix[j][k] -= factor * matrix[i][k]
            
            rank += 1
        
        return rank
    
    def eigenvalues(matrix):
        n = len(matrix)
        identity = [[0] * n for _ in range(n)]
        for i in range(n):
            identity[i][i] = 1
        
        def subtract_matrices(a, b):
            result = []
            for i in range(n):
                row = []
                for j in range(n):
                    row.append(a[i][j] - b[i][j])
                result.append(row)
            return result
        
        def multiply_matrices(a, b):
            result = [[0] * n for _ in range(n)]
            for i in range(n):
                for j in range(n):
                    for k in range(n):
                        result[i][j] += a[i][k] * b[k][j]
            return result
        
        def add_matrices(a, b):
            result = []
            for i in range(n):
                row = []
                for j in range(n):
                    row.append(a[i][j] + b[i][j])
                result.append(row)
            return result
        
        def matrix_power(matrix, power):
            if power == 0:
                return identity
            elif power == 1:
                return matrix
            else:
                half_power = matrix_power(matrix, power // 2)
                result = multiply_matrices(half_power, half_power)
                if power % 2 != 0:
                    result = multiply_matrices(result, matrix)
                return result
        
        def trace(matrix):
            return sum(matrix[i][i] for i in range(n))
        
        eigenvalues = []
        for k in range(1, n + 1):
            A_k = matrix_power(matrix, k)
            A_k_inv = gaussian_elimination(A_k)
            if A_k_inv == 0:
                break
            lambda_k = trace(A_k) / A_k_inv
            eigenvalues.append(lambda_k)
        
        return eigenvalues
    
    def minimal_rank(eigenvalues):
        return len([e for e in eigenvalues if e != 0])
    
    k_values = [2, 3, 4, 5]
    results = []
    
    for n in range(5, 41):
        for k in k_values:
            graph = generate_k_regular_graph(n, k)
            if graph is None:
                continue
            
            eigenvals = eigenvalues(graph)
            mfr = minimal_rank(eigenvals)
            
            results.append({
                "n": n,
                "k": k,
                "mfr": mfr
            })
    
    total_instances = len(results)
    max_n = max(result["n"] for result in results)
    
    if max_n < 16:
        return {
            "metric_name": "minimal_rank",
            "metric_value": None,
            "instances_tested": total_instances,
            "n_max": max_n,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    ratios = [result["mfr"] / (result["n"] ** (result["k"] / 2)) for result in results]
    mean_ratio = sum(ratios) / len(ratios)
    std_ratio = math.sqrt(sum((r - mean_ratio) ** 2 for r in ratios) / len(ratios))
    
    support_count = sum(1 for r in ratios if abs(r - mean_ratio) <= 0.1 * (result["n"] ** (result["k"] / 2)))
    support_fraction = support_count / len(ratios)
    
    if support_fraction >= 0.8:
        return {
            "metric_name": "minimal_rank",
            "metric_value": mean_ratio,
            "instances_tested": total_instances,
            "n_max": max_n,
            "conjecture_holds": True,
            "counterexample": ""
        }
    else:
        for i, r in enumerate(ratios):
            if abs(r - mean_ratio) > 0.2 * (results[i]["n"] ** (results[i]["k"] / 2)):
                return {
                    "metric_name": "minimal_rank",
                    "metric_value": mean_ratio,
                    "instances_tested": total_instances,
                    "n_max": max_n,
                    "conjecture_holds": False,
                    "counterexample": f"n={results[i]['n']}, k={results[i]['k']}"
                }
    
    return {
        "metric_name": "minimal_rank",
        "metric_value": mean_ratio,
        "instances_tested": total_instances,
        "n_max": max_n,
        "conjecture_holds": False,
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"n_max\": {result['n_max']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    support_count = sum(1 for r in results if r["conjecture_holds"])
    
    if support_count >= 0.8 * len(results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_count / len(results)}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"n_max too small\" first_failing_seed={first_failing_seed}")