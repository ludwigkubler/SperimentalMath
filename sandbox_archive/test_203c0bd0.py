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
    
    def generate_max_cut_instance(n):
        edges = set()
        for i in range(n):
            for j in range(i + 1, n):
                if random.random() < 0.5:
                    edges.add((i, j))
        return edges
    
    def degree_matrix(edges, n):
        deg = [0] * n
        for u, v in edges:
            deg[u] += 1
            deg[v] += 1
        D = [[deg[i] if i == j else 0 for j in range(n)] for i in range(n)]
        return D
    
    def laplacian_matrix(D):
        n = len(D)
        L = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                if i == j:
                    L[i][j] = D[i][i]
                elif (i, j) in edges or (j, i) in edges:
                    L[i][j] = -D[i][j]
        return L
    
    def eigenvalues(matrix):
        n = len(matrix)
        if n == 1:
            return [matrix[0][0]]
        
        # Gaussian elimination to transform matrix into upper triangular
        for i in range(n):
            max_row = max(range(i, n), key=lambda x: abs(matrix[x][i]))
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
            
            for j in range(i + 1, n):
                factor = matrix[j][i] / matrix[i][i]
                for k in range(n):
                    matrix[j][k] -= factor * matrix[i][k]
        
        # Extract eigenvalues from the diagonal
        return [matrix[i][i] for i in range(n)]
    
    def sos_moment_matrix(edges, n, d):
        D = degree_matrix(edges, n)
        L = laplacian_matrix(D)
        M_d = [[0] * n for _ in range(n)]
        
        for k in range(d + 1):
            for u in range(n):
                for v in range(u, n):
                    if (u, v) in edges or (v, u) in edges:
                        M_d[u][v] += Fraction(1, 2 * d)
                        M_d[v][u] += Fraction(1, 2 * d)
        
        return M_d
    
    def min_eigenvalue(matrix):
        eigenvals = eigenvalues(matrix)
        return min(eigenvals)
    
    n = random.randint(5, 40)
    edges = generate_max_cut_instance(n)
    d_values = [2, 3, 4]
    lambda_min = float('inf')
    gap = 1.0
    
    for d in d_values:
        M_d = sos_moment_matrix(edges, n, d)
        lambda_min_d = min_eigenvalue(M_d)
        if lambda_min_d < lambda_min:
            lambda_min = lambda_min_d
        
        # Calculate integrality gap
        integrality_gap = 1 - (lambda_min_d / (n * (n - 1) / 2))
        if integrality_gap > gap:
            gap = integrality_gap
    
    epsilon = lambda_min
    conjecture_holds = gap <= 1 - epsilon and gap <= 0.878 + epsilon
    
    return {
        "metric_name": "Integrality Gap",
        "metric_value": gap,
        "instances_tested": len(d_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"Gap {gap} exceeds 1 - epsilon={1 - epsilon}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_gap = sum(r["metric_value"] for r in results) / len(results)
    std_gap = math.sqrt(sum((r["metric_value"] - mean_gap) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_gap} std={std_gap} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Gap exceeds 1 - epsilon\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")