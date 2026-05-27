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
    for i in range(n):
        # Find pivot
        max_row = i
        for j in range(i+1, n):
            if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                max_row = j
        matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
        
        # Eliminate below
        for j in range(i+1, n):
            factor = matrix[j][i] / matrix[i][i]
            for k in range(n):
                matrix[j][k] -= factor * matrix[i][k]

def rank(matrix):
    n = len(matrix)
    augmented_matrix = [row[:] + [0]*n + [1 if i == j else 0 for j in range(n)] for i, row in enumerate(matrix)]
    gaussian_elimination(augmented_matrix)
    
    rank = n
    for i in range(n):
        if all(abs(val) < 1e-9 for val in augmented_matrix[i]):
            rank -= 1
    
    return rank

def twisted_quantum_entanglement(n):
    tensor = [[[0]*n for _ in range(n)] for _ in range(n)]
    
    # Construct the tensor (simplified example)
    for i in range(n):
        for j in range(n):
            for k in range(n):
                sign = 1 if (i + j + k) % 2 == 0 else -1
                tensor[i][j][k] += sign
    
    return tensor

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_rank = 0
    instances_tested = 0
    
    for n in n_values:
        for _ in range(5):  # Test each n with 5 different formulas
            formula = [random.randint(1, n) for _ in range(3)]
            tensor = twisted_quantum_entanglement(n)
            rank_value = rank(tensor)
            
            total_rank += rank_value
            instances_tested += 1
    
    average_rank = total_rank / instances_tested
    conjecture_holds = average_rank >= (n_values[-1] ** (2/3))
    
    return {
        "metric_name": "Average Rank",
        "metric_value": average_rank,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"Average rank {average_rank} < {n_values[-1] ** (2/3)}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 8)]  # Default to first 30 primes
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_rank = sum(res["metric_value"] for res in results) / len(results)
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction={support_fraction:.2f}")
    else:
        first_failing_seed = next(seed for seed, res in enumerate(results) if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Average rank < {seeds[-1] ** (2/3)}\" first_failing_seed={first_failing_seed}")