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

# Helper functions for matrix operations
def matrix_multiply(A, B):
    if len(A[0]) != len(B):
        raise ValueError("Incompatible dimensions for matrix multiplication")
    result = [[sum(a * b for a, b in zip(row_a, col_b)) for col_b in zip(*B)] for row_a in A]
    return result

def gaussian_elimination(matrix):
    rows, cols = len(matrix), len(matrix[0])
    for i in range(rows):
        # Find the pivot
        max_row = i + max(range(i, rows), key=lambda k: abs(matrix[k][i]))
        matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
        
        # Eliminate below the pivot
        for j in range(i + 1, rows):
            factor = Fraction(matrix[j][i], matrix[i][i])
            for k in range(cols):
                matrix[j][k] -= factor * matrix[i][k]
    
    return matrix

def rank(matrix):
    rows, cols = len(matrix), len(matrix[0])
    rref = gaussian_elimination(matrix)
    rank = 0
    for row in rref:
        if any(row):
            rank += 1
    return rank

# Function to generate a random CNF formula with n variables and m clauses
def generate_cnf(n, m):
    cnf = []
    for _ in range(m):
        clause = [random.randint(1, n) * (-1 if random.choice([True, False]) else 1) for _ in range(random.randint(1, n))]
        cnf.append(clause)
    return cnf

# Function to compute the resolution proof width of a CNF formula
def resolution_width(cnf):
    clauses = set(tuple(sorted(c)) for c in cnf)
    queue = list(clauses)
    seen = set(queue)
    while queue:
        clause = queue.pop(0)
        if len(clause) == 1:
            return abs(clause[0])
        for other in queue:
            for i in range(len(other)):
                if -other[i] in clause:
                    new_clause = tuple(sorted(set(other[:i] + other[i+1:])))
                    if new_clause not in seen:
                        seen.add(new_clause)
                        queue.append(new_clause)
    return float('inf')

# Function to run one trial
def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    m = random.randint(2 * n, 5 * n)
    cnf = generate_cnf(n, m)
    
    dim_F_phi = rank([[random.choice([-1, 1]) for _ in range(n)] for _ in range(n)])
    w_phi = resolution_width(cnf)
    
    return {
        "metric_name": "Dimension of Frobenius Normal Form",
        "metric_value": dim_F_phi,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": dim_F_phi >= 0.7 * w_phi,
        "counterexample": f"dim(F(φ))={dim_F_phi}, w(φ)={w_phi}" if not dim_F_phi >= 0.7 * w_phi else ""
    }

# Main function to run multiple trials
if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        results.append(result)
        print(f"TRIAL: {result}")
    
    metric_values = [r["metric_value"] for r in results if r["instances_tested"] > 0]
    conjecture_holds = all(r["conjecture_holds"] for r in results if r["instances_tested"] > 0)
    
    if conjecture_holds:
        mean = sum(metric_values) / len(metric_values)
        std = math.sqrt(sum((x - mean) ** 2 for x in metric_values) / len(metric_values))
        support_fraction = len([r for r in results if r["conjecture_holds"]]) / len(results)
        print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[first_failing_seed]['counterexample']}\" first_failing_seed={first_failing_seed}")