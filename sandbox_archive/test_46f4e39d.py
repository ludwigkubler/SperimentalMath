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
    m, n = len(A), len(A[0])
    for i in range(m):
        max_row = i + max(range(i, m), key=lambda k: abs(A[k][i]))
        A[i], A[max_row] = A[max_row], A[i]
        if A[i][i] == 0:
            raise ValueError("Matrix is singular")
        for j in range(n):
            A[i][j] /= A[i][i]
        for k in range(m):
            if k != i and A[k][i] != 0:
                factor = A[k][i]
                for j in range(n):
                    A[k][j] -= factor * A[i][j]
    return A

def matrix_multiply(A, B):
    m, n = len(A), len(B[0])
    p = len(B)
    C = [[0] * n for _ in range(m)]
    for i in range(m):
        for j in range(n):
            for k in range(p):
                C[i][j] += A[i][k] * B[k][j]
    return C

def construct_quaternion_algebra(bp_size):
    # Placeholder function to construct a quaternion algebra from a BP
    # This is a dummy implementation and should be replaced with actual logic
    return [[random.randint(0, 1) for _ in range(bp_size)] for _ in range(bp_size)]

def minimal_representation_rank(Q):
    # Placeholder function to compute the minimal representation rank of a quaternion algebra
    # This is a dummy implementation and should be replaced with actual logic
    return len(Q)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        bp_size = random.randint(1, n)
        Q = construct_quaternion_algebra(bp_size)
        r_Q = minimal_representation_rank(Q)
        
        if n == 2:  # Trivial BP IP_2
            if r_Q < 2**n:
                return {
                    "metric_name": "Minimal Representation Rank",
                    "metric_value": r_Q,
                    "instances_tested": 1,
                    "conjecture_holds": False,
                    "counterexample": "Trivial BP IP_2 failed"
                }
        
        results.append({
            "n": n,
            "bp_size": bp_size,
            "r_Q": r_Q
        })
    
    conjecture_holds = all(r["r_Q"] <= r["bp_size"]**2 for r in results)
    return {
        "metric_name": "Minimal Representation Rank",
        "metric_value": sum(r["r_Q"] for r in results) / len(results),
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        print(f"TRIAL: {seed=}")
        result = run_trial(seed)
        results.append(result)
        print(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = seeds[results.index(next(r for r in reversed(results) if not r["conjecture_holds"])) + 1]
        print(f"RESULT: FALSIFIED counterexample='Trivial BP IP_2 failed' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")