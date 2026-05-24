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
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math

def gaussian_elimination(A):
    n = len(A)
    for i in range(n):
        # Find pivot
        max_row = i
        for j in range(i+1, n):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        
        # Eliminate below
        pivot = A[i][i]
        for j in range(i+1, n):
            factor = A[j][i] / pivot
            for k in range(n):
                A[j][k] -= factor * A[i][k]

    return A

def rank(A):
    A = gaussian_elimination(A)
    rank = 0
    for row in A:
        if any(row):
            rank += 1
    return rank

def random_planar_cnf(n, m):
    variables = set(range(1, n+1))
    clauses = []
    for _ in range(m):
        clause = set()
        while len(clause) < 3:
            var = random.choice(list(variables))
            if random.choice([True, False]):
                clause.add(-var)
            else:
                clause.add(var)
        clauses.append(tuple(sorted(clause)))
    return clauses

def resolution_length(clauses):
    stack = []
    while True:
        new_clause = None
        for i in range(len(stack)):
            for j in range(i+1, len(stack)):
                if len(stack[i] & stack[j]) == 2:
                    new_clause = (stack[i] - stack[j]).union(stack[j] - stack[i])
                    break
            if new_clause:
                break
        if not new_clause:
            return len(stack)
        stack.append(new_clause)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        m = random.randint(1, min(n * (n - 1) // 2, 10))
        cnf = random_planar_cnf(n, m)
        resolution_len = resolution_length(cnf)
        
        hodge_rank = rank([[1 if i == j else 0 for j in range(n)] for i in range(n)])
        
        results.append({
            "n": n,
            "m": m,
            "resolution_len": resolution_len,
            "hodge_rank": hodge_rank
        })
    
    metric_value = sum(result["hodge_rank"] * result["resolution_len"] for result in results) / len(results)
    instances_tested = len(results)
    conjecture_holds = all(abs(result["hodge_rank"] - result["resolution_len"]) < 1e-6 for result in results)
    
    return {
        "metric_name": "Hodge Rank vs Resolution Length",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")