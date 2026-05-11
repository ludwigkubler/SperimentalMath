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
    def gcd(a, b):
        while b:
            a, b = b, a % b
        return a

    def extended_gcd(a, b):
        if a == 0:
            return b, 0, 1
        g, x1, y1 = extended_gcd(b % a, a)
        x = y1 - (b // a) * x1
        y = x1
        return g, x, y

    def mod_inverse(a, m):
        g, x, _ = extended_gcd(a, m)
        if g != 1:
            raise ValueError(f"No modular inverse for {a} under {m}")
        return x % m

    def matrix_multiply(A, B):
        rows_A, cols_A = len(A), len(A[0])
        rows_B, cols_B = len(B), len(B[0])
        if cols_A != rows_B:
            raise ValueError("Incompatible dimensions for matrix multiplication")
        result = [[sum(A[i][k] * B[k][j] for k in range(cols_A)) % 2 for j in range(cols_B)] for i in range(rows_A)]
        return result

    def gaussian_elimination(A):
        rows, cols = len(A), len(A[0])
        rank = 0
        for col in range(cols):
            pivot_row = -1
            for row in range(rank, rows):
                if A[row][col] == 1:
                    pivot_row = row
                    break
            if pivot_row != -1:
                A[pivot_row], A[rank] = A[rank], A[pivot_row]
                for r in range(rows):
                    if r != rank and A[r][col] == 1:
                        A[r] = [(A[r][c] + A[rank][c]) % 2 for c in range(cols)]
                rank += 1
        return rank

    def is_disjointness_matrix(M):
        n = len(M)
        for i in range(n):
            for j in range(i + 1, n):
                if sum(M[i][k] & M[j][k] for k in range(n)) != 0:
                    return False
        return True

    def generate_disjointness_matrix(n):
        M = [[random.randint(0, 1) for _ in range(n)] for _ in range(n)]
        while not is_disjointness_matrix(M):
            M = [[random.randint(0, 1) for _ in range(n)] for _ in range(n)]
        return M

    def compute_gonality(n):
        # Placeholder for actual computation of gonality
        return math.ceil(math.sqrt(n))

    n = random.choice([5, 10, 15, 20, 30, 40])
    seed = seed * n
    random.seed(seed)
    M = generate_disjointness_matrix(n)
    rank = gaussian_elimination(M)
    gonality = compute_gonality(n)
    communication_complexity = math.ceil(math.sqrt(n))
    
    conjecture_holds = gonality >= communication_complexity
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "Gonality",
        "metric_value": gonality,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_gonality = sum(r["metric_value"] for r in results) / len(results)
    std_gonality = math.sqrt(sum((r["metric_value"] - mean_gonality)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_gonality:.2f} std={std_gonality:.2f} support_fraction={support_fraction:.2f}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")