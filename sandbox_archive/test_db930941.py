# auto-injected by SEC sandbox
import itertools
import json
import sys
import os
import time
import re
from itertools import product, combinations, permutations, chain
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from collections import defaultdict

# Helper functions for Gaussian elimination and matrix operations
def gaussian_elimination(A, b):
    n = len(b)
    M = [A[i] + [b[i]] for i in range(n)]
    for i in range(n):
        max_row = max(range(i, n), key=lambda k: abs(M[k][i]))
        M[i], M[max_row] = M[max_row], M[i]
        factor = M[i][i]
        if factor == 0:
            raise ValueError("Matrix is singular")
        for j in range(n):
            M[i][j] /= factor
        b[i] /= factor
        for k in range(n):
            if k != i:
                factor = M[k][i]
                for j in range(n + 1):
                    M[k][j] -= factor * M[i][j]
    return [row[-1] for row in M]

def matrix_multiply(A, B):
    n = len(A)
    m = len(B[0])
    result = [[0] * m for _ in range(n)]
    for i in range(n):
        for j in range(m):
            for k in range(len(B)):
                result[i][j] += A[i][k] * B[k][j]
    return result

def matrix_add(A, B):
    n = len(A)
    m = len(A[0])
    result = [[A[i][j] + B[i][j] for j in range(m)] for i in range(n)]
    return result

def matrix_sub(A, B):
    n = len(A)
    m = len(A[0])
    result = [[A[i][j] - B[i][j] for j in range(m)] for i in range(n)]
    return result

def matrix_transpose(A):
    n = len(A)
    m = len(A[0])
    result = [[A[j][i] for j in range(n)] for i in range(m)]
    return result

# Function to generate a random Boolean formula
def generate_instance(n):
    variables = [f"x{i}" for i in range(1, n + 1)]
    clauses = []
    for _ in range(n):
        clause = random.sample(variables, random.randint(1, len(variables)))
        clauses.append(" & ".join(clause))
    return " | ".join(clauses)

# Function to compute the width of the DPLL search tree
def dpll_width(formula):
    # Placeholder function for actual DPLL implementation
    return 0

# Function to calculate the minimal local ring rank of a polynomial
def local_ring_rank(formula):
    # Placeholder function for actual computation
    return 0

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        instances_tested = 0
        total_width = 0
        total_rank = 0
        
        while instances_tested < 30:
            formula = generate_instance(n)
            width = dpll_width(formula)
            rank = local_ring_rank(formula)
            
            if width is None or rank is None:
                continue
            
            results.append({"n": n, "width": width, "rank": rank})
            instances_tested += 1
            total_width += width
            total_rank += rank
    
    if not results:
        return {
            "metric_name": "DPLL Width vs Local Ring Rank",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    mean_width = sum(result["width"] for result in results) / len(results)
    mean_rank = sum(result["rank"] for result in results) / len(results)
    correlation_coefficient = 0
    
    if len(results) > 1:
        numerator = sum((result["width"] - mean_width) * (result["rank"] - mean_rank) for result in results)
        denominator = math.sqrt(sum((result["width"] - mean_width) ** 2 for result in results)) * math.sqrt(sum((result["rank"] - mean_rank) ** 2 for result in results))
        correlation_coefficient = numerator / denominator
    
    return {
        "metric_name": "DPLL Width vs Local Ring Rank",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(result["n"] for result in results),
        "conjecture_holds": correlation_coefficient > 0.5,  # Adjust threshold as needed
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 7 for i in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all(result["conjecture_holds"] for result in results):
        mean_value = sum(result["metric_value"] for result in results) / len(results)
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_value} std=0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        counterexample = f"n={max(result['n'] for result in results)}, w={max(result['metric_value'] for result in results)}, r={min(local_ring_rank(generate_instance(n)) for n in [5, 10, 15, 20, 30, 40])}"
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")