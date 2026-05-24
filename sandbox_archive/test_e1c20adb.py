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

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def lcm(a, b):
    return abs(a*b) // gcd(a, b)

def matrix_multiply(A, B):
    rows_A, cols_A = len(A), len(A[0])
    rows_B, cols_B = len(B), len(B[0])
    if cols_A != rows_B:
        raise ValueError("Incompatible dimensions for matrix multiplication")
    result = [[0] * cols_B for _ in range(rows_A)]
    for i in range(rows_A):
        for j in range(cols_B):
            for k in range(cols_A):
                result[i][j] += A[i][k] * B[k][j]
    return result

def gaussian_elimination(matrix):
    rows, cols = len(matrix), len(matrix[0])
    rank = 0
    for i in range(rows):
        if all(matrix[i][j] == 0 for j in range(cols)):
            continue
        pivot_row = matrix[i]
        rank += 1
        for j in range(i + 1, rows):
            factor = -matrix[j][i] / pivot_row[i]
            for k in range(cols):
                if abs(matrix[j][k]) < 1e-9:
                    matrix[j][k] = 0
                else:
                    matrix[j][k] += factor * pivot_row[k]
    return rank

def rank(M):
    M_copy = [row[:] for row in M]
    return gaussian_elimination(M_copy)

def generate_random_boolean_function(n):
    return [random.choice([0, 1]) for _ in range(2**n)]

def compute_quantum_representation(f):
    n = int(math.log2(len(f)))
    Q_f = [[0] * (2**n) for _ in range(2**n)]
    for i in range(2**n):
        for j in range(2**n):
            if f[i ^ j] == 1:
                Q_f[i][j] = 1
    return Q_f

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        f = generate_random_boolean_function(n)
        Q_f = compute_quantum_representation(f)
        M_f = [[0] * (2**n) for _ in range(2**n)]
        
        for i in range(2**n):
            for j in range(2**n):
                if f[i ^ j] == 1:
                    M_f[i][j] = 1
        
        rank_M_f = rank(M_f)
        size_Q_f = len(Q_f)
        results.append({
            "n": n,
            "rank_M_f": rank_M_f,
            "size_Q_f": size_Q_f
        })
    
    mean_rank = sum(result["rank_M_f"] for result in results) / len(results)
    std_dev = math.sqrt(sum((result["rank_M_f"] - mean_rank) ** 2 for result in results) / len(results))
    conjecture_holds = all(mean_rank <= math.log(result["size_Q_f"]) + 3 * std_dev for result in results)
    
    return {
        "metric_name": "Rank of Entanglement Matrix",
        "metric_value": mean_rank,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"Mean rank {mean_rank} exceeds log(size(Q_f)) + 3*std_dev for some n"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_rank = sum(result["metric_value"] for result in results) / len(results)
    std_dev = math.sqrt(sum((result["metric_value"] - mean_rank) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_dev} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Mean rank exceeds log(size(Q_f)) + 3*std_dev\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE")