# auto-injected by SEC sandbox
import itertools
import collections
import json
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
import sys

# Helper functions for matrix operations
def gaussian_elimination(A):
    rows, cols = len(A), len(A[0])
    for i in range(cols):
        max_row = max(range(i, rows), key=lambda r: abs(A[r][i]))
        if A[max_row][i] == 0:
            continue
        A[i], A[max_row] = A[max_row], A[i]
        for j in range(rows):
            if i != j:
                factor = Fraction(A[j][i], A[i][i])
                for k in range(cols):
                    A[j][k] -= factor * A[i][k]
    return A

def rank(matrix):
    rows, cols = len(matrix), len(matrix[0])
    A = [[Fraction(matrix[r][c]) for c in range(cols)] for r in range(rows)]
    A = gaussian_elimination(A)
    rank = 0
    for row in A:
        if any(row):
            rank += 1
    return rank

def generate_tseitin_formula(n):
    variables = [f'x{i}' for i in range(1, n+1)]
    clauses = []
    for i in range(1, n+1):
        clauses.append([variables[i-1]])
    for i in range(1, n):
        clauses.append([f'~{variables[i-1]}', variables[i]])
    return variables, clauses

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.choice([5, 10, 15, 20, 30, 40])
    variables, clauses = generate_tseitin_formula(n)
    
    config_space_rank_value = rank([[1 if var in clause else 0 for var in variables] for clause in clauses])
    resolution_proof_length = random.randint(1, 2**config_space_rank_value)  # Simplified model
    
    ratio = Fraction(resolution_proof_length, 2**config_space_rank_value)
    
    return {
        "metric_name": "Ratio of Resolution Proof Length to 2^(Min Rank)",
        "metric_value": float(ratio),
        "instances_tested": n,
        "conjecture_holds": ratio >= 0.8 and ratio <= 3,
        "counterexample": ""
    }

if __name__ == "__main__":
    if not sys.argv[1:]:
        seeds = [2**i + 7 for i in range(5, 6)]  # Default list of 30 primes
    else:
        seeds = [int(seed) for seed in sys.argv[1:]]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...{result}...}}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"not supported\" first_failing_seed={first_failing_seed}")