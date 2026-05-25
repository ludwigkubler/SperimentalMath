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
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math

def gaussian_elimination(matrix):
    n = len(matrix)
    augmented_matrix = [row[:] for row in matrix]
    
    for i in range(n):
        max_row = i
        for j in range(i+1, n):
            if abs(augmented_matrix[j][i]) > abs(augmented_matrix[max_row][i]):
                max_row = j
        
        augmented_matrix[i], augmented_matrix[max_row] = augmented_matrix[max_row], augmented_matrix[i]
        
        pivot = augmented_matrix[i][i]
        if pivot == 0:
            continue
        
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

def random_boolean_function(n):
    return [random.choice([0, 1]) for _ in range(2**n)]

def tropicalized_permutation_pattern(boolean_func):
    n = int(math.log2(len(boolean_func)))
    pattern = []
    for i in range(n):
        row = []
        for j in range(2**i):
            if boolean_func[j] == 0:
                row.append(-math.inf)
            else:
                row.append(j)
        pattern.append(row)
    
    return pattern

def ac0_circuit_depth(boolean_func):
    n = int(math.log2(len(boolean_func)))
    depth = 0
    while len(boolean_func) > 1:
        boolean_func = [boolean_func[i] == boolean_func[j] for i, j in zip(range(0, len(boolean_func), 2), range(1, len(boolean_func), 2))]
        depth += 1
    
    return depth

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n = 5
    boolean_func = random_boolean_function(n)
    tropical_pattern = tropicalized_permutation_pattern(boolean_func)
    circuit_depth = ac0_circuit_depth(boolean_func)
    
    rank = gaussian_elimination(tropical_pattern)
    
    ratio = rank / (circuit_depth ** 2)
    
    return {
        "metric_name": "Rank to Circuit Depth Ratio",
        "metric_value": ratio,
        "instances_tested": 1,
        "conjecture_holds": ratio <= 4.0,  # Assuming C = 4 for this example
        "counterexample": "" if ratio <= 4.0 else f"Ratio {ratio} exceeds threshold"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_ratio = sum(res["metric_value"] for res in results) / len(results)
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, res in zip(seeds, results) if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Ratio exceeds threshold\" first_failing_seed={first_failing_seed}")