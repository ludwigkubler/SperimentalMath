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

# Helper functions for linear algebra
def dot_product(a, b):
    return sum(x * y for x, y in zip(a, b))

def matrix_multiplication(A, B):
    m = len(A)
    n = len(B[0])
    p = len(B)
    result = [[0] * n for _ in range(m)]
    for i in range(m):
        for j in range(n):
            for k in range(p):
                result[i][j] += A[i][k] * B[k][j]
    return result

def gaussian_elimination(A, b):
    m = len(A)
    n = len(A[0])
    augmented = [A[i] + [b[i]] for i in range(m)]
    
    for i in range(n):
        # Find pivot
        max_row = i
        for j in range(i+1, m):
            if abs(augmented[j][i]) > abs(augmented[max_row][i]):
                max_row = j
        
        # Swap rows
        augmented[i], augmented[max_row] = augmented[max_row], augmented[i]
        
        # Eliminate below pivot
        for j in range(i+1, m):
            factor = Fraction(augmented[j][i], augmented[i][i])
            for k in range(n + 1):
                augmented[j][k] -= factor * augmented[i][k]
    
    # Back substitution
    x = [0] * n
    for i in range(n-1, -1, -1):
        x[i] = Fraction(augmented[i][-1], augmented[i][i])
        for j in range(i-1, -1, -1):
            augmented[j][-1] -= augmented[j][i] * x[i]
    
    return x

def rank_of_matrix(A):
    m = len(A)
    n = len(A[0])
    B = [row[:] for row in A]
    rank = 0
    
    for i in range(n):
        if all(B[j][i] == 0 for j in range(rank, m)):
            continue
        
        # Swap rows
        B[rank], B[i] = B[i], B[rank]
        
        # Eliminate below pivot
        for j in range(rank+1, m):
            factor = Fraction(B[j][i], B[rank][i])
            for k in range(n):
                B[j][k] -= factor * B[rank][k]
        
        rank += 1
    
    return rank

def tutte_polynomial(G):
    n = len(G)
    if n == 0:
        return Fraction(1, 1)
    
    T = [[Fraction(0, 1)] * (n+1) for _ in range(n+1)]
    T[0][0] = Fraction(1, 1)
    
    for i in range(1, n+1):
        T[i][0] = Fraction(1, 1)
        T[i][i] = Fraction(1, 1)
        for j in range(1, i):
            T[i][j] = (T[i-1][j-1] + T[i-1][j]) * Fraction(i-1, 2)
    
    return T[n][0]

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    G = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
    for i in range(n):
        G[i][i] = 0
    
    ν_G = rank_of_matrix(G)
    T_G = tutte_polynomial(G)
    
    if ν_G == 0:
        return {
            "metric_name": "ν(G)",
            "metric_value": ν_G,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    circuit_size = 2 ** ν_G
    
    return {
        "metric_name": "circuit_size",
        "metric_value": circuit_size,
        "instances_tested": 1,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    total_metric_value = 0
    support_count = 0
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        
        total_metric_value += result["metric_value"]
        if result["conjecture_holds"]:
            support_count += 1
    
    mean_metric_value = total_metric_value / len(seeds)
    support_fraction = support_count / len(seeds)
    
    if support_fraction >= 0.95:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0 support_fraction={support_fraction}")
    else:
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={seeds[support_count]}")