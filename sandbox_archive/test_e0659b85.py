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
        for j in range(i + 1, n):
            if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                max_row = j
        matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
        
        # Eliminate below
        pivot = matrix[i][i]
        for j in range(i + 1, n):
            factor = Fraction(matrix[j][i], pivot)
            for k in range(n):
                matrix[j][k] -= factor * matrix[i][k]

    return matrix

def min_noncommutative_rank(clauses):
    n = len(clauses[0])
    matrix = [[0] * (n + 1) for _ in range(n + 1)]
    
    for clause in clauses:
        for i in range(2 * n):
            if i < n and i % 2 == 0:
                var = abs(clause[i // 2]) - 1
                matrix[var][var] += 1
            elif i >= n:
                var = abs(clause[i - n]) - 1
                matrix[n][var] += 1
                matrix[var][n] += 1
    
    rank = 0
    for row in gaussian_elimination(matrix):
        if any(row):
            rank += 1
    return rank

def dpll_solve(clauses, assignment=None):
    if assignment is None:
        assignment = [False] * len(clauses[0])
    
    def solve(index):
        if index == len(clauses):
            return True
        
        for value in [True, False]:
            new_assignment = assignment[:]
            new_assignment[index // 2] = value
            if all(new_assignment[var - 1] != (not clause[index % 2]) for clause in clauses if var in clause):
                if solve(index + 1):
                    return True
        
        return False
    
    return solve(0)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    clauses = []
    for _ in range(n):
        clause = [random.randint(-n, n) for _ in range(random.randint(1, n))]
        clauses.append(clause)
    
    rank = min_noncommutative_rank(clauses)
    depth = dpll_solve(clauses)
    
    if rank == 0:
        return {
            "metric_name": "min_rank",
            "metric_value": rank,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    metric_value = depth / rank
    conjecture_holds = metric_value >= 2 ** math.floor(math.log(rank, 2))
    counterexample = "" if conjecture_holds else f"depth={depth}, rank={rank}"
    
    return {
        "metric_name": "resolution_depth_over_min_rank",
        "metric_value": metric_value,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"depth_over_min_rank\" first_failing_seed={first_failing_seed}")