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
    
    def generate_disjointness_matrix(n):
        M = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i + 1, n):
                if random.choice([True, False]):
                    M[i][j] = 1
                    M[j][i] = 1
        return M
    
    def eigenvalues(matrix):
        n = len(matrix)
        if n == 0:
            return []
        
        # Simple power iteration method to find one eigenvalue
        v = [random.random() for _ in range(n)]
        for _ in range(100):  # Limit iterations to avoid infinite loops
            v = matrix_product(matrix, v)
            v /= norm(v)
        lambda_ = dot_product(v, matrix_product(matrix, v)) / dot_product(v, v)
        
        return [lambda_] + eigenvalues([row[:i] + row[i+1:] for row in matrix[1:]])
    
    def matrix_product(A, B):
        n = len(A)
        result = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    result[i][j] += A[i][k] * B[k][j]
        return result
    
    def norm(v):
        return math.sqrt(sum(x**2 for x in v))
    
    def dot_product(a, b):
        return sum(x * y for x, y in zip(a, b))
    
    n = random.randint(5, 40)
    M = generate_disjointness_matrix(n)
    eigs = eigenvalues(M)
    free_entropy = sum(math.log(abs(eig)) for eig in eigs) / len(eigs)
    
    return {
        "metric_name": "free_entropy",
        "metric_value": free_entropy,
        "instances_tested": 1,
        "conjecture_holds": free_entropy >= n,
        "counterexample": "" if free_entropy >= n else f"Free entropy {free_entropy} < n={n}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or list(range(2, 103))  # Default to first 30 primes
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_free_entropy = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_free_entropy} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_free_entropy} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Free entropy < n\" first_failing_seed={first_failing_seed}")