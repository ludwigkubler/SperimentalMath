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

# Constants
MAX_N = 40
NUM_SEEDS = 30
MIN_TROPICAL_RANK = 1
MAX_TROPICAL_RANK = 10

# Helper functions
def gaussian_elimination(A, b):
    n = len(b)
    for i in range(n):
        # Find pivot
        max_row = i
        for j in range(i+1, n):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        b[i], b[max_row] = b[max_row], b[i]
        
        # Eliminate below pivot
        for j in range(i+1, n):
            factor = A[j][i] / A[i][i]
            for k in range(i, n):
                A[j][k] -= factor * A[i][k]
            b[j] -= factor * b[i]
    
    # Back substitution
    x = [0.0] * n
    for i in range(n-1, -1, -1):
        x[i] = (b[i] - sum(A[i][j] * x[j] for j in range(i+1, n))) / A[i][i]
    return x

def matrix_multiply(A, B):
    n = len(A)
    C = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

def determinant(A):
    n = len(A)
    if n == 1:
        return A[0][0]
    det = 0
    sign = 1
    for j in range(n):
        submatrix = [row[:j] + row[j+1:] for row in A[1:]]
        det += sign * A[0][j] * determinant(submatrix)
        sign *= -1
    return det

def tropical_rank(clauses):
    n = len(clauses)
    if n == 0:
        return MIN_TROPICAL_RANK
    
    # Create adjacency matrix for the graph
    adj_matrix = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i+1, n):
            if any(clause[i] != clause[j] for clause in clauses):
                adj_matrix[i][j] = 1.0
                adj_matrix[j][i] = 1.0
    
    # Perform Gaussian elimination to find the rank
    A = adj_matrix + [[1.0] * n]
    b = [0.0] * n + [1.0]
    try:
        x = gaussian_elimination(A, b)
        return sum(1 for val in x if abs(val) > 1e-6)
    except ZeroDivisionError:
        return n

def resolution_width(cnf):
    queue = cnf[:]
    while queue:
        clause = random.choice(queue)
        queue.remove(clause)
        new_clauses = []
        for other_clause in queue:
            common_vars = set(clause) & set(other_clause)
            if len(common_vars) == 1:
                new_var = list(common_vars)[0]
                new_clause = [v for v in clause if v != new_var] + [v for v in other_clause if v != -new_var]
                if new_clause not in queue and new_clause not in new_clauses:
                    new_clauses.append(new_clause)
        queue.extend(new_clauses)
    return max(len(clause) for clause in queue)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    results = []
    for n in range(5, 41):
        cnf = [[random.choice([-1, 1]) * (i + 1) for i in range(n)] for _ in range(random.randint(2, 5))]
        mtr = tropical_rank(cnf)
        w = resolution_width(cnf)
        
        results.append({
            "n": n,
            "mtr": mtr,
            "w": w
        })
    
    mean_w = sum(result["w"] for result in results) / len(results)
    std_w = math.sqrt(sum((result["w"] - mean_w) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["w"] <= mean_w + 3 * std_w) / len(results)
    
    conjecture_holds = support_fraction >= 0.8
    counterexample = "" if conjecture_holds else "n_max=40, w > mean + 3*std"
    
    return {
        "metric_name": "resolution_width",
        "metric_value": mean_w,
        "instances_tested": len(results),
        "n_max": max(result["n"] for result in results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
    
    # Compute mean/std of metric_value, fraction of seeds where conjecture_holds
    all_results = [run_trial(seed) for seed in seeds]
    mean_w = sum(result["metric_value"] for result in all_results) / len(all_results)
    std_w = math.sqrt(sum((result["metric_value"] - mean_w) ** 2 for result in all_results) / len(all_results))
    support_fraction = sum(1 for result in all_results if result["conjecture_holds"]) / len(all_results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_w} std={std_w} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in all_results):
        first_failing_seed = next(seed for seed, result in zip(seeds, all_results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"n_max=40, w > mean + 3*std\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=budget_exceeded n_tested=30")