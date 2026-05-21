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
    
    def generate_max_cut_instance(n):
        edges = set()
        for i in range(n):
            for j in range(i + 1, n):
                if random.random() < 0.5:
                    edges.add((i, j))
        return edges
    
    def degree_matrix(edges, n):
        D = [[0] * n for _ in range(n)]
        for u, v in edges:
            D[u][v] += 1
            D[v][u] += 1
        return D
    
    def laplacian_matrix(D):
        L = [[0] * len(D) for _ in range(len(D))]
        for i in range(len(D)):
            L[i][i] = sum(D[i])
            for j in range(i + 1, len(D)):
                L[i][j] = -D[i][j]
                L[j][i] = -D[j][i]
        return L
    
    def eigenvalues(matrix):
        n = len(matrix)
        if n == 0:
            return []
        if n == 1:
            return [matrix[0][0]]
        
        # Gaussian elimination to reduce the matrix
        for i in range(n):
            max_row = max(range(i, n), key=lambda r: abs(matrix[r][i]))
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
            
            factor = 1 / matrix[i][i]
            for j in range(n):
                matrix[i][j] *= factor
            
            for k in range(n):
                if k != i:
                    factor = matrix[k][i]
                    for j in range(n):
                        matrix[k][j] -= factor * matrix[i][j]
        
        # Extract eigenvalues from the diagonal
        return [matrix[i][i] for i in range(n)]
    
    def sos_moment_matrix(edges, n, d):
        D = degree_matrix(edges, n)
        L = laplacian_matrix(D)
        M_d = [[0] * n for _ in range(n)]
        
        for u in range(n):
            for v in range(u + 1, n):
                if (u, v) in edges:
                    M_d[u][v] += D[u][v]
                    M_d[v][u] += D[v][u]
        
        # Compute the d-th power of L
        L_d = [[0] * n for _ in range(n)]
        for i in range(n):
            L_d[i][i] = 1
        
        for _ in range(d - 1):
            L_d_next = [[0] * n for _ in range(n)]
            for i in range(n):
                for j in range(n):
                    for k in range(n):
                        L_d_next[i][j] += L_d[i][k] * L[k][j]
            L_d = L_d_next
        
        return M_d
    
    def integrality_gap(edges, n):
        cut_value = 0
        for u, v in edges:
            if random.choice([True, False]):
                cut_value += 1
        return (2 * cut_value - n) / n
    
    n = random.randint(5, 40)
    edges = generate_max_cut_instance(n)
    
    gap = integrality_gap(edges, n)
    lambda_min = float('inf')
    
    for d in [2, 3, 4]:
        M_d = sos_moment_matrix(edges, n, d)
        eigenvals = eigenvalues(M_d)
        lambda_min = min(lambda_min, min(eigenvals))
    
    if gap > 0.878:
        conjecture_holds = False
        counterexample = f"Integrality gap {gap} exceeds 0.878"
    elif lambda_min >= 1 - gap:
        conjecture_holds = True
        counterexample = ""
    else:
        conjecture_holds = False
        counterexample = f"Eigenvalue {lambda_min} < 1 - gap ({1 - gap})"
    
    return {
        "metric_name": "Integrality Gap",
        "metric_value": gap,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2**i - 1 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_gap = sum(r["metric_value"] for r in results) / len(results)
    std_gap = math.sqrt(sum((r["metric_value"] - mean_gap)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_gap} std={std_gap} support_fraction={support_fraction}")
    elif any(r["counterexample"] for r in results):
        first_failing_seed = next((r["seed"] for r in results if r["counterexample"]), None)
        counterexample_desc = next((r["counterexample"] for r in results if r["counterexample"]), "")
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample_desc}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")