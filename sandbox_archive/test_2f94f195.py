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
    return abs(a * b) // gcd(a, b)

def matrix_multiply(A, B):
    m, n, p = len(A), len(B), len(B[0])
    C = [[0 for _ in range(p)] for _ in range(m)]
    for i in range(m):
        for j in range(p):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

def matrix_power(A, n):
    result = [[1 if i == j else 0 for j in range(len(A))] for i in range(len(A))]
    while n > 0:
        if n % 2 == 1:
            result = matrix_multiply(result, A)
        A = matrix_multiply(A, A)
        n //= 2
    return result

def determinant(matrix):
    n = len(matrix)
    if n == 1:
        return matrix[0][0]
    det = 0
    for j in range(n):
        submatrix = [row[:j] + row[j+1:] for row in matrix[1:]]
        det += ((-1) ** j) * matrix[0][j] * determinant(submatrix)
    return det

def permanent(matrix):
    n = len(matrix)
    if n == 1:
        return matrix[0][0]
    perm = 0
    for j in range(n):
        submatrix = [row[:j] + row[j+1:] for row in matrix[1:]]
        perm += ((-1) ** j) * matrix[0][j] * permanent(submatrix)
    return perm

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        det_orbit_invariants = set()
        perm_orbit_invariants = set()
        
        # Generate random matrices and compute determinants/permanents
        for _ in range(100):
            A = [[random.randint(-10, 10) for _ in range(n)] for _ in range(n)]
            det = determinant(A)
            perm = permanent(A)
            
            # Check if the determinant or permanent is zero
            if det == 0:
                det_orbit_invariants.add(0)
            else:
                det_orbit_invariants.add(det)
            
            if perm == 0:
                perm_orbit_invariants.add(0)
            else:
                perm_orbit_invariants.add(perm)
        
        # Count the number of unique invariants
        det_num_invariants = len(det_orbit_invariants)
        perm_num_invariants = len(perm_orbit_invariants)
        
        results.append({
            "n": n,
            "det_num_invariants": det_num_invariants,
            "perm_num_invariants": perm_num_invariants
        })
    
    metric_name = "Number of Invariant Polynomials"
    metric_value = sum(result["det_num_invariants"] for result in results) / len(results)
    instances_tested = len(results) * 100
    conjecture_holds = all(result["det_num_invariants"] < result["perm_num_invariants"] for result in results)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
    
    det_num_invariants = sum(result["det_num_invariants"] for result in results) / len(results)
    perm_num_invariants = sum(result["perm_num_invariants"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["det_num_invariants"] < result["perm_num_invariants"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={det_num_invariants} std={math.sqrt(sum((result['det_num_invariants'] - det_num_invariants) ** 2 for result in results) / len(results))} support_fraction={support_fraction}")
    elif any(result["det_num_invariants"] >= result["perm_num_invariants"] for result in results):
        first_failing_seed = next(seed for seed, result in enumerate(results) if result["det_num_invariants"] >= result["perm_num_invariants"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")