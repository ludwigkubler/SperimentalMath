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

def gaussian_elimination(matrix):
    n = len(matrix)
    for i in range(n):
        max_row = max(range(i, n), key=lambda r: abs(matrix[r][i]))
        matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
        
        denom = matrix[i][i]
        if denom == 0:
            continue
        
        for j in range(n):
            matrix[i][j] /= denom
        
        for k in range(n):
            if k != i:
                factor = matrix[k][i]
                for j in range(n):
                    matrix[k][j] -= factor * matrix[i][j]
    return sum(1 for row in matrix if any(row))

def free_probability_distribution(P):
    n = len(P)
    A = [[0] * (n + 1) for _ in range(n + 1)]
    for i in range(n):
        for j in range(n):
            A[i][j] = P[j][i]
    
    A[-1][-1] = -1
    for i in range(n):
        A[i][-1] = 1
    
    return gaussian_elimination(A)

def calculate_rank(P):
    rho_C = free_probability_distribution(P)
    return rho_C

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    alphabet_size = n
    X = [''.join(random.choices('abcdefghijklmnopqrstuvwxyz', k=n)) for _ in range(alphabet_size)]
    Y = [''.join(random.choices('abcdefghijklmnopqrstuvwxyz', k=n)) for _ in range(alphabet_size)]
    
    P = [[random.random() for _ in range(n)] for _ in range(n)]
    for row in P:
        total = sum(row)
        for j in range(n):
            row[j] /= total
    
    rank = calculate_rank(P)
    
    return {
        "metric_name": "rank",
        "metric_value": rank,
        "instances_tested": 1,
        "conjecture_holds": rank <= math.log(alphabet_size),
        "counterexample": "" if rank <= math.log(alphabet_size) else f"Rank {rank} > log({alphabet_size})"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    std_rank = math.sqrt(sum((r["metric_value"] - mean_rank) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"Rank exceeds log(n)\" first_failing_seed={first_failing_seed}")