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

def random_boolean_function(n):
    return [random.choice([0, 1]) for _ in range(2**n)]

def ac0_circuit_depth(boolean_function):
    n = int(math.log2(len(boolean_function)))
    depth = [0] * len(boolean_function)
    
    for i in range(n):
        for j in range(2**i, 2**(i+1)):
            if boolean_function[j-1] == 1:
                max_depth = 0
                for k in range(j-2, -1, -1):
                    if boolean_function[k] == 1 and depth[k] > max_depth:
                        max_depth = depth[k]
                depth[j-1] = 1 + max_depth
    
    return depth

def tropicalized_permutation_pattern(boolean_function):
    n = int(math.log2(len(boolean_function)))
    pattern = []
    
    for i in range(n):
        row = [0] * len(boolean_function)
        for j in range(2**i, 2**(i+1)):
            if boolean_function[j-1] == 1:
                row[j-1] = 1
        pattern.append(row)
    
    return pattern

def rank(matrix):
    m, n = len(matrix), len(matrix[0])
    augmented_matrix = [row + [0] for row in matrix]
    pivot_row = 0
    
    for i in range(n):
        if pivot_row >= m:
            break
        
        max_pivot = -1
        max_index = -1
        for j in range(pivot_row, m):
            if abs(augmented_matrix[j][i]) > max_pivot:
                max_pivot = abs(augmented_matrix[j][i])
                max_index = j
        
        augmented_matrix[pivot_row], augmented_matrix[max_index] = augmented_matrix[max_index], augmented_matrix[pivot_row]
        
        for j in range(pivot_row + 1, m):
            factor = augmented_matrix[j][i] / augmented_matrix[pivot_row][i]
            for k in range(n + 1):
                augmented_matrix[j][k] -= factor * augmented_matrix[pivot_row][k]
        
        pivot_row += 1
    
    rank = sum(1 for row in augmented_matrix if any(abs(x) > 1e-9 for x in row))
    return rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        boolean_function = random_boolean_function(n)
        depth = ac0_circuit_depth(boolean_function)
        pattern = tropicalized_permutation_pattern(boolean_function)
        r = rank(pattern)
        
        if len(depth) == 0 or max(depth) == 0:
            return {
                "metric_name": "Ratio of Rank to Depth^2",
                "metric_value": None,
                "instances_tested": 1,
                "conjecture_holds": False,
                "counterexample": "Empty depth array"
            }
        
        ratio = r / (max(depth) ** 2)
        results.append(ratio)
    
    mean_ratio = sum(results) / len(results)
    std_ratio = math.sqrt(sum((x - mean_ratio) ** 2 for x in results) / len(results))
    
    return {
        "metric_name": "Ratio of Rank to Depth^2",
        "metric_value": mean_ratio,
        "instances_tested": len(n_values),
        "conjecture_holds": all(r <= 10 for r in results),  # Arbitrary constant C
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    if not sys.argv[1:]:
        seeds = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    else:
        seeds = list(map(int, sys.argv[1:]))
    
    results = []
    
    for seed in seeds:
        print(f"TRIAL: {run_trial(seed)}")
        results.append(run_trial(seed))
    
    mean_ratio = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_ratio = math.sqrt(sum((r["metric_value"] - mean_ratio) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std={std_ratio} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")