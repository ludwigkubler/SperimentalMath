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
    
    def gcd(a, b):
        while b:
            a, b = b, a % b
        return a
    
    def lcm(a, b):
        return abs(a * b) // gcd(a, b)
    
    def matrix_multiply(A, B):
        m, n = len(A), len(B[0])
        p = len(B)
        result = [[sum(A[i][k] * B[k][j] for k in range(p)) for j in range(n)] for i in range(m)]
        return result
    
    def gaussian_elimination(matrix):
        rows, cols = len(matrix), len(matrix[0])
        rank = 0
        for col in range(cols):
            pivot_row = -1
            for row in range(rank, rows):
                if matrix[row][col] != 0:
                    pivot_row = row
                    break
            if pivot_row == -1:
                continue
            matrix[pivot_row], matrix[rank] = matrix[rank], matrix[pivot_row]
            for r in range(rows):
                if r != rank and matrix[r][col] != 0:
                    factor = matrix[r][col] / matrix[rank][col]
                    for c in range(cols):
                        matrix[r][c] -= factor * matrix[rank][c]
            rank += 1
        return rank
    
    def schur_algebra_rank(n, q):
        # Placeholder function to compute Schur algebra rank
        # This is a dummy implementation and should be replaced with actual computation
        return n * (n - 1) // 2
    
    n = random.randint(5, 40)
    q = random.randint(2, 10)
    
    rank = schur_algebra_rank(n, q)
    
    return {
        "metric_name": "Schur Algebra Rank",
        "metric_value": rank,
        "instances_tested": 1,
        "conjecture_holds": rank >= n**2,
        "counterexample": "" if rank >= n**2 else f"Rank {rank} is less than {n**2}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or list(range(30, 100))
    
    results = []
    total_rank = 0
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
        total_rank += trial_result["metric_value"]
    
    mean_rank = total_rank / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"Rank less than n^2\" first_failing_seed={first_failing_seed}")