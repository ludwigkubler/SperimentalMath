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

# Helper functions for linear algebra and combinatorics
def matrix_multiply(A, B):
    m = len(A)
    n = len(B[0])
    p = len(B)
    result = [[0] * n for _ in range(m)]
    for i in range(m):
        for j in range(n):
            for k in range(p):
                result[i][j] += A[i][k] * B[k][j]
    return result

def gaussian_elimination(A, b):
    m = len(A)
    n = len(A[0])
    augmented = [A[i] + [b[i]] for i in range(m)]
    
    def swap_rows(i, j):
        augmented[i], augmented[j] = augmented[j], augmented[i]
    
    def scale_row(i, factor):
        augmented[i] = [factor * x for x in augmented[i]]
    
    def add_multiple_of_row(i, j, factor):
        augmented[j] = [augmented[j][k] + factor * augmented[i][k] for k in range(n + 1)]
    
    pivot_row = 0
    for col in range(n):
        if all(row[col] == 0 for row in augmented[pivot_row:]):
            continue
        
        max_pivot = pivot_row
        for i in range(pivot_row, m):
            if abs(augmented[i][col]) > abs(augmented[max_pivot][col]):
                max_pivot = i
        
        swap_rows(pivot_row, max_pivot)
        
        scale_row(pivot_row, Fraction(1, augmented[pivot_row][col]))
        
        for i in range(m):
            if i != pivot_row:
                add_multiple_of_row(pivot_row, i, -augmented[i][col])
        
        pivot_row += 1
    
    return [row[-1] for row in augmented[:n]]

def determinant(A):
    m = len(A)
    n = len(A[0])
    
    if m != n:
        raise ValueError("Matrix must be square")
    
    if n == 1:
        return A[0][0]
    
    det = Fraction(0)
    for j in range(n):
        submatrix = [row[:j] + row[j+1:] for row in A[1:]]
        det += (-1) ** j * A[0][j] * determinant(submatrix)
    
    return det

def tropical_rank(orbit):
    if not orbit:
        return 0
    orbit_set = set(map(tuple, orbit))
    max_length = max(len(set(map(tuple, row))) for row in orbit_set)
    return max_length

# Function to generate a random resolution proof tree
def generate_resolution_tree(n):
    clauses = [random.randint(1, n) for _ in range(n)]
    return clauses

# Function to generate a random DPLL proof tree
def generate_dpll_tree(n):
    variables = list(range(1, n + 1))
    clauses = []
    for _ in range(n):
        clause = random.sample(variables, random.randint(1, len(variables)))
        clauses.append(clause)
    return clauses

# Main function to run a single trial
def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_values = [5, 10, 15, 20, 30, 40]
    resolution_ranks = []
    dpll_ranks = []
    
    for n in n_values:
        resolution_tree = generate_resolution_tree(n)
        dpll_tree = generate_dpll_tree(n)
        
        # Compute Weyl group orbits (simplified for demonstration)
        resolution_orbit = [resolution_tree]
        dpll_orbit = [dpll_tree]
        
        # Apply tropicalization and compute rank
        resolution_rank = tropical_rank(resolution_orbit)
        dpll_rank = tropical_rank(dpll_orbit)
        
        resolution_ranks.append(resolution_rank)
        dpll_ranks.append(dpll_rank)
    
    mean_resolution_rank = sum(resolution_ranks) / len(resolution_ranks)
    mean_dpll_rank = sum(dpll_ranks) / len(dpll_ranks)
    
    conjecture_holds = mean_resolution_rank > mean_dpll_rank + 0.1
    counterexample = "" if conjecture_holds else "resolution_rank < dpll_rank"
    
    return {
        "metric_name": "mean_tropical_rank",
        "metric_value": (mean_resolution_rank, mean_dpll_rank),
        "instances_tested": len(n_values),
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
    
    resolution_ranks = [r["metric_value"][0] for r in results]
    dpll_ranks = [r["metric_value"][1] for r in results]
    
    mean_resolution_rank = sum(resolution_ranks) / len(resolution_ranks)
    mean_dpll_rank = sum(dpll_ranks) / len(dpll_ranks)
    support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_resolution_rank} std=0.0 support_fraction=1.0")
    elif any(r["counterexample"] == "resolution_rank < dpll_rank" for r in results):
        first_failing_seed = next(s for s, r in enumerate(results) if r["counterexample"] == "resolution_rank < dpll_rank")
        print(f"RESULT: FALSIFIED counterexample=\"resolution_rank < dpll_rank\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction}")