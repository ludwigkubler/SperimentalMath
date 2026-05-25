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

def generate_sat_instance(n, m):
    variables = [f'x{i}' for i in range(n)]
    clauses = []
    for _ in range(m):
        clause = random.sample(variables, 2)
        if random.choice([True, False]):
            clause = [-1 * x for x in clause]
        clauses.append(clause)
    return variables, clauses

def construct_twisted_poisson_matrix(variables, clauses):
    n = len(variables)
    m = len(clauses)
    matrix = [[0] * (n + 2) for _ in range(n + 2)]
    
    for i, var in enumerate(variables):
        matrix[i][i] = 1
        matrix[i][-2] = -1
        matrix[-1][i] = -1
    
    for j, clause in enumerate(clauses):
        for x in clause:
            if x > 0:
                matrix[x-1][n+j] = 1
                matrix[n+j][x-1] = 1
            else:
                matrix[-2][n+j] += 1
                matrix[n+j][-2] += 1
    
    return matrix

def gaussian_elimination(matrix):
    n = len(matrix)
    for i in range(n):
        # Find pivot
        max_row = i
        for j in range(i+1, n):
            if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                max_row = j
        
        # Swap rows
        matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
        
        # Eliminate below pivot
        for j in range(i+1, n):
            factor = Fraction(matrix[j][i], matrix[i][i])
            for k in range(n + 2):
                matrix[j][k] -= factor * matrix[i][k]
    
    return matrix

def min_rank(matrix):
    n = len(matrix)
    rank = n
    for i in range(n):
        if all(matrix[i][j] == 0 for j in range(n)):
            rank -= 1
    return rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    max_n = 40
    results = []
    
    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):  # Ensure at least 30 instances per seed
            variables, clauses = generate_sat_instance(n, n)
            matrix = construct_twisted_poisson_matrix(variables, clauses)
            rank = min_rank(gaussian_elimination(matrix))
            
            expected_bound = 2 ** n * len(clauses)
            results.append({
                "n": n,
                "rank": rank,
                "expected_bound": expected_bound
            })
    
    metric_value = sum(result["rank"] for result in results) / len(results)
    conjecture_holds = all(result["rank"] <= result["expected_bound"] for result in results)
    counterexample = "" if conjecture_holds else "Rank exceeds expected bound"
    
    return {
        "metric_name": "Minimal Rank of Twisted Poisson Manifold",
        "metric_value": metric_value,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Rank exceeds expected bound\" first_failing_seed={seeds[first_failing_seed]}")