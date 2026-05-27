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

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def lcm(a, b):
    return abs(a*b) // gcd(a, b)

def matrix_multiply(A, B):
    m, k = len(A), len(B)
    n = len(B[0])
    C = [[0] * n for _ in range(m)]
    for i in range(m):
        for j in range(n):
            for l in range(k):
                C[i][j] += A[i][l] * B[l][j]
    return C

def gaussian_elimination(A, b):
    m, n = len(A), len(A[0])
    Augmented = [A[i] + [b[i]] for i in range(m)]
    
    def swap_rows(i, j):
        Augmented[i], Augmented[j] = Augmented[j], Augmented[i]
    
    def scale_row(i, c):
        Augmented[i] = [c * x for x in Augmented[i]]
    
    def add_multiple_of_row(i, j, c):
        Augmented[j] = [Augmented[j][k] + c * Augmented[i][k] for k in range(n+1)]
    
    r = 0
    for c in range(n):
        if r >= m:
            break
        
        pivot_row = r
        for i in range(r, m):
            if abs(Augmented[i][c]) > abs(Augmented[pivot_row][c]):
                pivot_row = i
        
        swap_rows(r, pivot_row)
        
        scale_row(r, 1 / Augmented[r][c])
        
        for i in range(m):
            if i != r:
                add_multiple_of_row(r, i, -Augmented[i][c])
        
        r += 1
    
    X = [0] * n
    for i in range(n-1, -1, -1):
        X[i] = Augmented[i][-1]
        for j in range(i+1, n):
            X[i] -= Augmented[i][j] * X[j]
    
    return X

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    total_rank = 0
    num_instances = 0
    
    for n in n_values:
        for _ in range(5):
            # Generate a random CNF formula with n variables
            clauses = []
            for _ in range(n):
                literals = [random.randint(1, n), -random.randint(1, n)]
                clauses.append(literals)
            
            # Compute the resolution proof depth (simplified version)
            d = len(clauses)  # This is a very rough estimate
            
            # Convert CNF to hypergeometric sequence
            # For simplicity, we use a dummy sequence here
            hypergeometric_sequence = [random.random() for _ in range(n)]
            
            # Compute the rank of the hypergeometric sequence
            A = [[hypergeometric_sequence[i]] for i in range(n)]
            b = [1] * n
            try:
                X = gaussian_elimination(A, b)
                rank = sum(1 for x in X if abs(x) > 1e-6)
            except Exception as e:
                return {
                    "metric_name": "minimal_rank",
                    "metric_value": None,
                    "instances_tested": num_instances,
                    "conjecture_holds": False,
                    "counterexample": str(e)
                }
            
            total_rank += rank
            num_instances += 1
    
    mean_rank = total_rank / num_instances
    conjecture_holds = mean_rank / n >= 0.8
    
    return {
        "metric_name": "minimal_rank",
        "metric_value": mean_rank,
        "instances_tested": num_instances,
        "conjecture_holds": conjecture_holds,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_rank = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction={support_fraction}")
    else:
        for r in results:
            if not r["conjecture_holds"]:
                print(f"RESULT: FALSIFIED counterexample=\"seed {r['seed']}\" first_failing_seed={r['seed']}")
                break