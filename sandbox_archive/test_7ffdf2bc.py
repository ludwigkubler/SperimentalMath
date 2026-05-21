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
    
    n = 40
    d = math.ceil(math.log(n))
    
    # Generate a random 3-CNF instance with n variables and m clauses
    m = 2 * n
    clauses = []
    for _ in range(m):
        literals = [random.choice([-1, 1]) * (i + 1) for i in range(3)]
        clause = tuple(sorted(literals))
        if clause not in clauses:
            clauses.append(clause)
    
    # Construct the degree-d moment matrix
    moment_matrix = [[0] * (n + 1) for _ in range(n + 1)]
    for clause in clauses:
        for literal in clause:
            var_index = abs(literal) - 1
            if literal > 0:
                moment_matrix[var_index][var_index] += 1
            else:
                moment_matrix[0][var_index] += 1
                moment_matrix[var_index][0] += 1
    
    # Compute eigenvalues using power iteration
    def matrix_multiply(A, B):
        result = [[0] * len(B[0]) for _ in range(len(A))]
        for i in range(len(A)):
            for j in range(len(B[0])):
                for k in range(len(B)):
                    result[i][j] += A[i][k] * B[k][j]
        return result
    
    def power_iteration(matrix, max_iter=100):
        v = [1] * (n + 1)
        v_norm = math.sqrt(sum(x**2 for x in v))
        v = [x / v_norm for x in v]
        
        for _ in range(max_iter):
            v_new = matrix_multiply(matrix, v)
            v_new_norm = math.sqrt(sum(x**2 for x in v_new))
            if abs(v_new_norm - v_norm) < 1e-6:
                break
            v = [x / v_new_norm for x in v_new]
            v_norm = v_new_norm
        
        return v
    
    eigenvector = power_iteration(moment_matrix)
    
    # Compute eigenvalues using numpy (for verification)
    import numpy as np
    eigenvalues, _ = np.linalg.eig(np.array(moment_matrix))
    
    lambda_min = min(eigenvalues.real)
    gamma = max(eigenvalues.real) - lambda_min
    
    conjecture_holds = lambda_min >= 1 / math.sqrt(n) and gamma >= 1 / n
    counterexample = "" if conjecture_holds else "lambda_min < 1/√n or gamma < 1/n"
    
    return {
        "metric_name": "Moment Matrix Spectral Gap",
        "metric_value": gamma,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_gamma = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_gamma} std=NA support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"lambda_min < 1/√n or gamma < 1/n\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")