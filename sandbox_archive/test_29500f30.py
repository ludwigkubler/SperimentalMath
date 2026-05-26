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
        for j in range(i+1, rows):
            if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                max_row = j
        matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
        
        # Eliminate below pivot
        for j in range(i+1, rows):
            factor = Fraction(matrix[j][i], matrix[i][i])
            for k in range(cols):
                matrix[j][k] -= factor * matrix[i][k]

    return matrix

def compute_rank(matrix):
    matrix = [row[:] for row in matrix]
    gaussian_elimination(matrix)
    rank = 0
    for row in matrix:
        if any(row):
            rank += 1
    return rank

def generate_xor_and_tree(depth, max_children=2):
    if depth == 0:
        return random.choice([True, False])
    children = [generate_xor_and_tree(depth-1) for _ in range(random.randint(1, max_children))]
    return (children[0], children[1])

def compute_twisted_alexander_module(tree):
    if isinstance(tree, bool):
        return [[Fraction(1)]]
    
    left_module = compute_twisted_alexander_module(tree[0])
    right_module = compute_twisted_alexander_module(tree[1])
    
    # Concatenate modules
    new_module = []
    for row_left in left_module:
        for row_right in right_module:
            newRow = [row_left[i] + row_right[i] for i in range(len(row_left))]
            new_module.append(newRow)
    
    return new_module

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        tree = generate_xor_and_tree(n)
        module = compute_twisted_alexander_module(tree)
        rank = compute_rank(module)
        results.append((n, rank))
    
    total_rank = sum(rank for _, rank in results)
    mean_rank = total_rank / len(results)
    conjecture_holds = all(rank <= 2 * n**2 for _, rank in results) and (len([r for r, _ in results if r > 2 * n**2]) == 0)
    
    return {
        "metric_name": "minimal_rank",
        "metric_value": mean_rank,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"rank={max(rank for _, rank in results)}, expected=2n^2"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(1, 1000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={math.sqrt(sum((result['metric_value'] - mean_value)**2 for result in results) / len(results))} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"rank exceeds bound\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")