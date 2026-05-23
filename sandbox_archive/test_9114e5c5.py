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

def gaussian_elimination(A):
    n = len(A)
    for i in range(n):
        # Find pivot
        max_row = i
        for k in range(i+1, n):
            if abs(A[k][i]) > abs(A[max_row][i]):
                max_row = k
        A[i], A[max_row] = A[max_row], A[i]
        
        # Eliminate below
        factor = Fraction(A[i][i])
        for k in range(i+1, n):
            A[k][i] /= factor
        
        # Eliminate above
        for k in range(i):
            factor = Fraction(A[k][i])
            for j in range(n):
                A[k][j] -= factor * A[i][j]
    return A

def coxeter_matrix_invariant(G):
    n = len(G)
    M = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i, n):
            if G[i][j] != 0:
                M[i][j] = G[i][j]
                M[j][i] = G[i][j]
    
    # Ensure the matrix is symmetric
    for i in range(n):
        for j in range(i+1, n):
            M[j][i] = M[i][j]
    
    # Perform Gaussian elimination to get the invariant
    M = gaussian_elimination(M)
    
    # Calculate the determinant (invariant)
    det = 1
    for i in range(n):
        det *= M[i][i]
    
    return abs(det)

def read_twice_bp_instance(n):
    # Generate a random read-twice branching program instance
    bp = []
    for _ in range(n):
        bp.append(random.choice([0, 1]))
    return bp

def compute_coxeter_group(bp):
    n = len(bp)
    G = [[0] * n for _ in range(n)]
    
    # Compute the Coxeter group matrix
    for i in range(n):
        for j in range(i+1, n):
            if bp[i] != bp[j]:
                G[i][j] = 2
                G[j][i] = 2
    
    return G

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    metric_name = "Coxeter Matrix Invariant vs BP_ReadTwice Circuit Size"
    instances_tested = 0
    total_rho_G = 0.0
    max_rho_G = 0.0
    
    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):
            bp = read_twice_bp_instance(n)
            G = compute_coxeter_group(bp)
            rho_G = coxeter_matrix_invariant(G)
            
            if rho_G > max_rho_G:
                max_rho_G = rho_G
            
            total_rho_G += math.log(n) * rho_G
            instances_tested += 1
    
    mean_rho_G = total_rho_G / instances_tested
    conjecture_holds = mean_rho_G >= 0.7 and max_rho_G <= 10 * math.log(40)
    
    return {
        "metric_name": metric_name,
        "metric_value": mean_rho_G,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"max_rho_G={max_rho_G} > 10 * log(40)"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or list(range(2, 30*31, 2))  # Default to first 30 primes
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(r["counterexample"] != "" for r in results):
        first_failing_seed = next((r["seed"] for r in results if r["counterexample"] != ""), None)
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction}")