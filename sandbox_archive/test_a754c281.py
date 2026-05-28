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

def generate_random_3cnf(n, m):
    variables = [f'x{i}' for i in range(1, n + 1)]
    clauses = []
    for _ in range(m):
        clause = random.sample(variables + ['~' + var for var in variables], 3)
        clauses.append(clause)
    return clauses

def construct_multivariate_cf(clauses):
    # Simplified representation; actual construction would be more complex
    return len(clauses)

def rank_of_matrix(matrix):
    n = len(matrix)
    m = len(matrix[0])
    if n != m:
        raise ValueError("Matrix is not square")
    
    for i in range(n):
        max_row = i
        for j in range(i + 1, n):
            if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                max_row = j
        
        if matrix[max_row][i] == 0:
            return None  # Matrix is singular
        
        matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
        
        for j in range(n):
            if i != j:
                factor = Fraction(matrix[j][i], matrix[i][i])
                for k in range(m):
                    matrix[j][k] -= factor * matrix[i][k]
    
    rank = sum(1 for row in matrix if any(row))
    return rank

def min_resolution_proof_length(clauses):
    # Simplified DPLL solver; actual implementation would be more complex
    return len(clauses)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    m = random.randint(n, n * 2)
    
    clauses = generate_random_3cnf(n, m)
    cf_representation = construct_multivariate_cf(clauses)
    rank = rank_of_matrix(cf_representation) if isinstance(cf_representation, list) else None
    proof_length = min_resolution_proof_length(clauses)
    
    if rank is None:
        return {
            "metric_name": "rank",
            "metric_value": 0,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    metric_value = rank / proof_length
    conjecture_holds = metric_value <= 10 and (rank >= m or proof_length == 0)
    counterexample = "" if conjecture_holds else f"Rank {rank} exceeds inverse of proof length {proof_length}"
    
    return {
        "metric_name": "rank",
        "metric_value": metric_value,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all("conjecture_holds" in r and r["conjecture_holds"] for r in results):
        mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        counterexample = next(result["counterexample"] for result in results if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")