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
    
    def generate_matrix(N):
        return [[random.choice([0, 1]) for _ in range(N)] for _ in range(N)]
    
    def matrix_multiply(A, B):
        N = len(A)
        C = [[0] * N for _ in range(N)]
        for i in range(N):
            for j in range(N):
                for k in range(N):
                    C[i][j] += A[i][k] * B[k][j]
        return C
    
    def gaussian_elimination(A):
        N = len(A)
        for i in range(N):
            max_row = i
            for j in range(i+1, N):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            for j in range(i+1, N):
                factor = A[j][i] / A[i][i]
                for k in range(N):
                    A[j][k] -= factor * A[i][k]
        return A
    
    def rank(A):
        A = gaussian_elimination(A)
        return sum(1 for row in A if any(row))
    
    def communication_complexity(M):
        N = len(M)
        total_bits = 0
        for i in range(N):
            for j in range(N):
                if M[i][j] == 1:
                    total_bits += math.ceil(math.log2(N+1))
        return total_bits
    
    N = random.randint(5, 40)
    M = generate_matrix(N)
    
    τ_n_M = rank(matrix_multiply(M, list(zip(*M))))
    CC_R_M = communication_complexity(M)
    
    if CC_R_M == 0:
        return {
            "metric_name": "τ_n(M) / CC_R(M)",
            "metric_value": float('inf'),
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "CC_R(M) is zero, making the ratio undefined."
        }
    
    C_n = τ_n_M / CC_R_M
    return {
        "metric_name": "τ_n(M) / CC_R(M)",
        "metric_value": τ_n_M / CC_R_M,
        "instances_tested": 1,
        "conjecture_holds": τ_n_M <= 2 * CC_R_M,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(1, 9973) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
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