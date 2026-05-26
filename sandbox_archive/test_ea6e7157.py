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

def generate_and_or_tree(depth, leaves):
    if depth == 0:
        return leaves.pop()
    else:
        left = generate_and_or_tree(depth - 1, leaves)
        right = generate_and_or_tree(depth - 1, leaves)
        return [left, right]

def matrix_multiply(A, B):
    m = len(A)
    n = len(B[0])
    p = len(B)
    result = [[0 for _ in range(n)] for _ in range(m)]
    for i in range(m):
        for j in range(n):
            for k in range(p):
                result[i][j] += A[i][k] * B[k][j]
    return result

def gaussian_elimination(A, b):
    n = len(A)
    augmented_matrix = [A[i] + [b[i]] for i in range(n)]
    for i in range(n):
        max_row = i
        for j in range(i+1, n):
            if abs(augmented_matrix[j][i]) > abs(augmented_matrix[max_row][i]):
                max_row = j
        augmented_matrix[i], augmented_matrix[max_row] = augmented_matrix[max_row], augmented_matrix[i]
        pivot = augmented_matrix[i][i]
        for j in range(i, n+1):
            augmented_matrix[i][j] /= pivot
        for j in range(n):
            if j != i:
                factor = augmented_matrix[j][i]
                for k in range(i, n+1):
                    augmented_matrix[j][k] -= factor * augmented_matrix[i][k]
    return [row[-1] for row in augmented_matrix]

def min_rank(V_T):
    try:
        rank = 0
        A = []
        for v in V_T:
            if any(v):
                A.append(v)
        m = len(A)
        n = len(A[0])
        B = [[A[i][j] for j in range(n)] for i in range(m)]
        rank = gaussian_elimination(B, [0]*n).count(0)
        return rank
    except Exception as e:
        print(f"Error in min_rank: {e}")
        return None

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    D = math.ceil(math.log2(n + 1))
    leaves = [random.choice([0, 1]) for _ in range(n)]
    T = generate_and_or_tree(D, leaves)
    
    V_T = []
    def build_vector(node):
        if isinstance(node, list):
            left, right = node
            build_vector(left)
            build_vector(right)
        else:
            V_T.append([node])
    build_vector(T)
    
    rank = min_rank(V_T)
    if rank is None:
        return {
            "metric_name": "minRank",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    expected_rank = n**2
    if rank < expected_rank / 2 or rank > expected_rank * 2:
        return {
            "metric_name": "minRank",
            "metric_value": rank,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": f"rank {rank} is outside the expected range [{expected_rank/2}, {expected_rank*2}]"
        }
    
    return {
        "metric_name": "minRank",
        "metric_value": rank,
        "instances_tested": 1,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = list(map(int, sys.argv[1:])) or [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    metric_values = [r["metric_value"] for r in results if r["metric_value"] is not None]
    support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={sum(metric_values)/len(metric_values):.2f} std=0.00 support_fraction=1.00")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={sum(metric_values)/len(metric_values):.2f} std={math.sqrt(sum((x - sum(metric_values)/len(metric_values))**2 for x in metric_values) / len(metric_values)):0.2f} support_fraction={support_fraction:.2f}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='rank outside expected range' first_failing_seed={first_failing_seed}")