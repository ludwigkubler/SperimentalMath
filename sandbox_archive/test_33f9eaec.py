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
    for i in range(n):
        # Find pivot
        max_row = i
        for j in range(i+1, n):
            if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                max_row = j
        matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
        
        # Eliminate below the pivot
        factor = Fraction(1, matrix[i][i])
        for j in range(i, n):
            matrix[i][j] *= factor
        
        for k in range(n):
            if k != i:
                factor = matrix[k][i]
                for j in range(i, n):
                    matrix[k][j] -= factor * matrix[i][j]
    return matrix

def field_rank(matrix):
    reduced_matrix = gaussian_elimination(matrix)
    rank = 0
    for row in reduced_matrix:
        if any(row[j] != 0 for j in range(len(row))):
            rank += 1
    return rank

def communication_complexity(f, n):
    inputs = [(i >> j) & 1 for i in range(2**n) for j in range(n)]
    outputs = [f(inputs[i]) for i in range(2**n)]
    matrix = [[0] * (2**n) for _ in range(2**n)]
    for i in range(2**n):
        for j in range(2**n):
            if inputs[i] & inputs[j] == 0:
                matrix[i][j] = outputs[i] ^ outputs[j]
    return sum(abs(matrix[i][j]) for i in range(2**n) for j in range(i+1, 2**n)) / (2**(2*n-2))

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        f = lambda x: random.choice([0, 1])
        C = communication_complexity(f, n)
        rank = field_rank([[C[i][j] for j in range(2**n)] for i in range(2**n)])
        
        results.append({
            "n": n,
            "communication_complexity": C,
            "field_rank": rank
        })
    
    mean_rank = sum(result["field_rank"] for result in results) / len(results)
    std_rank = math.sqrt(sum((result["field_rank"] - mean_rank)**2 for result in results) / len(results))
    
    support_fraction = sum(1 for result in results if abs(result["field_rank"] - result["communication_complexity"]**2) <= 3 * std_rank) / len(results)
    
    return {
        "metric_name": "Brauer group rank",
        "metric_value": mean_rank,
        "instances_tested": len(results),
        "n_max": max(result["n"] for result in results),
        "conjecture_holds": support_fraction >= 0.8,
        "counterexample": "" if support_fraction >= 0.8 else f"support_fraction={support_fraction}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(sys.argv[1])] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
    
    results = [run_trial(seed) for seed in seeds]
    mean_rank = sum(result["metric_value"] for result in results) / len(results)
    std_rank = math.sqrt(sum((result["metric_value"] - mean_rank)**2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if abs(result["metric_value"] - result["n_max"]**2) <= 3 * std_rank) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"support_fraction={support_fraction}\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction}")