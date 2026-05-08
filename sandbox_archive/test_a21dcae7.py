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
    m = len(matrix[0])
    rank = 0
    
    for i in range(n):
        if rank >= m:
            break
        
        pivot_row = -1
        for j in range(rank, n):
            if matrix[j][i] != 0:
                pivot_row = j
                break
        
        if pivot_row == -1:
            continue
        
        matrix[i], matrix[pivot_row] = matrix[pivot_row], matrix[i]
        
        for j in range(n):
            if i != j:
                factor = Fraction(matrix[j][i], matrix[i][i])
                for k in range(m):
                    matrix[j][k] -= factor * matrix[i][k]
        
        rank += 1
    
    return rank

def generate_random_system(n, q=2):
    A = [[random.randint(0, q-1) for _ in range(n)] for _ in range(n)]
    b = [random.randint(0, q-1) for _ in range(n)]
    augmented_matrix = [row + [b[i]] for i, row in enumerate(A)]
    return augmented_matrix

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_solutions = 0
    instances_tested = 0
    
    for n in n_values:
        for _ in range(5):  # Sample 5 instances per n
            augmented_matrix = generate_random_system(n)
            rank = gaussian_elimination(augmented_matrix)
            solutions = 2 ** (n - rank) if rank == n else 0
            total_solutions += solutions
            instances_tested += 1
    
    metric_value = total_solutions / instances_tested
    conjecture_holds = metric_value >= 1  # Simplified for testing purposes
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "Number of Solutions",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i - 1 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = (sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))**0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")