# auto-injected by SEC sandbox
import itertools
import collections
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
import sys
import json

def gaussian_elimination(A):
    n = len(A)
    for i in range(n):
        max_row = i + max(range(i, n), key=lambda j: abs(A[j][i]))
        A[i], A[max_row] = A[max_row], A[i]
        for j in range(i+1, n):
            factor = A[j][i] / A[i][i]
            for k in range(n):
                A[j][k] -= factor * A[i][k]
    return A

def matrix_rank(A, tol=1e-9):
    A_echelon = gaussian_elimination(A)
    rank = sum(1 for row in A_echelon if any(abs(x) > tol for x in row))
    return rank

def sign_matrix(M):
    N = len(M)
    result = [[0] * N for _ in range(N)]
    for i in range(N):
        for j in range(N):
            result[i][j] = 1 if M[i][j] > 0 else -1
    return result

def prefix_sum_matrix(M):
    N = len(M)
    result = [[0] * (N+1) for _ in range(N)]
    for i in range(N):
        for j in range(1, N+1):
            result[i][j] = result[i][j-1] + M[i][j-1]
    return result

def zero_crossing_count(prefix_sum):
    count = 0
    current_sum = prefix_sum[0]
    for i in range(1, len(prefix_sum)):
        if current_sum == 0:
            count += 1
        current_sum += prefix_sum[i]
    return count

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.choice([3, 4, 5])
    N = 2 ** n
    
    def generate_random_matrix():
        return [[random.choice([-1, 1]) for _ in range(N)] for _ in range(N)]
    
    def generate_rank_1_planted(v):
        M = [[0] * N for _ in range(N)]
        for i in range(N):
            for j in range(N):
                M[i][j] = v[i] * v[j]
        return sign_matrix(M)
    
    def generate_rk_r_planted(r, v_list):
        M = [[0] * N for _ in range(N)]
        for u, v in zip(v_list[:r], v_list[r:]):
            for i in range(N):
                for j in range(N):
                    M[i][j] += u[i] * v[j]
        return sign_matrix(M)
    
    def generate_symmetric_structured():
        if random.choice([0, 1]) == 0:
            return [[1 if i == j else -1 if (i + j) % 2 == 0 else 0 for j in range(N)] for i in range(N)]
        elif random.choice([0, 1]) == 1:
            return [[1 if i == j else 0 for j in range(N)] for i in range(N)]
        elif random.choice([0, 1]) == 2:
            return [[1 if (i + j) % 2 == 0 else -1 for j in range(N)] for i in range(N)]
        elif random.choice([0, 1]) == 3:
            return [[1 if i == j else 0 for j in range(N)] for i in range(N)]
    
    instances_tested = 0
    max_R_row = 0
    max_R_col = 0
    
    for _ in range(200):
        M = generate_random_matrix()
        rk = matrix_rank(M)
        prefix_sum = prefix_sum_matrix(M)
        R_row = zero_crossing_count(prefix_sum)
        max_R_row = max(max_R_row, R_row)
        
        M_transpose = [list(x) for x in zip(*M)]
        prefix_sum_col = prefix_sum_matrix(M_transpose)
        R_col = zero_crossing_count(prefix_sum_col)
        max_R_col = max(max_R_col, R_col)
        
        instances_tested += 1
    
    B_row = 4 * math.sqrt(rk * N * math.log2(N))
    B_col = 4 * math.sqrt(rk * N * math.log2(N))
    
    conjecture_holds_row = max_R_row <= B_row
    conjecture_holds_col = max_R_col <= B_col
    
    return {
        "metric_name": "max_zero_crossing_count",
        "metric_value": max(max_R_row, max_R_col),
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds_row and conjecture_holds_col,
        "counterexample": "" if conjecture_holds_row and conjecture_holds_col else "mapping_undefined"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [11, 23, 37, 53, 71]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {json.dumps(result)}")
        results.append(result)
    
    total_instances = sum(r["instances_tested"] for r in results)
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={seeds[first_failing_seed]}")
    else:
        print(f"RESULT: INCONCLUSIVE mapping_undefined")