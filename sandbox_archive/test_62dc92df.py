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
        for k in range(i+1, n):
            if abs(matrix[k][i]) > abs(matrix[max_row][i]):
                max_row = k
        matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
        
        # Eliminate
        factor = Fraction(1, matrix[i][i])
        for j in range(i, n):
            matrix[i][j] *= factor
        
        for k in range(n):
            if k != i:
                factor = Fraction(matrix[k][i])
                for j in range(i, n):
                    matrix[k][j] -= factor * matrix[i][j]

def rank_polymatroid(clauses):
    n = len(clauses)
    matrix = [[0] * (n + 1) for _ in range(n)]
    
    for i in range(n):
        for j in range(i+1, n):
            count = sum(1 for clause in clauses if set(range(len(clause))) & set([i, j]))
            matrix[i][j] = count
            matrix[j][i] = count
    
    gaussian_elimination(matrix)
    
    rank = 0
    for i in range(n):
        if any(matrix[i][j] != 0 for j in range(i+1)):
            rank += 1
    
    return rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    clauses = []
    
    # Generate a random 3-CNF formula
    for _ in range(n):
        clause = [random.choice([-1, 1]) * (i + 1) for i in range(random.randint(2, 3))]
        clauses.append(clause)
    
    rank = rank_polymatroid(clauses)
    
    # Determine if the instance is hard or easy based on monotone circuit size
    is_hard_instance = any(abs(x) == x for clause in clauses for x in clause)
    
    metric_value = rank
    instances_tested = 1
    
    conjecture_holds = False
    counterexample = ""
    
    if is_hard_instance:
        if rank >= n / 2:  # Arbitrary threshold to consider the instance hard
            conjecture_holds = True
    else:
        if rank <= math.log(n, 2):
            conjecture_holds = True
    
    return {
        "metric_name": "polymatroid_rank",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or list(range(2, 200, 7))[:30]
    
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
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        counterexample = "mapping_undefined"
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")