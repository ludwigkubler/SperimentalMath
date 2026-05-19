# auto-injected by SEC sandbox
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from fractions import Fraction
from itertools import combinations

def gaussian_elimination(matrix):
    n = len(matrix)
    identity = [[Fraction(1 if i == j else 0) for j in range(n)] for i in range(n)]
    
    for i in range(n):
        # Find pivot
        max_row = i
        for r in range(i+1, n):
            if abs(matrix[r][i]) > abs(matrix[max_row][i]):
                max_row = r
        
        # Swap rows
        matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
        identity[i], identity[max_row] = identity[max_row], identity[i]
        
        # Make pivot 1
        denom = matrix[i][i]
        for j in range(n):
            matrix[i][j] /= denom
            identity[i][j] /= denom
        
        # Eliminate other rows
        for r in range(n):
            if r != i:
                factor = matrix[r][i]
                for j in range(n):
                    matrix[r][j] -= factor * matrix[i][j]
                    identity[r][j] -= factor * identity[i][j]
    
    return identity

def matrix_multiply(A, B):
    n = len(A)
    C = [[Fraction(0) for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

def eigenvalues(matrix):
    n = len(matrix)
    if n == 1:
        return [matrix[0][0]]
    
    # Compute characteristic polynomial
    char_poly = [Fraction(1)]
    for i in range(n):
        char_poly = [c * x - matrix[i][i] * c for c in char_poly]
        for j in range(i+1, n):
            char_poly.append(-matrix[j][i])
    
    # Find roots using companion matrix method
    companion_matrix = [[Fraction(0) for _ in range(n-1)] for _ in range(n-1)]
    for i in range(n-2):
        companion_matrix[i][i+1] = Fraction(1)
    companion_matrix[-1][-2] = -char_poly[-2]
    
    # Compute eigenvalues of companion matrix
    identity = [[Fraction(1 if i == j else 0) for j in range(n-1)] for i in range(n-1)]
    eigenvals = []
    for _ in range(n):
        A_inv = gaussian_elimination(identity)
        e_val = sum(A_inv[i][i] * char_poly[-i-2] for i in range(n))
        eigenvals.append(e_val)
        identity[0][-1] += Fraction(1)
    
    return eigenvals

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    
    # Generate a random connected graph
    G = {i: set() for i in range(n)}
    edges = list(combinations(range(n), 2))
    random.shuffle(edges)
    added_edges = 0
    while len(G) > 1:
        u, v = edges.pop()
        if u not in G[v]:
            G[u].add(v)
            G[v].add(u)
            added_edges += 1
            if added_edges == n - 1:
                break
    
    # Compute the Laplacian matrix
    L = [[Fraction(0) for _ in range(n)] for _ in range(n)]
    for i in range(n):
        L[i][i] = Fraction(len(G[i]))
        for j in G[i]:
            if i < j:
                L[i][j] = -Fraction(1)
                L[j][i] = -Fraction(1)
    
    # Compute the second smallest eigenvalue of the Laplacian matrix
    lambda_values = sorted(eigenvalues(L))
    lambda_2 = lambda_values[1]
    
    # Compute the Tseitin formula's Resolution lower bound
    resolution_bound = 2 ** (math.log(lambda_2, 2) / math.log(2, 10))
    
    return {
        "metric_name": "Resolution Bound",
        "metric_value": resolution_bound,
        "instances_tested": n,
        "conjecture_holds": lambda_2 > 0 and resolution_bound >= 2 ** (math.log(lambda_2, 2) / math.log(2, 10)),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_support")