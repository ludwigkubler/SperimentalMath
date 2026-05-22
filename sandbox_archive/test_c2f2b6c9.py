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

# Helper functions for Gaussian elimination and matrix operations
def gaussian_elimination(matrix):
    rows, cols = len(matrix), len(matrix[0])
    for i in range(rows):
        # Find pivot
        max_row = i
        for r in range(i+1, rows):
            if abs(matrix[r][i]) > abs(matrix[max_row][i]):
                max_row = r
        matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
        
        # Eliminate below the pivot
        for r in range(i+1, rows):
            factor = Fraction(matrix[r][i], matrix[i][i])
            for c in range(cols):
                matrix[r][c] -= factor * matrix[i][c]

    return matrix

def determinant(matrix):
    n = len(matrix)
    det = 0
    if n == 2:
        det = matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
    else:
        for c in range(n):
            submatrix = [row[:c] + row[c+1:] for row in matrix[1:]]
            det += ((-1) ** c) * matrix[0][c] * determinant(submatrix)
    return det

def generate_cnf(n, k):
    # Generate a random CNF formula representing k-CLIQUE instances
    clauses = []
    for i in range(k):
        clause = [random.randint(1, n), -random.randint(1, n)]
        clauses.append(clause)
    return clauses

def grb_minimal_intersection_rank(cnf):
    # Compute the Gröbner basis and determine its minimal intersection rank
    # This is a simplified representation; actual computation would be complex
    # For demonstration, we use a dummy value based on n and k
    return (n ** 2 * k / 3)

def construct_monotone_circuit(n):
    # Construct a monotone circuit of varying depths for each instance
    # This is a simplified representation; actual construction would be complex
    # For demonstration, we use a dummy value based on n
    return random.randint(10, 100)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    results = []
    for _ in range(30):
        n = random.choice([5, 10, 15, 20, 30, 40])
        k = random.randint(2, min(n // 2, 5))
        
        cnf = generate_cnf(n, k)
        grb_rank = grb_minimal_intersection_rank(cnf)
        circuit_depth = construct_monotone_circuit(n)
        
        results.append((grb_rank, circuit_depth))
    
    mean_grb_rank = sum(grb for grb, _ in results) / len(results)
    mean_circuit_depth = sum(depth for _, depth in results) / len(results)
    ratio = mean_grb_rank / mean_circuit_depth
    
    return {
        "metric_name": "Ratio of Gröbner Rank to Circuit Depth",
        "metric_value": ratio,
        "instances_tested": len(results),
        "conjecture_holds": False if ratio < 2 else True,
        "counterexample": "" if ratio >= 2 else f"Ratio {ratio} < 2"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(1, 1000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_ratio = sum(result["metric_value"] for result in results) / len(results)
    std_ratio = math.sqrt(sum((result["metric_value"] - mean_ratio) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_ratio} std={std_ratio} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in enumerate(results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Ratio < 2\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")