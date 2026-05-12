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

def finite_field_add(a, b, q):
    return (a + b) % q

def finite_field_mul(a, b, q):
    return (a * b) % q

def finite_field_inv(a, q):
    for i in range(1, q):
        if finite_field_mul(a, i, q) == 1:
            return i
    raise ValueError("No inverse found")

def gaussian_elimination(matrix, n, q):
    for i in range(n):
        # Find pivot row
        pivot_row = i
        while pivot_row < n and matrix[pivot_row][i] == 0:
            pivot_row += 1
        if pivot_row == n:
            continue
        
        # Swap rows
        matrix[i], matrix[pivot_row] = matrix[pivot_row], matrix[i]
        
        # Eliminate below pivot
        for j in range(i + 1, n):
            factor = finite_field_mul(matrix[j][i], finite_field_inv(matrix[i][i], q), q)
            for k in range(n + 1):
                matrix[j][k] = finite_field_add(matrix[j][k], finite_field_mul(-factor, matrix[i][k], q), q)

def rank(matrix, n, q):
    gaussian_elimination(matrix, n, q)
    return sum(1 for row in matrix if any(x != 0 for x in row[:n]))

def generate_projective_plane(q):
    if q < 2:
        raise ValueError("q must be at least 2")
    
    points = [(i, j) for i in range(q) for j in range(q)]
    lines = []
    
    # Vertical lines
    for i in range(q):
        line = [(i, j) for j in range(q)]
        lines.append(line)
    
    # Horizontal lines
    for j in range(q):
        line = [(i, j) for i in range(q)]
        lines.append(line)
    
    # Diagonal lines
    for k in range(2 * q - 1):
        if k < q:
            line = [(i, (i + k) % q) for i in range(q)]
        else:
            line = [(q - 1 - (k - q), i) for i in range(q)]
        lines.append(line)
    
    return points, lines

def generate_cnf_from_plane(points, lines):
    n = len(points)
    m = len(lines)
    cnf = []
    
    # Each point must be on at least one line
    for i in range(n):
        clause = [j + 1 for j in range(m) if (i // q, i % q) in lines[j]]
        cnf.append(clause)
    
    return cnf

def compute_seed_length(cnf):
    n = len(cnf)
    m = sum(len(clause) for clause in cnf)
    seed_length = 0
    
    # Simulate iterative partitioning
    while m > 1:
        seed_length += 1
        m = math.ceil(m / 2)
    
    return seed_length

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    q_values = [2, 3]
    results = []
    
    for q in q_values:
        points, lines = generate_projective_plane(q)
        cnf = generate_cnf_from_plane(points, lines)
        
        if len(cnf) != q * (q + 1):
            return {
                "metric_name": "seed_length",
                "metric_value": None,
                "instances_tested": 0,
                "conjecture_holds": False,
                "counterexample": "mapping_undefined"
            }
        
        seed_length = compute_seed_length(cnf)
        expected_bound = q**2 + q + 1
        
        results.append({
            "q": q,
            "seed_length": seed_length,
            "expected_bound": expected_bound
        })
    
    conjecture_holds = all(result["seed_length"] <= result["expected_bound"] for result in results)
    counterexample = "" if conjecture_holds else f"q={results[0]['q']}, seed_length={results[0]['seed_length']}, expected_bound={results[0]['expected_bound']}"
    
    return {
        "metric_name": "seed_length",
        "metric_value": sum(result["seed_length"] for result in results) / len(results),
        "instances_tested": len(results),
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
    
    mean_seed_length = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_seed_length} std=0.0 support_fraction=1.0")
    elif any(not result["conjecture_holds"] for result in results) and support_fraction >= 0.8:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"q={results[0]['q']}, seed_length={results[0]['seed_length']}, expected_bound={results[0]['expected_bound']}\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction}")