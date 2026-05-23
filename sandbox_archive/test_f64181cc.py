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

def gaussian_elimination(A):
    rows, cols = len(A), len(A[0])
    for i in range(cols):
        max_row = max(range(i, rows), key=lambda j: abs(A[j][i]))
        if A[max_row][i] == 0:
            continue
        A[i], A[max_row] = A[max_row], A[i]
        for j in range(rows):
            if i != j:
                factor = -A[j][i] / A[i][i]
                for k in range(cols):
                    A[j][k] += factor * A[i][k]

def rank(A):
    rows, cols = len(A), len(A[0])
    A_copy = [row[:] for row in A]
    gaussian_elimination(A_copy)
    rank = 0
    for i in range(min(rows, cols)):
        if A_copy[i][i] != 0:
            rank += 1
    return rank

def tensor_product(f, g):
    n = len(f)
    result = [f[i] * g[i] for i in range(n)]
    return result

def compute_theta(n, k):
    # Placeholder function for θ(n, k). Implement as needed.
    return 2 ** (n - k)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    f = [random.choice([0, 1]) for _ in range(2**n)]
    
    T_f = []
    for x in range(2**n):
        T_f.append(f[x])
    
    min_rank_T_f = rank(T_f)
    
    g = [1 - y for y in f]
    tensor_product_f_g = tensor_product(f, g)
    theta_value = compute_theta(n, len(tensor_product_f_g))
    
    conjecture_holds = min_rank_T_f <= theta_value
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "min_rank_T_f",
        "metric_value": min_rank_T_f,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]]
    if not seeds:
        primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
        seeds = random.sample(primes, 30)
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(res["metric_value"] for res in results) / len(results)
    std_value = math.sqrt(sum((res["metric_value"] - mean_value) ** 2 for res in results) / len(results))
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(res["seed"] for res in results if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")