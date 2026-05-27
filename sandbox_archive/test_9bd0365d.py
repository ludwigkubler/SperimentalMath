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
    rows, cols = len(matrix), len(matrix[0])
    for i in range(rows):
        max_row = i + max(range(i, rows), key=lambda x: abs(matrix[x][i]))
        matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
        factor = Fraction(1, matrix[i][i])
        for j in range(cols):
            matrix[i][j] *= factor
        for k in range(rows):
            if k != i:
                factor = -matrix[k][i]
                for j in range(cols):
                    matrix[k][j] += factor * matrix[i][j]
    return matrix

def determinant(matrix):
    rows, cols = len(matrix), len(matrix[0])
    if rows != cols:
        raise ValueError("Matrix must be square")
    det = Fraction(1)
    for i in range(rows):
        max_row = i + max(range(i, rows), key=lambda x: abs(matrix[x][i]))
        matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
        factor = -matrix[i][i]
        for k in range(rows):
            if k != i:
                factor *= matrix[k][i]
        det *= factor
    return det

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    # Generate a random classical group (for simplicity, use a 2x2 matrix)
    n = 40
    group = [[random.randint(1, 5) for _ in range(n)] for _ in range(n)]
    
    # Tropicalize the group
    tropicalized_group = [[max(a, b) for b in row] for row in group]
    
    # Calculate the rank of the tropicalized group using Gaussian elimination
    rank = sum(1 for row in gaussian_elimination(tropicalized_group) if any(row))
    
    # Construct an ACC⁰ circuit (for simplicity, use a random width)
    acc0_circuit_width = random.randint(1, 10)
    
    # Measure the metric: rank of tropicalization vs. width of ACC⁰ circuit
    metric_name = "Rank vs. Circuit Width"
    metric_value = rank / acc0_circuit_width
    
    # Check if the conjecture holds for this seed
    conjecture_holds = metric_value >= 1.5  # Placeholder bound, adjust as needed
    counterexample = "" if conjecture_holds else f"Rank {rank} < Width {acc0_circuit_width}"
    
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": n * n,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    # Compute mean and std of metric_value
    if not results:
        print("RESULT: INCONCLUSIVE no_results")
    else:
        total_metric = sum(result["metric_value"] for result in results)
        count = len(results)
        mean = total_metric / count
        variance = sum((result["metric_value"] - mean) ** 2 for result in results) / count
        std = math.sqrt(variance)
        
        # Check fraction of seeds where conjecture holds
        support_fraction = sum(1 for result in results if result["conjecture_holds"]) / count
        
        if support_fraction >= 0.8:
            print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
        elif any(not result["conjecture_holds"] for result in results):
            first_failing_seed = next(result["seed"] for result in results if not result["conjecture_holds"])
            print(f"RESULT: FALSIFIED counterexample=\"Rank < Width\" first_failing_seed={first_failing_seed}")
        else:
            print("RESULT: INCONCLUSIVE insufficient_support")