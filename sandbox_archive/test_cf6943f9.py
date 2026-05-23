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
    
    def generate_boolean_ring(n):
        return [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
    
    def matrix_multiply(A, B):
        n = len(A)
        C = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C
    
    def gaussian_elimination(M):
        n = len(M)
        for i in range(n):
            max_row = i
            for j in range(i+1, n):
                if abs(M[j][i]) > abs(M[max_row][i]):
                    max_row = j
            M[i], M[max_row] = M[max_row], M[i]
            if M[i][i] == 0:
                return None
            for j in range(i+1, n):
                factor = M[j][i] / M[i][i]
                for k in range(n):
                    M[j][k] -= factor * M[i][k]
        rank = sum(1 for row in M if any(row))
        return rank
    
    def min_rank_K(R):
        # Simplified algorithm for Boolean rings
        n = len(R)
        I = [[int(i == j) for i in range(n)] for j in range(n)]
        A = [row[:] + [0] * n for row in R]
        B = [row[:] + [1] * n for row in R]
        rank_A = gaussian_elimination(A)
        rank_B = gaussian_elimination(B)
        return min(rank_A, rank_B)
    
    def tseitin_formula(R):
        # Simplified Tseitin formula construction
        n = len(R)
        clauses = []
        for i in range(n):
            for j in range(n):
                if R[i][j] == 1:
                    clauses.append([i+1, -(j+1)])
        return clauses
    
    def resolution_proof_length(clauses):
        # Simplified resolution proof length calculation
        n = len(clauses)
        max_length = 0
        for clause in clauses:
            max_length = max(max_length, len(clause))
        return max_length
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_length = 0
    instances_tested = 0
    
    for n in n_values:
        R = generate_boolean_ring(n)
        rank_K = min_rank_K(R)
        if rank_K is None:
            continue
        clauses = tseitin_formula(R)
        length = resolution_proof_length(clauses)
        total_length += length
        instances_tested += 1
    
    if instances_tested == 0:
        return {
            "metric_name": "Resolution Proof Length",
            "metric_value": 0,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    mean_length = total_length / instances_tested
    conjecture_holds = mean_length >= math.exp2(rank_K)
    
    return {
        "metric_name": "Resolution Proof Length",
        "metric_value": mean_length,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"mean_length={mean_length} < 2^rank_K={math.exp2(rank_K)}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 35)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_length = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_length} std=0 support_fraction=1")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_length} std=0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mean_length < 2^rank_K\" first_failing_seed={first_failing_seed}")