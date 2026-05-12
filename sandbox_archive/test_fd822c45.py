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
        # Find pivot
        max_row = i
        for j in range(i+1, n):
            if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                max_row = j
        matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
        
        # Eliminate below the pivot
        factor = Fraction(1, matrix[i][i])
        for j in range(i+1, n):
            matrix[j][i] *= factor
        
        # Eliminate above the pivot
        for j in range(i):
            factor = matrix[j][i]
            for k in range(n):
                matrix[j][k] -= factor * matrix[i][k]
    return matrix

def tropical_dimension(matrix):
    n = len(matrix)
    rank = 0
    for i in range(n):
        if all(abs(matrix[j][i]) == float('inf') for j in range(n)):
            continue
        rank += 1
    return rank

def random_read_once_bp(n):
    bp = []
    for _ in range(2**n):
        state = [random.randint(0, n-1) for _ in range(n)]
        bp.append(state)
    return bp

def random_read_twice_bp(n):
    bp = []
    for _ in range(2**(n+1)):
        state = [random.randint(0, n-1) for _ in range(n)]
        bp.append(state)
    return bp

def tropical_matrix(bp):
    n = len(bp[0])
    m = len(bp)
    matrix = [[float('inf')] * n for _ in range(m)]
    for i in range(m):
        for j in range(n):
            if bp[i][j] == 0:
                matrix[i][j] = 0
            else:
                matrix[i][j] = float('inf')
    return matrix

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n = 10
    read_once_bp = random_read_once_bp(n)
    read_twice_bp = random_read_twice_bp(n)
    
    read_once_dim = tropical_dimension(tropical_matrix(read_once_bp))
    read_twice_dim = tropical_dimension(tropical_matrix(read_twice_bp))
    
    result = {
        "metric_name": "tropical_dimension",
        "metric_value": read_twice_dim,
        "instances_tested": 1,
        "conjecture_holds": read_once_dim >= n/2 and read_twice_dim <= math.log(n, 2) + 1,
        "counterexample": ""
    }
    
    return result

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else list(range(30))
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        counterexample = next(r["counterexample"] for r in results if not r["conjecture_holds"])
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")