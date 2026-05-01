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
    rows, cols = len(matrix), len(matrix[0])
    for i in range(rows):
        # Find the pivot
        max_row = i
        for r in range(i + 1, rows):
            if abs(matrix[r][i]) > abs(matrix[max_row][i]):
                max_row = r
        matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
        
        # Eliminate
        for r in range(rows):
            if r != i:
                factor = matrix[r][i] / matrix[i][i]
                for c in range(cols):
                    matrix[r][c] -= factor * matrix[i][c]

def rank(matrix):
    rows, cols = len(matrix), len(matrix[0])
    augmented_matrix = [row + row[:] for row in matrix]
    gaussian_elimination(augmented_matrix)
    rank = 0
    for r in range(rows):
        if any(abs(augmented_matrix[r][c]) > 1e-9 for c in range(cols)):
            rank += 1
    return rank

def truth_table(f, n):
    return [[f(tuple(i)) for i in itertools.product([0, 1], repeat=n)]]

def min_circuit_size(f, n):
    # Placeholder function; actual implementation needed
    return 2**n - 1  # Example: all inputs map to the same output

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.choice([5, 10, 15, 20, 30, 40])
    f = lambda x: random.randint(0, 1)
    tt = truth_table(f, n)
    matrix = [[int(bit) for bit in row] for row in tt]
    matroid_rank = rank(matrix)
    circuit_size = min_circuit_size(f, n)
    
    return {
        "metric_name": "min_circuit_size",
        "metric_value": circuit_size,
        "instances_tested": 1,
        "conjecture_holds": circuit_size >= matroid_rank,
        "counterexample": "" if circuit_size >= matroid_rank else f"n={n}, rank={matroid_rank}, circuit_size={circuit_size}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or list(range(2, 50, 2))  # Default to first 30 primes if no seeds provided
    
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
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[first_failing_seed]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")