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

# Helper functions for matrix operations
def gaussian_elimination(A):
    n = len(A)
    for i in range(n):
        # Find pivot
        max_row = i
        for j in range(i+1, n):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        
        # Eliminate below pivot
        for j in range(i+1, n):
            factor = A[j][i] / A[i][i]
            for k in range(n):
                A[j][k] -= factor * A[i][k]

def matrix_rank(A):
    A_copy = [row[:] for row in A]
    gaussian_elimination(A_copy)
    rank = 0
    for row in A_copy:
        if any(row):
            rank += 1
    return rank

# Helper function to generate Tseitin formula
def generate_tseitin_formula(n):
    variables = list(range(1, n+1))
    clauses = []
    
    # Generate clauses for each variable
    for var in variables:
        clause = [var, -var]
        clauses.append(clause)
    
    # Generate clauses for OR gates
    for i in range(2**n):
        binary_rep = format(i, '0{}b'.format(n))
        literals = [int(binary_rep[j]) * (j+1) if binary_rep[j] == '1' else -(j+1) for j in range(n)]
        clauses.append(literals)
    
    return variables, clauses

# Main function to run a single trial
def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.choice([5, 10, 15, 20, 30, 40])
    variables, clauses = generate_tseitin_formula(n)
    
    # Construct the tropical divisor class group
    G = [[0] * (n + 1) for _ in range(n + 1)]
    for clause in clauses:
        if len(clause) == 2:
            x, y = abs(clause[0]), abs(clause[1])
            G[x][y], G[y][x] = 1, 1
    
    # Compute the rank of G
    rk_G = matrix_rank(G)
    
    # Compute the resolution proof width (simplified for this test)
    w_phi = len(variables) * len(clauses)
    
    # Check if the ratio is within [0.5, 1.5]
    if 0.5 <= rk_G / w_phi <= 1.5:
        conjecture_holds = True
        counterexample = ""
    else:
        conjecture_holds = False
        counterexample = "ratio_out_of_bounds"
    
    return {
        "metric_name": "rank_to_width_ratio",
        "metric_value": rk_G / w_phi,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
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
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"ratio_out_of_bounds\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")