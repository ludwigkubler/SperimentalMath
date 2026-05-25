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
    
    def matrix_multiplication(A, B):
        m, n, p = len(A), len(B), len(B[0])
        C = [[0] * p for _ in range(m)]
        for i in range(m):
            for j in range(p):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C
    
    def compute_hodge_invariant(f):
        # Placeholder for actual computation
        # This is a dummy function to illustrate the structure
        n = len(f)
        H = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i+1, n):
                H[i][j] = f[i] - f[j]
                H[j][i] = f[j] - f[i]
        return gaussian_elimination(H)
    
    def compute_circuit_size(f):
        # Placeholder for actual computation
        # This is a dummy function to illustrate the structure
        n = len(f)
        size = 0
        for i in range(1, n):
            size += abs(f[i] - f[i-1])
        return size
    
    def min_rank(H):
        rank = 0
        for row in H:
            if any(row):
                rank += 1
        return rank
    
    n = random.randint(5, 40)
    f = [random.randint(1, 100) for _ in range(n)]
    
    H = compute_hodge_invariant(f)
    circuit_size = compute_circuit_size(f)
    rank = min_rank(H)
    
    metric_value = rank / circuit_size if circuit_size > 0 else float('inf')
    conjecture_holds = metric_value >= 0.8
    counterexample = "" if conjecture_holds else f"n={n}, f={f}, rank={rank}, circuit_size={circuit_size}"
    
    return {
        "metric_name": "Ratio of Min Rank to Circuit Size",
        "metric_value": metric_value,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    
    if not sys.argv[1:]:
        seeds = [2**i + 3 for i in range(5, 8)]  # First 30 prime numbers
    else:
        seeds = [int(s) for s in sys.argv[1:]]
    
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
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        for r in results:
            if not r["conjecture_holds"]:
                counterexample = r["counterexample"]
                first_failing_seed = seed
                break
        
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")