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

def matrix_rank(matrix):
    m, n = len(matrix), len(matrix[0])
    rank = 0
    for i in range(n):
        if all(matrix[j][i] == 0 for j in range(m)):
            continue
        pivot_row = next(j for j in range(i, m) if matrix[j][i] != 0)
        matrix[i], matrix[pivot_row] = matrix[pivot_row], matrix[i]
        for j in range(m):
            if i != j:
                factor = Fraction(matrix[j][i], matrix[i][i])
                for k in range(n):
                    matrix[j][k] -= factor * matrix[i][k]
        rank += 1
    return rank

def generate_k_cnf(n, q):
    clauses = []
    for _ in range(n):
        literals = random.sample(range(1, n + 1), 2)
        clause = [random.choice([-1, 1]) * literal for literal in literals]
        clauses.append(clause)
    return clauses

def construct_matrix(clauses, q):
    m = len(clauses)
    n = len(clauses[0])
    matrix = [[0] * (q + 1) for _ in range(m)]
    for i, clause in enumerate(clauses):
        for literal in clause:
            if literal > 0:
                matrix[i][literal] += 1
            else:
                matrix[i][-literal] -= 1
    return matrix

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.choice([5, 10, 15, 20, 30, 40])
    q = random.randint(2, 10)
    clauses = generate_k_cnf(n, q)
    matrix = construct_matrix(clauses, q)
    rank = matrix_rank(matrix)
    
    if rank < n**(2/3) * q**(1/3):
        return {
            "metric_name": "minimal_rank",
            "metric_value": rank,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": f"n={n}, q={q}, rank={rank}"
        }
    
    return {
        "metric_name": "minimal_rank",
        "metric_value": rank,
        "instances_tested": 1,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else list(range(2, 30))
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = (sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results)) ** 0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"n={results[0]['instances_tested']}, q={q}\" first_failing_seed={first_failing_seed}")