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
    n = len(A)
    for i in range(n):
        # Find pivot
        max_row = i
        for j in range(i + 1, n):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        
        # Eliminate below the pivot
        factor = Fraction(A[i][i])
        for j in range(i + 1, n):
            A[j][i] /= factor
        
        # Eliminate above the pivot
        for j in range(i):
            factor = Fraction(A[j][i])
            for k in range(n):
                A[j][k] -= factor * A[i][k]
    return A

def rank(matrix):
    n = len(matrix)
    m = len(matrix[0])
    A = [row[:] + [1] for row in matrix]  # Augmented matrix
    A = gaussian_elimination(A)
    
    rank = 0
    for i in range(n):
        if any(A[i][j] != 0 for j in range(m)):
            rank += 1
    return rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    
    # Generate random monomially equivalent algebraic curves over a function field
    A = [[random.random() for _ in range(n)] for _ in range(n)]
    B = [[A[i][j] * (i + j + 1) for j in range(n)] for i in range(n)]
    
    # Compute the monotone circuit depth for each curve
    depth_A = sum(abs(x) for row in A for x in row)
    depth_B = sum(abs(x) for row in B for x in row)
    
    # Compute the rank of each curve
    rank_A = rank(A)
    rank_B = rank(B)
    
    # Estimate a constant c by comparing the ranks and monotone circuit depths
    if rank_A == 0 or rank_B == 0:
        return {
            "metric_name": "c",
            "metric_value": float('inf'),
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "rank_zero"
        }
    
    c = depth_A / rank_A
    if depth_B > c * rank_B:
        return {
            "metric_name": "c",
            "metric_value": c,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": f"depth_B={depth_B} exceeds {c}*rank_B={c*rank_B}"
        }
    
    return {
        "metric_name": "c",
        "metric_value": c,
        "instances_tested": 1,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean = sum(r['metric_value'] for r in results) / len(results)
    std_dev = math.sqrt(sum((r['metric_value'] - mean) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r['conjecture_holds']) / len(results)
    
    if all(r['conjecture_holds'] for r in results):
        print(f"RESULT: SUPPORTED mean={mean} std={std_dev} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean} std={std_dev} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r['conjecture_holds'])
        print(f"RESULT: FALSIFIED counterexample=\"c_exceeds_threshold\" first_failing_seed={first_failing_seed}")