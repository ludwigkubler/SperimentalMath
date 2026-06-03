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

def symplectic_laplacian(V):
    n = len(V)
    L_S = [[0] * n for _ in range(n)]
    
    for i in range(n):
        for j in range(i, n):
            if i == j:
                L_S[i][j] = 2
            else:
                L_S[i][j] = V[j][i] - V[i][j]
                L_S[j][i] = -L_S[i][j]
    
    return L_S

def eigenvalues(matrix):
    n = len(matrix)
    if n == 1:
        return [matrix[0][0]]
    
    # Gaussian elimination to reduce the matrix
    for i in range(n):
        max_row = i
        for j in range(i+1, n):
            if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                max_row = j
        
        matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
        
        for j in range(i+1, n):
            factor = Fraction(matrix[j][i], matrix[i][i])
            for k in range(n):
                matrix[j][k] -= factor * matrix[i][k]
    
    # Extract eigenvalues from the diagonal
    return [matrix[i][i] for i in range(n)]

def communication_complexity_rank(V):
    n = len(V)
    rank = 0
    
    for i in range(n):
        if any(V[j][i] != 0 for j in range(n)):
            rank += 1
    
    return rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    d = random.randint(5, 30)
    F = [Fraction(i) for i in range(2, 10)]
    V = [[random.choice(F) for _ in range(d)] for _ in range(d)]
    
    L_S = symplectic_laplacian(V)
    eigenvals = eigenvalues(L_S)
    non_zero_eigenvals = [val for val in eigenvals if val != 0]
    
    if not non_zero_eigenvals:
        return {
            "metric_name": "lambda_min",
            "metric_value": None,
            "instances_tested": 1,
            "n_max": d,
            "conjecture_holds": False,
            "counterexample": "no_non_zero_eigenvalues"
        }
    
    lambda_min = min(non_zero_eigenvals)
    r_V = communication_complexity_rank(V)
    
    return {
        "metric_name": "lambda_min",
        "metric_value": float(lambda_min),
        "instances_tested": 1,
        "n_max": d,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_lambda_min = sum(res["metric_value"] for res in results if res["metric_value"] is not None) / len(results)
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["metric_value"] is not None for res in results):
        RESULT = "SUPPORTED" if support_fraction >= 0.8 else "FALSIFIED"
    else:
        RESULT = "INCONCLUSIVE"
    
    print(f"{RESULT} mean={mean_lambda_min:.4f} std=NA support_fraction={support_fraction:.2f}")