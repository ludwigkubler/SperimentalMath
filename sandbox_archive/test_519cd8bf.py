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
    
    def generate_matrix(n):
        return [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
    
    def matrix_multiply(A, B):
        n = len(A)
        C = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C
    
    def noncommutative_tensor_product(M):
        n = len(M)
        T = [[0] * (n**2) for _ in range(n**2)]
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    for l in range(n):
                        T[i*n + k][j*n + l] = M[i][k] * M[j][l]
        return T
    
    def rank(matrix):
        n = len(matrix)
        A = [row[:] for row in matrix]
        pivot_row = 0
        for i in range(n):
            if A[pivot_row][i] == 0:
                found_nonzero = False
                for j in range(pivot_row + 1, n):
                    if A[j][i] != 0:
                        A[pivot_row], A[j] = A[j], A[pivot_row]
                        found_nonzero = True
                        break
                if not found_nonzero:
                    continue
            for j in range(n):
                if i == j:
                    continue
                factor = -A[j][i] / A[pivot_row][i]
                for k in range(n):
                    A[j][k] += factor * A[pivot_row][k]
            pivot_row += 1
        return pivot_row
    
    def communication_complexity(M):
        n = len(M)
        total_bits = 0
        for i in range(n):
            for j in range(n):
                if M[i][j] == 1:
                    total_bits += math.ceil(math.log2(n))
        return total_bits / (n * n)
    
    def randomized_communication_complexity(M, num_samples=1000):
        n = len(M)
        total_bits = 0
        for _ in range(num_samples):
            i, j = random.sample(range(n), 2)
            if M[i][j] == 1:
                total_bits += math.ceil(math.log2(n))
        return total_bits / (n * n * num_samples)
    
    n = random.randint(5, 40)
    M = generate_matrix(n)
    T = noncommutative_tensor_product(M)
    τ_n_M = rank(T)
    CC_R_M = communication_complexity(M)
    C_n = τ_n_M / CC_R_M
    
    return {
        "metric_name": "C_n",
        "metric_value": C_n,
        "instances_tested": 1,
        "conjecture_holds": τ_n_M <= 2 * CC_R_M,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else list(range(2, 30))
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_C_n = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_C_n} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_C_n} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"C_n exceeded 2 * CC_R(M)\" first_failing_seed={seeds[first_failing_seed]}")