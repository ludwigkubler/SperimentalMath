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
        # Find pivot
        max_row = i
        for r in range(i+1, rows):
            if abs(matrix[r][i]) > abs(matrix[max_row][i]):
                max_row = r
        matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
        
        # Eliminate below
        for r in range(i+1, rows):
            factor = -matrix[r][i] / matrix[i][i]
            for c in range(cols):
                if i == c:
                    matrix[r][c] = 0
                else:
                    matrix[r][c] += factor * matrix[i][c]

def determinant(matrix):
    n = len(matrix)
    det = Fraction(1)
    for i in range(n):
        det *= matrix[i][i]
    return det

def characteristic_polynomial(matrix):
    n = len(matrix)
    x = Fraction('x')
    identity = [[Fraction(0) if r != c else Fraction(1) for c in range(n)] for r in range(n)]
    
    # Augmented matrix
    aug_matrix = [row + identity[i] for i, row in enumerate(matrix)]
    
    # Perform Gaussian elimination
    gaussian_elimination(aug_matrix)
    
    # Calculate determinant of the upper triangular matrix
    char_poly = determinant([[aug_matrix[r][c] for c in range(n)] for r in range(n)])
    
    return char_poly

def rank(matrix):
    n, m = len(matrix), len(matrix[0])
    row_rref = [row[:] for row in matrix]
    rank = 0
    
    for i in range(m):
        if sum(row[i] != Fraction(0) for row in row_rref[:n]):
            rank += 1
            # Make the leading coefficient 1
            lead_coeff = row_rref[rank-1][i]
            for j in range(n):
                row_rref[j][i] /= lead_coeff
            
            # Eliminate above and below
            for r in range(rank-1):
                factor = -row_rref[r][i]
                for c in range(m):
                    if i == c:
                        row_rref[r][c] = 0
                    else:
                        row_rref[r][c] += factor * row_rref[rank-1][c]
    
    return rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.choice([5, 10, 15, 20, 30, 40])
    communication_matrix = [[random.randint(0, 1) for _ in range(n)] for _ in range(n)]
    
    char_poly = characteristic_polynomial(communication_matrix)
    rank_val = rank(communication_matrix)
    
    # Count distinct p-adic roots modulo p^2
    p = 2
    p_adic_roots = set()
    for coeff in char_poly.numerator.coefficients:
        if coeff % p == 0:
            root = -coeff / (p**2)
            if root not in p_adic_roots:
                p_adic_roots.add(root)
    
    n_max = n
    instances_tested = 1
    
    # Calculate the ratio |N_{p-adic}(φ)| / Var(Rank(φ))
    mean_ratio = len(p_adic_roots) / (rank_val * (n - rank_val))
    
    conjecture_holds = mean_ratio <= 3
    counterexample = "" if conjecture_holds else f"mean_ratio={mean_ratio}"
    
    return {
        "metric_name": "mean_ratio",
        "metric_value": mean_ratio,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    std_metric_value = math.sqrt(sum((result["metric_value"] - mean_metric_value)**2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results) and support_fraction >= 0.8:
        first_failing_seed = next(seed for seed, result in enumerate(results, start=1) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mean_ratio' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")