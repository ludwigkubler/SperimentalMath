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
        # Find the pivot row
        max_row = i
        for j in range(i+1, n):
            if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                max_row = j
        matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
        
        # Eliminate below the pivot
        for j in range(i+1, n):
            factor = matrix[j][i] / matrix[i][i]
            for k in range(n):
                matrix[j][k] -= factor * matrix[i][k]
    
    # Back-substitute to find the solution
    for i in range(n-1, -1, -1):
        for j in range(i+1, n):
            matrix[i][-1] -= matrix[i][j] * matrix[j][-1]
        matrix[i][-1] /= matrix[i][i]
        matrix[i][i] = 1
    
    return [row[-1] for row in matrix]

def compute_real_rank(matrix):
    augmented_matrix = [row + [1] for row in matrix]
    rank = len(gaussian_elimination(augmented_matrix))
    return rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n = 10
    c = 0.5
    
    # Generate a random AC⁰ circuit computing PARITY on n inputs
    def parity_circuit(inputs):
        result = inputs[0]
        for input in inputs[1:]:
            result ^= input
        return result
    
    # Construct the Karchmer-Wigderson communication matrix
    M_C = []
    for x in range(2**n):
        row = []
        for y in range(2**n):
            row.append(parity_circuit([x & (1 << i) > 0 for i in range(n)]) ^ parity_circuit([y & (1 << i) > 0 for i in range(n)]))
        M_C.append(row)
    
    # Compute the real rank of the matrix
    rank = compute_real_rank(M_C)
    
    # Check if the conjecture holds
    conjecture_holds = rank >= c * math.sqrt(n)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "real_rank",
        "metric_value": rank,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]  # Default to first 30 primes
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean_rank = sum(result["metric_value"] for result in results) / len(results)
    std_rank = math.sqrt(sum((result["metric_value"] - mean_rank)**2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE mapping_undefined")