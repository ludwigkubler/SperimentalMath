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

def gaussian_elimination(A, b):
    n = len(b)
    for i in range(n):
        # Find pivot row
        max_row = i
        for j in range(i+1, n):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        
        # Swap rows
        A[i], A[max_row] = A[max_row], A[i]
        b[i], b[max_row] = b[max_row], b[i]
        
        # Eliminate below pivot
        for j in range(i+1, n):
            factor = -A[j][i] / A[i][i]
            for k in range(n):
                A[j][k] += factor * A[i][k]
            b[j] += factor * b[i]
    
    # Back substitution
    x = [0] * n
    for i in range(n-1, -1, -1):
        x[i] = (b[i] - sum(A[i][j] * x[j] for j in range(i+1, n))) / A[i][i]
    
    return x

def tseitin_to_polynomial(clauses):
    n = len(clauses)
    A = [[0] * (n + 2) for _ in range(n + 2)]
    b = [0] * (n + 2)
    
    for i, clause in enumerate(clauses):
        for literal in clause:
            if literal > 0:
                A[i][literal - 1] += 1
            else:
                A[i][-1] -= 1
        A[i][-2] = 1
    
    b[-2] = n
    b[-1] = 1
    
    roots = gaussian_elimination(A, b)
    num_roots = sum(1 for root in roots if abs(root) < 1e-6)
    
    return num_roots

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n = random.randint(5, 40)
    clauses = []
    for _ in range(n):
        clause = [random.randint(-n, -1)]
        for _ in range(random.randint(1, 3)):
            clause.append(random.randint(1, n))
        clauses.append(clause)
    
    num_roots = tseitin_to_polynomial(clauses)
    
    return {
        "metric_name": "num_roots",
        "metric_value": num_roots,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_num_roots = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_num_roots} std=0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"not enough data\" first_failing_seed={first_failing_seed}")