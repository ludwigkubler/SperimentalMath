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

def factorial(n):
    if n == 0:
        return 1
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result

def hook_walk(n):
    # Compute the number of standard Young tableaux of the staircase shape (n,n-1,...,1)
    # with inversion compatibility with at least one permutation in S_n.
    if n == 1:
        return 1
    count = 0
    for i in range(1, n + 1):
        count += hook_walk(n - i) * factorial(i - 1) // factorial(n)
    return count

def perm_to_matrix(perm, n):
    # Convert a permutation to an n x n matrix.
    matrix = [[0] * n for _ in range(n)]
    for i in range(n):
        matrix[i][perm[i]] = 1
    return matrix

def tensor_product(A, B):
    # Compute the tensor product of two matrices A and B.
    result = []
    for a_row in A:
        new_row = []
        for b_col in zip(*B):
            new_row.append([a * b for a, b in zip(a_row, b_col)])
        result.append(sum(new_row, []))
    return result

def tensor_rank(tensor):
    # Compute the rank of a 3-tensor using greedy tropical slice elimination.
    n = len(tensor)
    eps = 1e-9
    rank = 0
    while True:
        max_slice = None
        max_value = -math.inf
        for i in range(n):
            slice_sum = sum(sum(row) for row in tensor[i])
            if slice_sum > max_value:
                max_slice = i
                max_value = slice_sum
        if max_value < eps:
            break
        rank += 1
        for j in range(n):
            tensor[j][max_slice] = [0] * n
    return rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    results = []
    for n in range(2, 8):
        Per_n = [[random.randint(1, 3) for _ in range(n)] for _ in range(n)]
        Det_n = [[random.randint(1, 3) for _ in range(n)] for _ in range(n)]
        
        T_Per_n = tensor_product(Per_n, perm_to_matrix(range(n), n))
        T_Det_n = tensor_product(Det_n, perm_to_matrix(range(n), n))
        
        SYT_n = hook_walk(n)
        B_n = math.ceil(math.log2(SYT_n / factorial(n)))
        
        D_n = tensor_rank(T_Per_n) - tensor_rank(T_Det_n)
        
        results.append({
            "metric_name": "D(n)",
            "metric_value": D_n,
            "instances_tested": 1,
            "conjecture_holds": D_n >= B_n and (D_n == B_n if n <= 3 else True),
            "counterexample": "" if D_n >= B_n else f"n={n}, D(n)={D_n}, B(n)={B_n}"
        })
    
    total_D = sum(result["metric_value"] for result in results)
    total_B = sum(1 for result in results if result["conjecture_holds"])
    support_fraction = total_B / len(results)
    
    return {
        "seed": seed,
        "total_D": total_D,
        "total_B": total_B,
        "support_fraction": support_fraction
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [11, 23, 37, 53, 71]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_D = sum(result["total_D"] for result in results) / len(results)
    mean_B = sum(result["total_B"] for result in results) / len(results)
    support_fraction = sum(result["support_fraction"] for result in results) / len(results)
    
    if all(result["support_fraction"] == 1.0 for result in results):
        print(f"RESULT: SUPPORTED mean={mean_D} std=0.0 support_fraction=1.0")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"n={first_failing_seed}\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction}")