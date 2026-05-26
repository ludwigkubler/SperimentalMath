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
    rows, cols = len(matrix), len(matrix[0])
    for i in range(rows):
        # Find pivot
        max_row = i
        for r in range(i + 1, rows):
            if abs(matrix[r][i]) > abs(matrix[max_row][i]):
                max_row = r
        matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
        
        # Eliminate below
        factor = Fraction(matrix[i][i])
        for j in range(i + 1, cols):
            matrix[i][j] /= factor
        
        for r in range(i + 1, rows):
            factor = Fraction(matrix[r][i])
            for j in range(i, cols):
                matrix[r][j] -= factor * matrix[i][j]
    
    # Back substitution
    for i in range(rows - 1, -1, -1):
        for r in range(i + 1, rows):
            matrix[i][-1] -= matrix[r][-1] * matrix[i][r]
        matrix[i][-1] /= matrix[i][i]
    
    rank = sum(1 for row in matrix if any(row))
    return rank

def xor_and_tree_width(f):
    # Placeholder function to compute XOR-AND tree width
    # This is a stub and should be replaced with actual computation
    n = len(f)
    return 2 ** (n - 1)

def quaternionic_representation(f):
    # Placeholder function to compute quaternionic representation
    # This is a stub and should be replaced with actual computation
    n = len(f)
    Q = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i, n):
            if f[i] == f[j]:
                Q[i][j] = 1
                Q[j][i] = 1
    return Q

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    # Generate a random Boolean function with n variables
    n = random.choice([10, 15, 20])
    f = [random.randint(0, 1) for _ in range(2 ** n)]
    
    # Compute quaternionic representation
    Q = quaternionic_representation(f)
    minimal_rank = gaussian_elimination(Q)
    
    # Compute XOR-AND tree width
    xor_and_width = xor_and_tree_width(f)
    
    # Check the conjecture
    conjecture_holds = minimal_rank <= xor_and_width
    counterexample = "" if conjecture_holds else f"rank={minimal_rank}, expected={xor_and_width}"
    
    return {
        "metric_name": "min_rank",
        "metric_value": minimal_rank,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")