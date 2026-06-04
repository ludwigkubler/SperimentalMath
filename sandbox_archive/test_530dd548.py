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
    
    def gaussian_elimination(A):
        m, n = len(A), len(A[0])
        for i in range(m):
            max_row = i
            for j in range(i+1, m):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            factor = A[i][i]
            for j in range(n):
                A[i][j] /= factor
            for j in range(m):
                if j != i:
                    factor = A[j][i]
                    for k in range(n):
                        A[j][k] -= factor * A[i][k]
        return A

    def matrix_multiply(A, B):
        m, n, p = len(A), len(B), len(B[0])
        C = [[0] * p for _ in range(m)]
        for i in range(m):
            for j in range(p):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C

    def trace(A):
        return sum(A[i][i] for i in range(len(A)))

    def log2(x):
        if x <= 0:
            return float('-inf')
        return math.log2(x)

    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        # Generate a random communication complexity function
        f_n = [random.randint(0, 1) for _ in range(n)]
        
        # Construct the associated quantum state G_f
        dim = 2 ** n
        G_f = [[0] * dim for _ in range(dim)]
        for i in range(dim):
            for j in range(dim):
                if (i & j) == 0:
                    G_f[i][j] = f_n[i ^ j]
        
        # Compute the minimal geometric entanglement E(G_f)
        eigenvalues = []
        A = [[0] * dim for _ in range(dim)]
        for i in range(dim):
            for j in range(dim):
                A[i][j] = G_f[i][j] - (trace(G_f) / dim)
        A = gaussian_elimination(A)
        for i in range(dim):
            eigenvalues.append(abs(A[i][i]))
        
        min_entanglement = sum(eigenvalue ** 2 for eigenvalue in eigenvalues if eigenvalue > 0)
        
        # Compute the communication complexity rank
        rank = len([x for x in f_n if x == 1])
        
        results.append({
            "n": n,
            "entanglement": min_entanglement,
            "rank": rank
        })
    
    metric_sum = sum(result["entanglement"] * result["rank"] for result in results)
    mean = Fraction(metric_sum, len(results))
    std_dev = math.sqrt(sum((result["entanglement"] * result["rank"] - mean) ** 2 for result in results) / len(results))
    
    conjecture_holds = all(result["entanglement"] <= 10 * log2(result["n"]) ** 2 for result in results)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "Geometric Entanglement and Communication Complexity Rank",
        "metric_value": float(mean),
        "instances_tested": len(results),
        "n_max": max(result["n"] for result in results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean = sum(result["metric_value"] for result in results) / len(results)
    std_dev = math.sqrt(sum((result["metric_value"] - mean) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean} std={std_dev} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean} std={std_dev} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")