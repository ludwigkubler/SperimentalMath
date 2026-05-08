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

def generate_disjointness_matrix(n):
    matrix = [[0] * (2**n) for _ in range(2**n)]
    for i in range(n):
        row, col = random.randint(0, 2**n - 1), random.randint(0, 2**n - 1)
        while matrix[row][col] == 1:
            row, col = random.randint(0, 2**n - 1), random.randint(0, 2**n - 1)
        matrix[row][col] = 1
    return matrix

def rank(matrix):
    n = len(matrix)
    augmented_matrix = [row + [0] for row in matrix]
    for i in range(n):
        augmented_matrix[i][i+n] = 1
    
    def swap_rows(a, b):
        augmented_matrix[a], augmented_matrix[b] = augmented_matrix[b], augmented_matrix[a]
    
    def scale_row(row, scalar):
        augmented_matrix[row] = [scalar * x for x in augmented_matrix[row]]
    
    def add_scaled_row(a, b, scalar):
        augmented_matrix[a] = [a + scalar * b for a, b in zip(augmented_matrix[a], augmented_matrix[b])]
    
    for i in range(n):
        if augmented_matrix[i][i] == 0:
            for j in range(i+1, n):
                if augmented_matrix[j][i] != 0:
                    swap_rows(i, j)
                    break
            else:
                continue
        
        scale_row(i, 1 / augmented_matrix[i][i])
        
        for j in range(n):
            if i != j:
                add_scaled_row(j, i, -augmented_matrix[j][i])
    
    rank = sum(1 for row in augmented_matrix[:n] if any(x != 0 for x in row))
    return rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = 40
    matrix = generate_disjointness_matrix(n)
    secant_dimension = rank(matrix) - 1
    conjecture_holds = secant_dimension >= 0.2 * n
    counterexample = "" if conjecture_holds else f"dim(sec(M))={secant_dimension}, expected ≥{0.2*n}"
    
    return {
        "metric_name": "secant_dimension",
        "metric_value": secant_dimension,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2**i + 1 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean = sum(r["metric_value"] for r in results) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean} std={std_dev} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE no_counterexamples")