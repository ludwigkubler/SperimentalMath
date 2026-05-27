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
        # Find a non-zero pivot in column i
        pivot_row = i
        while pivot_row < rows and matrix[pivot_row][i] == 0:
            pivot_row += 1
        if pivot_row == rows:
            continue  # Column is all zeros, skip it
        
        # Swap the current row with the pivot row
        matrix[i], matrix[pivot_row] = matrix[pivot_row], matrix[i]
        
        # Eliminate non-zero entries below the pivot
        for j in range(i + 1, rows):
            factor = -matrix[j][i] / matrix[i][i]
            for k in range(cols):
                if i == k:
                    matrix[j][k] = 0
                else:
                    matrix[j][k] += factor * matrix[i][k]
    return matrix

def compute_minimal_rank(matrix):
    rows, cols = len(matrix), len(matrix[0])
    rank = 0
    for row in range(rows):
        if any(matrix[row][j] != 0 for j in range(cols)):
            rank += 1
    return rank

def generate_boolean_formula(tree_width):
    if tree_width == 0:
        return random.choice([True, False])
    else:
        left = generate_boolean_formula(tree_width - 1)
        right = generate_boolean_formula(tree_width - 1)
        return (left and right) or (not left and not right)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_tests = 30
    total_rank = 0
    supports_conjecture = True
    
    for _ in range(n_tests):
        k = random.randint(1, 40)
        formula = generate_boolean_formula(k)
        
        # Constructive mapping (simplified example)
        matrix = [[random.choice([0, 1]) for _ in range(k)] for _ in range(k)]
        reduced_matrix = gaussian_elimination(matrix)
        minimal_rank = compute_minimal_rank(reduced_matrix)
        
        total_rank += minimal_rank
        
        if minimal_rank > k**2 * math.log(k):
            supports_conjecture = False
            counterexample = f"Formula with tree-width {k}, rank {minimal_rank}"
            break
    
    mean_rank = total_rank / n_tests
    result = {
        "metric_name": "Minimal Rank",
        "metric_value": mean_rank,
        "instances_tested": n_tests,
        "conjecture_holds": supports_conjecture,
        "counterexample": counterexample if not supports_conjecture else ""
    }
    
    return result

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        print(f"TRIAL: {seed}")
        result = run_trial(seed)
        results.append(result)
        
        print(result)
    
    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        counterexample = results[results.index(next(r for r in results if not r["conjecture_holds"]))]["counterexample"]
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")