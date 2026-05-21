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
    n = random.choice([5, 10, 15, 20, 30, 40])
    
    # Generate a read-twice branching program for IP_2 on n bits
    def generate_read_twice_bp(n):
        bp = []
        for i in range(2**n):
            if i == 0:
                bp.append([i])
            else:
                parent = random.choice(bp[i-1])
                bp.append([parent, parent ^ (1 << random.randint(0, n-1))])
        return bp
    
    def construct_transition_matrix(bp):
        m = [[0] * len(bp) for _ in range(len(bp))]
        for i, path in enumerate(bp):
            for j in range(len(path)):
                if j < len(path) - 1:
                    m[i][path[j+1]] += 1
        return m
    
    def max_singular_value(matrix):
        n = len(matrix)
        U, S, Vt = svd(matrix)
        return S[0]
    
    def svd(A):
        # Simple SVD implementation using power iteration method
        m, n = len(A), len(A[0])
        if m < n:
            A = transpose(A)
            m, n = n, m
        
        U = identity(m)
        Vt = identity(n)
        sigma = [sum(A[i][j]**2 for j in range(n))**0.5 for i in range(m)]
        
        for _ in range(100):
            Q = gram_schmidt([A[i] for i in range(m)])
            U = multiply(Q, U)
            
            R = transpose(U) @ A
            Q = gram_schmidt([R[j] for j in range(n)])
            Vt = multiply(Q, Vt)
            
            sigma = [sum(R[i][j]**2 for j in range(n))**0.5 for i in range(m)]
        
        return U, sigma, Vt
    
    def identity(size):
        return [[1 if i == j else 0 for j in range(size)] for i in range(size)]
    
    def transpose(matrix):
        return [[matrix[j][i] for j in range(len(matrix))] for i in range(len(matrix[0]))]
    
    def multiply(A, B):
        m, n = len(A), len(B[0])
        result = [[sum(A[i][k] * B[k][j] for k in range(len(B))) for j in range(n)] for i in range(m)]
        return result
    
    def gram_schmidt(vectors):
        u = [v[:] for v in vectors]
        for i in range(1, len(u)):
            for j in range(i):
                u[i] = subtract(u[i], scalar_multiply(dot_product(u[j], u[i]), u[j]))
            u[i] = normalize(u[i])
        return u
    
    def dot_product(v1, v2):
        return sum(x * y for x, y in zip(v1, v2))
    
    def subtract(v1, v2):
        return [x - y for x, y in zip(v1, v2)]
    
    def scalar_multiply(scalar, vector):
        return [scalar * x for x in vector]
    
    def normalize(vector):
        norm = sum(x**2 for x in vector)**0.5
        if norm == 0:
            raise ValueError("Cannot normalize zero vector")
        return [x / norm for x in vector]
    
    bp = generate_read_twice_bp(n)
    M_P = construct_transition_matrix(bp)
    max_sing_val = max_singular_value(M_P)
    
    metric_name = "max_singular_value"
    metric_value = max_sing_val
    instances_tested = 1
    conjecture_holds = max_sing_val >= n
    counterexample = "" if conjecture_holds else f"n={n}, max_sing_val={max_sing_val}"
    
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else list(range(2, 30*4 + 2, 2))
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = (sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))**0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        result = f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}"
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in enumerate(results) if not r["conjecture_holds"])
        result = f"RESULT: FALSIFIED counterexample=\"n={results[first_failing_seed]['instances_tested']}, max_sing_val={results[first_failing_seed]['metric_value']}\" first_failing_seed={first_failing_seed}"
    else:
        result = "RESULT: INCONCLUSIVE insufficient_data"
    
    print(result)