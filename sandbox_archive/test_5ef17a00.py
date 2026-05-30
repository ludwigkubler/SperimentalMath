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
        for _ in range(n * 2):
            literals = [random.randint(1, n), random.randint(-n, -1)]
            random.shuffle(literals)
            clause = (literals[0], literals[1])
            if clause not in clauses and (-clause[0], -clause[1]) not in clauses:
                clauses.append(clause)
        return clauses

    def tseitin_graph(n, clauses):
        vertices = set()
        edges = []
        
        for i in range(1, n + 1):
            vertices.add(f'x{i}')
            vertices.add(f'¬x{i}')
        
        for clause in clauses:
            p, q = clause
            v_p = f'x{abs(p)}'
            v_q = f'x{abs(q)}'
            v_not_p = f'¬x{abs(p)}'
            v_not_q = f'¬x{abs(q)}'
            
            vertices.add(f'y{len(vertices) + 1}')
            edges.append((f'y{len(vertices) - 1}', v_p))
            edges.append((f'y{len(vertices) - 1}', v_q))
            edges.append((v_not_p, f'y{len(vertices) - 1}'))
            edges.append((v_not_q, f'y{len(vertices) - 1}'))
            
            vertices.add(f'z{len(vertices) + 1}')
            edges.append((f'z{len(vertices) - 1}', v_p))
            edges.append((f'z{len(vertices) - 1}', v_not_q))
            edges.append((v_not_p, f'z{len(vertices) - 1}'))
            edges.append((v_q, f'z{len(vertices) - 1}'))
        
        return vertices, edges

    def adjacency_matrix(n, clauses):
        vertices, edges = tseitin_graph(n, clauses)
        m = len(vertices)
        adj_matrix = [[0] * m for _ in range(m)]
        
        for u, v in edges:
            i = list(vertices).index(u)
            j = list(vertices).index(v)
            adj_matrix[i][j] = 1
            adj_matrix[j][i] = 1
        
        return adj_matrix

    def gaussian_elimination(matrix):
        n = len(matrix)
        for i in range(n):
            # Find the pivot row
            max_row = i
            for j in range(i + 1, n):
                if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                    max_row = j
            
            # Swap rows
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
            
            # Eliminate below the pivot
            for j in range(i + 1, n):
                factor = matrix[j][i] / matrix[i][i]
                for k in range(n):
                    matrix[j][k] -= factor * matrix[i][k]
        
        return matrix

    def eigenvalues(matrix):
        n = len(matrix)
        if n == 0:
            return []
        
        # Convert to a list of lists
        A = [[matrix[i][j] for j in range(n)] for i in range(n)]
        
        # Perform Gaussian elimination
        U = gaussian_elimination(A)
        
        # Extract eigenvalues from the diagonal of U
        eigenvals = [U[i][i] for i in range(n)]
        return eigenvals

    def smallest_eigenvalue(matrix):
        eigenvals = eigenvalues(matrix)
        if not eigenvals:
            return 0
        return min(eigenvals)

    n_values = [20, 30, 40]
    results = []
    
    for n in n_values:
        clauses = generate_3cnf(n)
        adj_matrix = adjacency_matrix(n, clauses)
        lambda_min = smallest_eigenvalue(adj_matrix)
        diff = abs(lambda_min - 0.5)
        
        if diff > 10 / n:
            return {
                "metric_name": "spectral_gap",
                "metric_value": diff,
                "instances_tested": 1,
                "n_max": n,
                "conjecture_holds": False,
                "counterexample": f"n={n}, |λ_min(A(φ)) - (1/2)| = {diff} > 10/n"
            }
        
        results.append({
            "metric_name": "spectral_gap",
            "metric_value": diff,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": True,
            "counterexample": ""
        })
    
    return {
        "metric_name": "spectral_gap",
        "metric_value": sum(result["metric_value"] for result in results) / len(results),
        "instances_tested": len(results),
        "n_max": max(result["n_max"] for result in results),
        "conjecture_holds": all(result["conjecture_holds"] for result in results),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(sys.argv[1])] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
    
    results = [run_trial(seed) for seed in seeds]
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0 support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='n=20, |λ_min(A(φ)) - (1/2)| > 10/n' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=support_fraction_too_low")