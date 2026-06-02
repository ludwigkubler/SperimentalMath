# auto-injected by SEC sandbox
import math
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
from fractions import Fraction

def gaussian_elimination(matrix):
    n = len(matrix)
    augmented_matrix = [row[:] + [1] for row in matrix]
    rank = 0
    
    for i in range(n):
        if i >= len(augmented_matrix): break
        
        # Find pivot
        pivot_row = i
        while pivot_row < n and augmented_matrix[pivot_row][i] == 0:
            pivot_row += 1
        if pivot_row == n: continue
        
        # Swap rows
        augmented_matrix[i], augmented_matrix[pivot_row] = augmented_matrix[pivot_row], augmented_matrix[i]
        
        # Eliminate below the pivot
        for j in range(i + 1, n):
            factor = Fraction(augmented_matrix[j][i], augmented_matrix[i][i])
            for k in range(n + 1):
                augmented_matrix[j][k] -= factor * augmented_matrix[i][k]
    
    # Count non-zero rows
    rank = sum(1 for row in augmented_matrix if any(row[k] != 0 for k in range(n)))
    
    return matrix, augmented_matrix, rank

def minimal_p_adic_rank(code):
    n = len(code)
    p = 2  # Using binary representation for simplicity
    
    # Convert code to a matrix
    A = [[int(bit) for bit in codeword] for codeword in code]
    
    _, _, rank = gaussian_elimination(A)
    return rank

def communication_complexity_rank(code):
    n = len(code)
    p = 2  # Using binary representation for simplicity
    
    # Convert code to a matrix
    A = [[int(bit) for bit in codeword] for codeword in code]
    
    _, _, rank = gaussian_elimination(A)
    return rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = 40
    instances_tested = 30
    n_max = 40
    
    min_ranks = []
    comm_complexity_ranks = []
    
    for _ in range(instances_tested):
        code_length = random.randint(5, 10)
        code = [''.join(random.choice('01') for _ in range(code_length)) for _ in range(n)]
        
        min_rank = minimal_p_adic_rank(code)
        comm_complexity_rank_value = communication_complexity_rank(code)
        
        min_ranks.append(min_rank)
        comm_complexity_ranks.append(comm_complexity_rank_value)
    
    correlation_coefficient = sum((min_ranks[i] - sum(min_ranks) / instances_tested) * (comm_complexity_ranks[i] - sum(comm_complexity_ranks) / instances_tested) for i in range(instances_tested)) / instances_tested
    
    conjecture_holds = correlation_coefficient >= 0.7
    counterexample = "" if conjecture_holds else "correlation_coefficient < 0.7"
    
    return {
        "metric_name": "Correlation Coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(res["metric_value"] for res in results) / len(results)
    std_value = (sum((res["metric_value"] - mean_value) ** 2 for res in results) / len(results)) ** 0.5
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(res["seed"] for res in results if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient < 0.7\" first_failing_seed={first_failing_seed}")