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
    m = 10 * n
    clauses = []
    for _ in range(m):
        literals = [random.choice([f'x{i}', f'-x{i}']) for i in range(1, n+1)]
        clause = random.sample(literals, 3)
        clauses.append(clause)
    
    # Construct the degree-d moment matrix
    moment_matrix = [[0] * (n + 1) for _ in range(n + 1)]
    for clause in clauses:
        for literal in clause:
            var = abs(int(literal[1:]))
            sign = -1 if literal.startswith('-') else 1
            moment_matrix[var][var] += sign**d
    
    # Compute eigenvalues using power iteration
    def power_iteration(matrix, max_iter=100):
        v = [random.random() for _ in range(n + 1)]
        v /= sum(v)
        for _ in range(max_iter):
            v_new = matrix_multiply(matrix, v)
            v_new /= sum(v_new)
            if abs(sum(v_new)) < 1e-10:
                break
            v = v_new
        return v
    
    def matrix_multiply(A, B):
        result = [[0] * len(B[0]) for _ in range(len(A))]
        for i in range(len(A)):
            for j in range(len(B[0])):
                for k in range(len(B)):
                    result[i][j] += A[i][k] * B[k][j]
        return result
    
    eigenvector = power_iteration(moment_matrix)
    eigenvalues = sorted(eigenvector, reverse=True)
    
    λ_min = eigenvalues[-1]
    γ = eigenvalues[0] - λ_min
    
    # Check the conjecture
    λ_min_threshold = 1 / math.sqrt(n)
    γ_threshold = 1 / n
    
    conjecture_holds = λ_min >= λ_min_threshold and γ >= γ_threshold
    counterexample = "" if conjecture_holds else f"λ_min={λ_min}, γ={γ}"
    
    return {
        "metric_name": "Spectral Gap",
        "metric_value": γ,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")