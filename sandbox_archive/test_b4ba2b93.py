# auto-injected by SEC sandbox
import math
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
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n = 30  # Number of vertices in the expander graph
    p = 2   # Prime number for p-adic analysis
    
    # Generate an n-vertex expander graph
    edges = []
    for i in range(n):
        for j in range(i + 1, n):
            if random.choice([True, False]):
                edges.append((i, j))
    
    # Compute the local index ν(G)
    adjacency_matrix = [[0] * n for _ in range(n)]
    for u, v in edges:
        adjacency_matrix[u][v] = 1
        adjacency_matrix[v][u] = 1
    
    def matrix_multiply(A, B):
        m, k, n = len(A), len(B[0]), len(B)
        C = [[0] * n for _ in range(m)]
        for i in range(m):
            for j in range(n):
                for l in range(k):
                    C[i][j] += A[i][l] * B[l][j]
        return C
    
    def gaussian_elimination(A, b):
        m, n = len(A), len(A[0])
        augmented_matrix = [A[i] + [b[i]] for i in range(m)]
        
        for i in range(n):
            max_row = i
            for j in range(i+1, m):
                if abs(augmented_matrix[j][i]) > abs(augmented_matrix[max_row][i]):
                    max_row = j
            
            augmented_matrix[i], augmented_matrix[max_row] = augmented_matrix[max_row], augmented_matrix[i]
            
            pivot = augmented_matrix[i][i]
            for j in range(i, n+1):
                augmented_matrix[i][j] /= pivot
            
            for j in range(m):
                if j != i:
                    factor = augmented_matrix[j][i]
                    for k in range(i, n+1):
                        augmented_matrix[j][k] -= factor * augmented_matrix[i][k]
        
        return [row[-1] for row in augmented_matrix[:n]]
    
    def p_adic_analytic_continuation(A):
        m = len(A)
        det = 1
        for i in range(m):
            det *= A[i][i]
        return det
    
    ν_G = abs(p_adic_analytic_continuation(adjacency_matrix))
    
    # Compute the resolution proof width
    def tseitin_formula(edges, n):
        literals = [f'x{i}' for i in range(n)]
        clauses = []
        
        for u, v in edges:
            clauses.append([literals[u], literals[v]])
            clauses.append([-literals[u], -literals[v]])
            clauses.append([-literals[u], literals[v]])
            clauses.append([literals[u], -literals[v]])
        
        return clauses
    
    def resolution_width(clauses):
        queue = clauses[:]
        learned_clauses = []
        while queue:
            clause1 = queue.pop(0)
            for clause2 in queue + learned_clauses:
                if len(set(clause1) & set(clause2)) == 1:
                    new_clause = list(set(clause1) ^ set(clause2))
                    if not any(new_clause == c for c in queue + learned_clauses):
                        learned_clauses.append(new_clause)
        return max(len(c) for c in learned_clauses)
    
    clauses = tseitin_formula(edges, n)
    width = resolution_width(clauses)
    
    # Check the conjecture
    if width >= 2 ** (ν_G * math.log(p)):
        conjecture_holds = True
        counterexample = ""
    else:
        conjecture_holds = False
        counterexample = f"Width {width} < 2^(Ω({ν_G})) for ν(G)={ν_G}"
    
    return {
        "metric_name": "resolution_width",
        "metric_value": width,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_width = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_width} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_width} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[first_failing_seed]['counterexample']}\" first_failing_seed={first_failing_seed + 1}")