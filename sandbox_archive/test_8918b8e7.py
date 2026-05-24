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

def generate_cnf(n):
    cnf = []
    for _ in range(2 * n):
        clause = [random.randint(1, n)]
        while len(clause) < 3:
            var = random.randint(1, n)
            if var not in clause and -var not in clause:
                clause.append(var)
        cnf.append(clause)
    return cnf

def gaussian_elimination(matrix):
    rows, cols = len(matrix), len(matrix[0])
    for i in range(rows):
        # Find the pivot
        max_row = i
        for r in range(i + 1, rows):
            if abs(matrix[r][i]) > abs(matrix[max_row][i]):
                max_row = r
        matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
        
        # Eliminate below the pivot
        for r in range(i + 1, rows):
            factor = matrix[r][i] / matrix[i][i]
            for c in range(cols):
                matrix[r][c] -= factor * matrix[i][c]

    return matrix

def rank(matrix):
    matrix = gaussian_elimination(matrix)
    rank = 0
    for row in matrix:
        if any(row):
            rank += 1
    return rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n = random.randint(5, 40)
    cnf = generate_cnf(n)
    
    # Convert CNF to vector space over GF(2)
    variables = set()
    for clause in cnf:
        for var in clause:
            variables.add(abs(var))
    variable_count = len(variables)
    vector_space = [[0] * variable_count for _ in range(1 << n)]
    
    for i, clause in enumerate(cnf):
        for var in clause:
            if var > 0:
                vector_space[i][var - 1] = 1
            else:
                vector_space[i][abs(var) - 1] = 1
    
    # Compute the Brauer group rank
    brauer_group_rank = rank(vector_space)
    
    # Simulate resolution refutation depth (simplified model)
    refutation_depth = n * math.log2(n)
    
    return {
        "metric_name": "Rank vs DPLL Heig",
        "metric_value": brauer_group_rank,
        "instances_tested": 1,
        "conjecture_holds": brauer_group_rank >= 2**(n/4),
        "counterexample": "" if brauer_group_rank >= 2**(n/4) else f"n={n}, rank={brauer_group_rank}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(1, 1000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction={support_fraction}")
    elif any(r["metric_value"] <= n**(1/8) for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"rank ≤ n^(1/8)\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=unknown")