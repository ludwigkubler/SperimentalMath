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

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def lcm(a, b):
    return abs(a * b) // gcd(a, b)

def matrix_multiply(A, B):
    rows_A, cols_A = len(A), len(A[0])
    rows_B, cols_B = len(B), len(B[0])
    if cols_A != rows_B:
        raise ValueError("Incompatible dimensions for matrix multiplication")
    result = [[sum(A[i][k] * B[k][j] for k in range(cols_A)) for j in range(cols_B)] for i in range(rows_A)]
    return result

def gaussian_elimination(matrix):
    rows, cols = len(matrix), len(matrix[0])
    for i in range(rows):
        max_row = i
        for j in range(i + 1, rows):
            if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                max_row = j
        matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
        pivot = matrix[i][i]
        if pivot == 0:
            continue
        for j in range(i, cols):
            matrix[i][j] /= pivot
        for k in range(rows):
            if k != i:
                factor = matrix[k][i]
                for j in range(i, cols):
                    matrix[k][j] -= factor * matrix[i][j]
    return matrix

def rank(matrix):
    reduced_matrix = gaussian_elimination(matrix)
    rank = 0
    for row in reduced_matrix:
        if any(row):
            rank += 1
    return rank

def generate_bp_instance(n):
    # Simple read-twice BP instance generation
    return [random.choice([0, 1]) for _ in range(2 * n)]

def communication_complexity(bp_instance):
    # Simplified communication complexity measure
    return sum(bp_instance)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        bp_instance = generate_bp_instance(n)
        kac_moody_rank = rank([[bp_instance[i], bp_instance[n + i]] for i in range(n)])
        comm_complexity = communication_complexity(bp_instance)
        results.append((kac_moody_rank, comm_complexity))
    
    mean_rank = sum(r[0] for r in results) / len(results)
    mean_comm_complexity = sum(r[1] for r in results) / len(results)
    support_fraction = all(abs(mean_rank - n) <= 0.5 * n and abs(comm_complexity ** 2 - n) <= 0.5 * n for n, _ in results)
    
    return {
        "metric_name": "Rank vs Communication Complexity",
        "metric_value": mean_rank,
        "instances_tested": len(results),
        "conjecture_holds": support_fraction,
        "counterexample": "" if support_fraction else f"Mean rank {mean_rank}, expected range [n-0.5n, n+0.5n], Mean comm complexity {mean_comm_complexity}, expected range [sqrt(n)-0.5n, sqrt(n)+0.5n]"
    }

if __name__ == "__main__":
    import sys
    seeds = list(map(int, sys.argv[1:])) or [2**i + 1 for i in range(30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    std_rank = math.sqrt(sum((r["metric_value"] - mean_rank)**2 for r in results) / len(results))
    support_fraction = all(r["conjecture_holds"] for r in results)
    
    if support_fraction:
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction=1.0")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Rank out of expected range\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")