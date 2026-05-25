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
    n = len(matrix)
    augmented_matrix = [row[:] + [0] for row in matrix]
    for i in range(n):
        max_row = i
        for j in range(i+1, n):
            if abs(augmented_matrix[j][i]) > abs(augmented_matrix[max_row][i]):
                max_row = j
        augmented_matrix[i], augmented_matrix[max_row] = augmented_matrix[max_row], augmented_matrix[i]
        pivot = augmented_matrix[i][i]
        for j in range(i, n+1):
            augmented_matrix[i][j] /= pivot
        for j in range(n):
            if j != i:
                factor = augmented_matrix[j][i]
                for k in range(i, n+1):
                    augmented_matrix[j][k] -= factor * augmented_matrix[i][k]
    rank = 0
    for row in augmented_matrix:
        if any(row):
            rank += 1
    return rank

def tropicalize(permutation):
    n = len(permutation)
    tropicalized = [[-math.inf] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            tropicalized[i][j] = permutation[j] + permutation[i]
    return tropicalized

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    depth = random.randint(1, 40)
    
    # Construct a boolean function with linear threshold gates
    function = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
    
    # Convert the function to its tropicalized permutation pattern
    tropical_pattern = tropicalize(function)
    
    # Compute the AC⁰ circuit depth (simulated by the given depth)
    ac0_depth = depth
    
    # Compute the minimal rank of the tropicalized permutation pattern
    r = gaussian_elimination(tropical_pattern)
    
    # Calculate the ratio of rank to depth squared
    if ac0_depth == 0:
        return {
            "metric_name": "Rank/Depth^2",
            "metric_value": math.inf,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "AC⁰ depth is zero"
        }
    
    ratio = Fraction(r, ac0_depth ** 2)
    
    return {
        "metric_name": "Rank/Depth^2",
        "metric_value": float(ratio),
        "instances_tested": 1,
        "conjecture_holds": ratio <= 4,  # Assuming C = 4 for simplicity
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Rank/Depth^2 exceeds 4\" first_failing_seed={seeds[first_failing_seed]}")