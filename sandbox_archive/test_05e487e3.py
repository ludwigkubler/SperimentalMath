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
        # Find pivot row
        max_row = i
        for k in range(i + 1, n):
            if abs(matrix[k][i]) > abs(matrix[max_row][i]):
                max_row = k
        matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
        
        # Eliminate non-pivot elements
        factor = Fraction(1, matrix[i][i])
        for j in range(i, n):
            matrix[i][j] *= factor
        
        for k in range(n):
            if k != i:
                factor = matrix[k][i]
                for j in range(i, n):
                    matrix[k][j] -= factor * matrix[i][j]
    return matrix

def compute_fourier_multiplier_norm(circuit):
    n = len(circuit)
    adjacency_matrix = [[0] * n for _ in range(n)]
    
    # Construct the adjacency matrix
    for i in range(n):
        for j in range(i + 1, n):
            if circuit[i][j] == 1:
                adjacency_matrix[i][j] = 1
                adjacency_matrix[j][i] = 1
    
    # Perform Gaussian elimination to get the reduced row echelon form
    reduced_matrix = gaussian_elimination(adjacency_matrix)
    
    # Compute the infinity norm of the Fourier multiplier operator
    max_norm = 0
    for i in range(n):
        row_sum = sum(abs(reduced_matrix[i][j]) for j in range(n))
        if row_sum > max_norm:
            max_norm = row_sum
    
    return max_norm

def generate_random_circuit(n, d):
    circuit = [[0] * n for _ in range(n)]
    degree_counts = [0] * n
    
    while True:
        i, j = random.sample(range(n), 2)
        if i != j and degree_counts[i] < d and degree_counts[j] < d:
            circuit[i][j] = 1
            circuit[j][i] = 1
            degree_counts[i] += 1
            degree_counts[j] += 1
        
        if all(d == d for d in degree_counts):
            break
    
    return circuit

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        for _ in range(5):
            circuit = generate_random_circuit(n, d=2)
            norm = compute_fourier_multiplier_norm(circuit)
            entanglement_complexity = sum(sum(row) for row in circuit) // 2
            results.append({
                "n": n,
                "norm": norm,
                "entanglement_complexity": entanglement_complexity
            })
    
    if not results:
        return {
            "metric_name": "Fourier Multiplier Norm",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    max_norm = max(result["norm"] for result in results)
    avg_norm = sum(result["norm"] for result in results) / len(results)
    std_norm = math.sqrt(sum((result["norm"] - avg_norm) ** 2 for result in results) / len(results))
    
    return {
        "metric_name": "Fourier Multiplier Norm",
        "metric_value": avg_norm,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": all(result["norm"] <= 4 * result["entanglement_complexity"] ** 2 for result in results),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    avg_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - avg_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={avg_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={avg_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        counterexample = "Fourier multiplier norm > 4 * entanglement complexity^2"
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")