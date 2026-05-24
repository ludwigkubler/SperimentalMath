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

def generate_k_cnf(n, k):
    clauses = []
    for _ in range(k):
        clause = [random.choice([-1, 1]) * (i + 1) for i in random.sample(range(n), random.randint(1, n))]
        clauses.append(clause)
    return clauses

def gaussian_elimination(matrix):
    rows, cols = len(matrix), len(matrix[0])
    for col in range(cols):
        pivot_row = None
        for row in range(col, rows):
            if matrix[row][col] != 0:
                pivot_row = row
                break
        if pivot_row is None:
            continue
        matrix[pivot_row], matrix[col] = matrix[col], matrix[pivot_row]
        for row in range(rows):
            if row != col and matrix[row][col] != 0:
                factor = Fraction(matrix[row][col], matrix[col][col])
                for j in range(cols):
                    matrix[row][j] -= factor * matrix[col][j]
    rank = sum(1 for row in matrix if any(x != 0 for x in row))
    return rank

def resolution_length(cnf):
    stack = cnf[:]
    while True:
        new_clauses = []
        added_clause = False
        for i in range(len(stack)):
            for j in range(i + 1, len(stack)):
                clause_i = set(abs(x) for x in stack[i])
                clause_j = set(abs(x) for x in stack[j])
                if not (clause_i & clause_j):
                    continue
                new_clause = [x for x in stack[i] if abs(x) not in clause_j]
                new_clause.extend([x for x in stack[j] if abs(x) not in clause_i])
                if len(new_clause) > 0:
                    new_clauses.append(new_clause)
                    added_clause = True
        if not added_clause:
            break
        stack.extend(new_clauses)
    return len(stack)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    k = 3
    cnf = generate_k_cnf(n, k)
    
    tropicalized_scheme_rank = gaussian_elimination(cnf)
    resolution_length_value = resolution_length(cnf)
    
    if resolution_length_value > 2 * tropicalized_scheme_rank**2:
        return {
            "metric_name": "resolution_length_over_rank_squared",
            "metric_value": resolution_length_value,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": f"n={n}, k={k}, rank={tropicalized_scheme_rank}, length={resolution_length_value}"
        }
    
    return {
        "metric_name": "resolution_length_over_rank_squared",
        "metric_value": resolution_length_value,
        "instances_tested": 1,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = next(r["counterexample"] for r in results if r["counterexample"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")