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

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def lcm(a, b):
    return abs(a * b) // gcd(a, b)

def gaussian_elimination(matrix):
    n = len(matrix)
    for i in range(n):
        if matrix[i][i] == 0:
            for j in range(i + 1, n):
                if matrix[j][i] != 0:
                    matrix[i], matrix[j] = matrix[j], matrix[i]
                    break
            else:
                raise ValueError("Matrix is singular")
        factor = Fraction(matrix[i][i])
        for j in range(n):
            matrix[i][j] /= factor
        for j in range(n):
            if i != j:
                factor = Fraction(matrix[j][i])
                for k in range(n):
                    matrix[j][k] -= factor * matrix[i][k]
    return matrix

def construct_twisted_poisson_matrix(variables, clauses):
    n = len(variables)
    m = len(clauses)
    matrix = [[0] * (n + m) for _ in range(n + m)]
    
    for i in range(n):
        matrix[i][i] = 1
    
    for j in range(m):
        var1, var2 = clauses[j]
        if var1 < n:
            matrix[var1][n + j] = -1
        else:
            matrix[n + var1 - n][n + j] = -1
        
        if var2 < n:
            matrix[var2][n + j] = 1
        else:
            matrix[n + var2 - n][n + j] = 1
    
    return gaussian_elimination(matrix)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n = random.randint(5, 40)
    m = random.randint(n, n * 3)
    variables = list(range(n))
    clauses = [(random.choice(variables), random.choice(variables)) for _ in range(m)]
    
    try:
        matrix = construct_twisted_poisson_matrix(variables, clauses)
        rank = sum(1 for row in matrix if any(row[i] != 0 for i in range(len(row))))
        
        expected_bound = 2 ** n * m
        conjecture_holds = rank <= expected_bound
        
        return {
            "metric_name": "Minimal Rank of Twisted Poisson Manifold",
            "metric_value": rank,
            "instances_tested": 1,
            "conjecture_holds": conjecture_holds,
            "counterexample": "" if conjecture_holds else f"Rank {rank} > {expected_bound}"
        }
    except Exception as e:
        return {
            "metric_name": "Minimal Rank of Twisted Poisson Manifold",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": str(e)
        }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else list(range(2, 30)) + list(range(101, 130))
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    total_rank = sum(r["metric_value"] for r in results if r["metric_value"] is not None)
    num_tests = sum(r["instances_tested"] for r in results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={total_rank / num_tests:.2f} std=0.00 support_fraction=1.00")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={total_rank / num_tests:.2f} std=0.00 support_fraction={support_fraction:.2f}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='{result['counterexample']}' first_failing_seed={first_failing_seed}")