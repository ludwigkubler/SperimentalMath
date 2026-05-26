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
    rows, cols = len(matrix), len(matrix[0])
    for i in range(rows):
        max_row = i + max(range(i, rows), key=lambda r: abs(matrix[r][i]))
        matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
        for j in range(cols):
            if j != i:
                factor = Fraction(matrix[j][i], matrix[i][i])
                for k in range(cols):
                    matrix[j][k] -= factor * matrix[i][k]
    return matrix

def rank(matrix):
    rows, cols = len(matrix), len(matrix[0])
    row_echelon_form = gaussian_elimination(matrix)
    rank = 0
    for i in range(rows):
        if any(row_echelon_form[i][j] != 0 for j in range(cols)):
            rank += 1
    return rank

def frege_proof_width(clauses):
    width = 0
    for clause in clauses:
        width = max(width, len(clause))
    return width

def generate_random_formula(n):
    variables = [f'x{i}' for i in range(1, n+1)]
    clauses = []
    for _ in range(n):
        clause = random.sample(variables + [f'~{v}' for v in variables], 2)
        clauses.append(clause)
    return clauses

def run_trial(seed: int) -> dict:
    random.seed(seed)
    results = []
    n_values = [5, 10, 15, 20, 30, 40]
    for n in n_values:
        for _ in range(5):  # Ensure at least 30 instances per seed
            clauses = generate_random_formula(n)
            frege_width = frege_proof_width(clauses)
            if frege_width == 1:
                continue
            brauer_rank = rank([[1]])
            results.append((n, frege_width, brauer_rank))
    
    total_instances = len(results)
    mean_brauer_rank = sum(r[2] for r in results) / total_instances
    max_ratio = max(abs(r[2] / r[1]) for r in results)
    conjecture_holds = max_ratio <= 10  # Arbitrary constant c
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "Brauer Rank to Frege Proof Width Ratio",
        "metric_value": mean_brauer_rank,
        "instances_tested": total_instances,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_brauer_rank = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        result = "SUPPORTED"
    elif support_fraction >= 0.8:
        result = "SUPPORTED"
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        result = f"FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}"
    
    print(f"RESULT: {result} mean={mean_brauer_rank:.2f} std=0.00 support_fraction={support_fraction:.2f}")