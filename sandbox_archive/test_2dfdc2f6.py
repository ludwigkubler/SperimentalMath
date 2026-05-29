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

def generate_truth_table(n):
    return [[random.randint(0, 1) for _ in range(2**n)] for _ in range(2**n)]

def tensor_product(A, B):
    n = len(A)
    m = len(B)
    result = []
    for i in range(n):
        row = []
        for j in range(m):
            row.extend([A[i][k] * B[j][k] for k in range(len(B[j]))])
        result.append(row)
    return result

def rank(matrix):
    m, n = len(matrix), len(matrix[0])
    augmented_matrix = [row + [1 if i == j else 0 for j in range(n)] for i, row in enumerate(matrix)]
    for col in range(n):
        max_row = max(range(col, m), key=lambda r: abs(augmented_matrix[r][col]))
        augmented_matrix[col], augmented_matrix[max_row] = augmented_matrix[max_row], augmented_matrix[col]
        if augmented_matrix[col][col] == 0:
            return None
        for row in range(m):
            if row != col:
                factor = -augmented_matrix[row][col] / augmented_matrix[col][col]
                for j in range(n + 1):
                    augmented_matrix[row][j] += factor * augmented_matrix[col][j]
    return sum(1 for row in range(m) if augmented_matrix[row][-1] != 0)

def dpll_conversion_time(n):
    # Placeholder function to simulate DPLL conversion time
    # This is a dummy implementation and should be replaced with actual logic
    return random.randint(1, n**2)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.choice([5, 10, 15, 20, 30, 40])
    truth_table = generate_truth_table(n)
    identity_matrix = [[1 if i == j else 0 for j in range(2**n)] for i in range(2**n)]
    tensor_prod = tensor_product(truth_table, identity_matrix)
    rank_value = rank(tensor_prod)
    conversion_time = dpll_conversion_time(n)
    
    if rank_value is None:
        return {
            "metric_name": "log_2(rank)",
            "metric_value": float('inf'),
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "tensor_product_not_full_rank"
        }
    
    log_rank = math.log2(rank_value)
    log_conversion_time = math.log2(conversion_time)
    
    return {
        "metric_name": "log_2(rank)",
        "metric_value": log_rank,
        "instances_tested": 1,
        "conjecture_holds": False,
        "counterexample": ""
    }

if __name__ == "__main__":
    if len(sys.argv) > 1:
        seeds = [int(s) for s in sys.argv[1:]]
    else:
        primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
        primes += [2 * p for p in primes if 2 * p < 40]
        primes += [3 * p for p in primes if 3 * p < 40]
        primes += [5 * p for p in primes if 5 * p < 40]
        seeds = random.sample(primes, 30)
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={seeds[first_failing_seed]}")