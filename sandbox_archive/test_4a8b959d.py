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
    rank = 0
    for j in range(n):
        i_max = rank
        for i in range(rank, m):
            if abs(A[i][j]) > abs(A[i_max][j]):
                i_max = i
        if A[i_max][j] == 0:
            continue
        A[rank], A[i_max] = A[i_max], A[rank]
        pivot = A[rank][j]
        for j2 in range(n):
            A[rank][j2] /= pivot
        for i in range(m):
            if i != rank and A[i][j] != 0:
                factor = A[i][j]
                for j2 in range(n):
                    A[i][j2] -= factor * A[rank][j2]
        rank += 1
    return rank

def matrix_rank(matrix):
    m, n = len(matrix), len(matrix[0])
    A = [row[:] for row in matrix]
    return gaussian_elimination(A)

def communication_complexity(matrix):
    N = len(matrix)
    if N == 0:
        return 0
    rank_Q = matrix_rank(matrix)
    return 1 + math.log2(N * rank_Q)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    N = 40
    matrix = [[random.choice([-1, 1]) for _ in range(N)] for _ in range(N)]
    cc = communication_complexity(matrix)
    metric_value = cc
    instances_tested = 1
    conjecture_holds = False
    counterexample = ""
    
    if rank_Q < math.log2(N) / 4:
        if cc <= 3:
            conjecture_holds = True
        else:
            counterexample = "CC(XOR, M) > 3 for low-rank matrix"
    
    return {
        "metric_name": "communication_complexity",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    if len(sys.argv) > 1:
        seeds = [int(seed) for seed in sys.argv[1:]]
    else:
        primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]
        seeds = random.sample(primes, 30)
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    total_metric_value = sum(res["metric_value"] for res in results)
    mean_metric_value = total_metric_value / len(results)
    std_metric_value = (sum((res["metric_value"] - mean_metric_value) ** 2 for res in results) / len(results)) ** 0.5
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not res["conjecture_holds"] for res in results) and support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, res in zip(seeds, results) if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"CC(XOR, M) > 3 for low-rank matrix\" first_failing_seed={first_failing_seed}")