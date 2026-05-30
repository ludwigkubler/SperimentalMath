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
C = 10
N_MIN = 20
N_MAX = 40
SEEDS = [random.randint(1, 1000) for _ in range(30)]

def adjacency_matrix(n, clauses):
    vertices = set()
    adj_matrix = [[0] * (n + len(clauses)) for _ in range(n + len(clauses))]
    
    # Add edges for variables
    for i in range(n):
        vertices.add(f'x{i}')
        vertices.add(f'y{i}')
        adj_matrix[i][i] = 1
    
    # Add edges for clauses
    for j, clause in enumerate(clauses):
        for var in clause:
            if var.startswith('x'):
                u = var
                v = f'y{j}'
            else:
                u = f'x{int(var[1:])}'
                v = f'y{j}'
            
            vertices.add(u)
            vertices.add(v)
            adj_matrix[list(vertices).index(u)][list(vertices).index(v)] = 1
            adj_matrix[list(vertices).index(v)][list(vertices).index(u)] = 1
    
    return adj_matrix, vertices

def smallest_eigenvalue(adj_matrix):
    n = len(adj_matrix)
    eigenvalues = []
    
    # Compute eigenvalues using power iteration method
    for _ in range(100):  # Number of iterations
        v = [random.random() for _ in range(n)]
        v /= sum(v)  # Normalize
        
        Av = [sum(adj_matrix[i][j] * v[j] for j in range(n)) for i in range(n)]
        lambda_ = sum(Av[i] * v[i] for i in range(n))
        
        eigenvalues.append(lambda_)
    
    return min(eigenvalues)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [20, 30, 40]
    results = []
    
    for n in n_values:
        clauses = []
        for _ in range(n):
            clause = random.sample(['x' + str(i), 'y' + str(i)], 2) + ['z' + str(random.randint(1, n))]
            clauses.append(clause)
        
        adj_matrix, vertices = adjacency_matrix(n, clauses)
        lambda_min = smallest_eigenvalue(adj_matrix)
        value = abs(lambda_min - Fraction(1, 2))
        
        results.append({
            "n": n,
            "lambda_min": lambda_min,
            "value": value
        })
    
    mean_value = sum(result["value"] for result in results) / len(results)
    conjecture_holds = all(value <= C/n for result in results for n in n_values if n >= N_MIN and n <= N_MAX)
    counterexample = "" if conjecture_holds else "lambda_min does not satisfy the bound"
    
    return {
        "metric_name": "Spectral Gap",
        "metric_value": mean_value,
        "instances_tested": len(results),
        "n_max": max(result["n"] for result in results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else SEEDS
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"lambda_min does not satisfy the bound\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")