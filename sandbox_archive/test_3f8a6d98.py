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

# Define a function to perform Gaussian elimination on a matrix
def gaussian_elimination(matrix):
    n = len(matrix)
    for i in range(n):
        # Find the pivot row
        max_row = i
        for j in range(i+1, n):
            if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                max_row = j
        # Swap rows
        matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
        
        # Eliminate non-pivot elements below the pivot
        for j in range(i+1, n):
            factor = Fraction(matrix[j][i], matrix[i][i])
            for k in range(n):
                matrix[j][k] -= factor * matrix[i][k]

    return matrix

# Define a function to compute the rank of a matrix using Gaussian elimination
def matrix_rank(matrix):
    n = len(matrix)
    rank = 0
    for i in range(n):
        if all(abs(matrix[i][j]) < 1e-9 for j in range(n)):
            continue
        rank += 1
        for j in range(i+1, n):
            factor = Fraction(matrix[j][i], matrix[i][i])
            for k in range(n):
                matrix[j][k] -= factor * matrix[i][k]
    return rank

# Define a function to generate a random instance of an n-communication protocol
def generate_protocol(n):
    # This is a placeholder function. Replace with actual protocol generation logic.
    return [[random.randint(0, 1) for _ in range(n)] for _ in range(n)]

# Define the main trial function
def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    total_metric_value = [0] * 6  # For n=5,10,15,20,30,40
    instances_tested = 0
    n_max = 0
    
    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):  # Test each size with 5 different instances
            protocol = generate_protocol(n)
            matrix = []
            for row in protocol:
                matrix.append([Fraction(row[j]) for j in range(n)])
            
            rank = matrix_rank(matrix)
            total_metric_value[n-5] += rank
            instances_tested += 1
            n_max = max(n_max, n)
    
    mean_metric_value = [total_metric_value[i] / 30 for i in range(6)]
    std_metric_value = [math.sqrt(sum((total_metric_value[i] - mean_metric_value[i]) ** 2 for _ in range(30)) / 29) if instances_tested > 0 else 0 for i in range(6)]
    
    conjecture_holds = all(mean_metric_value[i] <= (i+5) * math.log(i+5, 2) for i in range(6))
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "semialgebra_rank",
        "metric_value": mean_metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"n_max\": {result['n_max']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean_metric_value = [sum(r['metric_value'][i] for r in results) / len(results) for i in range(6)]
    std_metric_value = [math.sqrt(sum((r['metric_value'][i] - mean_metric_value[i]) ** 2 for r in results) / (len(results) - 1)) if len(results) > 0 else 0 for i in range(6)]
    support_fraction = sum(r['conjecture_holds'] for r in results) / len(results)
    
    if all(r['conjecture_holds'] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r['conjecture_holds'] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result['conjecture_holds'])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")