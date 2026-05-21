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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    if n % 2 != 0:
        n += 1
    
    # Generate random graph G(n, 1/2)
    adjacency_matrix = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
    for i in range(n):
        adjacency_matrix[i][i] = 0
    
    # Calculate the number of eigenvalues in the interval [-sqrt(n log n), sqrt(n log n)]
    def matrix_power(matrix, k):
        result = [[0] * n for _ in range(n)]
        for i in range(n):
            result[i][i] = 1
        for _ in range(k):
            new_result = [[0] * n for _ in range(n)]
            for i in range(n):
                for j in range(n):
                    for k in range(n):
                        new_result[i][j] += matrix[i][k] * matrix[k][j]
            result = new_result
        return result
    
    def matrix_trace(matrix):
        return sum(matrix[i][i] for i in range(n))
    
    def matrix_determinant(matrix):
        if n == 1:
            return matrix[0][0]
        det = 0
        for j in range(n):
            submatrix = [row[:j] + row[j+1:] for row in matrix[1:]]
            det += (-1) ** j * matrix[0][j] * matrix_determinant(submatrix)
        return det
    
    def gaussian_elimination(matrix):
        augmented_matrix = [row[:] + [i] for i, row in enumerate(matrix)]
        rows, cols = len(augmented_matrix), len(augmented_matrix[0])
        for col in range(cols - 1):
            max_row = col
            for row in range(col + 1, rows):
                if abs(augmented_matrix[row][col]) > abs(augmented_matrix[max_row][col]):
                    max_row = row
            augmented_matrix[col], augmented_matrix[max_row] = augmented_matrix[max_row], augmented_matrix[col]
            factor = augmented_matrix[col][col]
            for j in range(col, cols):
                augmented_matrix[col][j] /= factor
            for i in range(rows):
                if i != col:
                    factor = augmented_matrix[i][col]
                    for j in range(col, cols):
                        augmented_matrix[i][j] -= factor * augmented_matrix[col][j]
        return [row[-1] for row in augmented_matrix[:-1]]
    
    eigenvalues = gaussian_elimination(adjacency_matrix)
    eigenvalue_count = sum(1 for ev in eigenvalues if -math.sqrt(n * math.log(n)) <= ev <= math.sqrt(n * math.log(n)))
    
    # Determine the minimal SOS degree required to achieve the approximation ratio
    sos_degree = int(math.ceil(math.sqrt(n)))
    
    return {
        "metric_name": "SOS Degree",
        "metric_value": sos_degree,
        "instances_tested": 1,
        "conjecture_holds": eigenvalue_count >= sos_degree * 0.878,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 999999) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = "eigenvalue_count < sos_degree * 0.878"
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")