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

def gaussian_elimination(A):
    n = len(A)
    for i in range(n):
        # Find pivot row
        max_row = i
        for j in range(i+1, n):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        
        # Swap rows
        A[i], A[max_row] = A[max_row], A[i]
        
        # Eliminate below pivot
        for j in range(i+1, n):
            factor = -A[j][i] / A[i][i]
            for k in range(n):
                A[j][k] += factor * A[i][k]
    
    return A

def matrix_multiplication(A, B):
    m = len(A)
    n = len(B[0])
    p = len(B)
    C = [[0 for _ in range(n)] for _ in range(m)]
    for i in range(m):
        for j in range(n):
            for k in range(p):
                C[i][j] += A[i][k] * B[k][j]
    return C

def determinant(A):
    n = len(A)
    if n == 1:
        return A[0][0]
    
    det = 0
    for j in range(n):
        submatrix = [row[:j] + row[j+1:] for row in A[1:]]
        det += (-1) ** j * A[0][j] * determinant(submatrix)
    return det

def hodge_index(clause):
    n = len(clause)
    if n == 0:
        return 0
    
    # Create matrix A
    A = [[0 for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(i+1, n):
            A[i][j] = -1
            A[j][i] = -1
    
    # Add identity matrix to A
    for i in range(n):
        A[i][i] += 1
    
    # Compute determinant of A
    det_A = determinant(A)
    
    return abs(det_A)

def dpll_path_length(clause):
    n = len(clause)
    if n == 0:
        return 0
    
    # Simplify clause
    simplified_clause = []
    for literal in clause:
        if -literal not in simplified_clause:
            simplified_clause.append(literal)
    
    # Compute DPLL path length
    return len(simplified_clause)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    hodge_values = []
    dpll_lengths = []
    
    for n in n_values:
        for _ in range(5):  # Ensure at least 30 instances per seed
            clause = [random.randint(-n, n) for _ in range(n)]
            hodge_values.append(hodge_index(clause))
            dpll_lengths.append(dpll_path_length(clause))
    
    if len(hodge_values) < 30:
        return {
            "metric_name": "Hodge Index vs DPLL Path Length",
            "metric_value": None,
            "instances_tested": len(hodge_values),
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "not_enough_instances"
        }
    
    # Compute correlation coefficient
    hodge_mean = sum(hodge_values) / len(hodge_values)
    dpll_mean = sum(dpll_lengths) / len(dpll_lengths)
    
    numerator = sum((h - hodge_mean) * (d - dpll_mean) for h, d in zip(hodge_values, dpll_lengths))
    denominator = math.sqrt(sum((h - hodge_mean) ** 2 for h in hodge_values)) * math.sqrt(sum((d - dpll_mean) ** 2 for d in dpll_lengths))
    
    correlation_coefficient = numerator / denominator if denominator != 0 else 0
    
    # Compute average absolute difference in ranks
    hodge_ranks = sorted(range(len(hodge_values)), key=hodge_values.__getitem__)
    dpll_ranks = sorted(range(len(dpll_lengths)), key=dpll_lengths.__getitem__)
    rank_differences = [abs(h - d) for h, d in zip(hodge_ranks, dpll_ranks)]
    average_rank_difference = sum(rank_differences) / len(rank_differences)
    
    return {
        "metric_name": "Hodge Index vs DPLL Path Length",
        "metric_value": correlation_coefficient,
        "instances_tested": 30,
        "n_max": max(n_values),
        "conjecture_holds": correlation_coefficient >= 0.7 and average_rank_difference <= 3,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all(r["conjecture_holds"] for r in results):
        support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")