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
    
    def generate_3cnf(n):
        clauses = []
        for _ in range(2 * n):
            literals = [random.choice([1, -1]) * (i + 1) for i in range(n)]
            clause = random.sample(literals, 3)
            clauses.append(clause)
        return clauses
    
    def tseitin_graph(clauses):
        n = len(clauses)
        variables = set()
        edges = []
        
        for i in range(n):
            x = i + 1
            y = n + i + 1
            z = 2 * n + i + 1
            variables.add(x)
            variables.add(y)
            variables.add(z)
            
            edges.append((x, y))
            edges.append((y, z))
            edges.append((z, x))
            
            for literal in clauses[i]:
                if literal > 0:
                    edges.append((literal, y))
                    edges.append((literal, z))
                else:
                    edges.append((-literal, x))
        
        return variables, edges
    
    def adjacency_matrix(variables, edges):
        n = len(variables)
        adj_matrix = [[0] * n for _ in range(n)]
        
        for u, v in edges:
            i = abs(u) - 1
            j = abs(v) - 1
            if u > 0 and v > 0:
                adj_matrix[i][j] += 1
                adj_matrix[j][i] += 1
            elif u < 0 and v < 0:
                adj_matrix[i][j] -= 1
                adj_matrix[j][i] -= 1
        
        return adj_matrix
    
    def eigenvalues(matrix):
        n = len(matrix)
        if n == 0:
            return []
        
        # Gaussian elimination to find the determinant (eigenvalue)
        det = 1.0
        for i in range(n):
            pivot = matrix[i][i]
            if pivot == 0:
                continue
            for j in range(i + 1, n):
                factor = matrix[j][i] / pivot
                for k in range(i, n):
                    matrix[j][k] -= factor * matrix[i][k]
        
        for i in range(n):
            det *= matrix[i][i]
        
        return [det]
    
    def spectral_gap(eigenvalues):
        if not eigenvalues:
            return 0
        lambda_min = min(eigenvalues)
        return abs(lambda_min - 0.5)
    
    n_values = [20, 30, 40]
    results = []
    
    for n in n_values:
        phi = generate_3cnf(n)
        variables, edges = tseitin_graph(phi)
        adj_matrix = adjacency_matrix(variables, edges)
        lambda_min = spectral_gap(eigenvalues(adj_matrix))
        results.append({
            "n": n,
            "lambda_min": lambda_min
        })
    
    if not results:
        return {
            "metric_name": "spectral_gap",
            "metric_value": 0.0,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    lambda_min_values = [result["lambda_min"] for result in results]
    n_values = [result["n"] for result in results]
    
    C = 10
    max_lambda_diff = max([abs(l - 0.5) / n for l, n in zip(lambda_min_values, n_values)])
    
    return {
        "metric_name": "spectral_gap",
        "metric_value": max_lambda_diff,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": max_lambda_diff <= C / max(n_values),
        "counterexample": "" if max_lambda_diff <= C / max(n_values) else f"max_lambda_diff={max_lambda_diff} > {C}/{max(n_values)}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, **{trial_result}}}")
        results.append(trial_result)
    
    if all(result["conjecture_holds"] for result in results):
        mean_value = sum(result["metric_value"] for result in results) / len(results)
        std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
        support_fraction = len([result for result in results if result["conjecture_holds"]]) / len(results)
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(result["counterexample"] == "mapping_undefined" for result in results):
        print("RESULT: INCONCLUSIVE mapping_undefined")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")