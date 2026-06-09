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
    
    def generate_cnf(n, c):
        clauses = []
        for _ in range(c):
            clause = set()
            while len(clause) < 3:
                var = random.randint(1, n)
                if var not in clause:
                    clause.add(var)
            clauses.append(tuple(sorted(clause)))
        return clauses
    
    def adjacency_matrix(n, clauses):
        A = [[0] * n for _ in range(n)]
        for clause in clauses:
            for i in range(len(clause)):
                for j in range(i + 1, len(clause)):
                    A[clause[i] - 1][clause[j] - 1] = 1
                    A[clause[j] - 1][clause[i] - 1] = 1
        return A
    
    def geometric_entropy(matrix):
        n = len(matrix)
        if n == 0:
            return 0.0
        
        # Compute the eigenvalues of the adjacency matrix
        eigvals = []
        for i in range(n):
            v = [0] * n
            v[i] = 1
            v_norm = sum(x**2 for x in v)**0.5
            v = [x / v_norm for x in v]
            
            max_eigval = -float('inf')
            for j in range(n):
                dot_product = sum(matrix[i][k] * v[k] for k in range(n))
                if abs(dot_product) > max_eigval:
                    max_eigval = abs(dot_product)
            
            eigvals.append(max_eigval)
        
        # Compute the geometric entropy
        H_min = -sum(math.log(eigval) / n for eigval in eigvals if eigval != 0)
        return H_min
    
    def correlation_coefficient(x, y):
        mean_x = sum(x) / len(x)
        mean_y = sum(y) / len(y)
        cov = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(len(x))) / len(x)
        std_x = math.sqrt(sum((x[i] - mean_x)**2 for i in range(len(x))) / len(x))
        std_y = math.sqrt(sum((y[i] - mean_y)**2 for i in range(len(y))) / len(y))
        return cov / (std_x * std_y)
    
    n_max = 40
    instances_tested = 0
    H_min_values = []
    c_values = []
    
    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):  # Ensure at least 30 instances per seed
            clauses = generate_cnf(n, random.randint(2 * n, 3 * n))
            adj_matrix = adjacency_matrix(n, clauses)
            H_min = geometric_entropy(adj_matrix)
            if H_min is not None:
                H_min_values.append(H_min)
                c_values.append(len(clauses))
                instances_tested += 1
    
    if instances_tested < 30:
        return {
            "metric_name": "geometric_entropy",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "insufficient_instances"
        }
    
    r = correlation_coefficient(H_min_values, c_values)
    return {
        "metric_name": "geometric_entropy",
        "metric_value": r,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": r >= 0.9,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_r = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_r = (sum((r["metric_value"] - mean_r)**2 for r in results if r["metric_value"] is not None) / len(results))**0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_r} std={std_r} support_fraction={support_fraction}")
    elif support_fraction >= 0.95:
        print(f"RESULT: SUPPORTED mean={mean_r} std={std_r} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient < 0.9\" first_failing_seed={first_failing_seed}")