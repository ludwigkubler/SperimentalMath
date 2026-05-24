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

def gaussian_elimination(A, b):
    n = len(A)
    m = len(b)
    augmented_matrix = [A[i] + [b[i]] for i in range(n)]
    
    # Forward elimination
    for i in range(n):
        if A[i][i] == 0:
            return None  # Singular matrix, no unique solution
        
        # Normalize the pivot row
        pivot = Fraction(augmented_matrix[i][i])
        augmented_matrix[i] = [Fraction(x) / pivot for x in augmented_matrix[i]]
        
        # Eliminate below the pivot
        for j in range(i + 1, n):
            factor = augmented_matrix[j][i]
            augmented_matrix[j] = [augmented_matrix[j][k] - factor * augmented_matrix[i][k] for k in range(n + m)]
    
    # Backward substitution
    x = [0] * n
    for i in range(n - 1, -1, -1):
        x[i] = augmented_matrix[i][-m]
        for j in range(i + 1, n):
            x[i] -= augmented_matrix[i][j] * x[j]
    
    return x

def rank(matrix):
    if not matrix:
        return 0
    
    m = len(matrix)
    n = len(matrix[0])
    A_rref = gaussian_elimination(matrix, [0]*m)
    
    if A_rref is None:
        return 0
    
    rank = 0
    for row in A_rref:
        if any(row):
            rank += 1
    
    return rank

def degree_of_smallest_xor_tautology(poly):
    n = len(poly)
    for i in range(1, 2**n):
        tautology = [bool(i & (1 << j)) for j in range(n)]
        if all(poly[j] == tautology[j] for j in range(n)):
            return sum(tautology)
    return n

def random_polynomial(n, degree):
    coefficients = [random.randint(0, 1) for _ in range(degree + 1)]
    return [coefficients[i] * (x**i) for i, x in enumerate(range(n))]

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_metric_value = 0
    instances_tested = 0
    
    for n in n_values:
        for _ in range(5):  # Test each n with 5 different polynomials
            poly = random_polynomial(n, degree=n-1)
            rho_f = rank([[poly[i] for i in range(j, j+degree_of_smallest_xor_tautology(poly)+1)] for j in range(n)])
            
            if rho_f is None:
                return {
                    "metric_name": "rank",
                    "metric_value": 0,
                    "instances_tested": instances_tested,
                    "conjecture_holds": False,
                    "counterexample": "singular_matrix"
                }
            
            degree_smallest_xor = degree_of_smallest_xor_tautology(poly)
            total_metric_value += rho_f
            instances_tested += 1
    
    mean_metric_value = total_metric_value / instances_tested
    return {
        "metric_name": "rank",
        "metric_value": mean_metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": mean_metric_value > degree_smallest_xor,
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
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0 support_fraction=1")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='degree_of_smallest_xor_tautology' first_failing_seed={first_failing_seed}")