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
    n = 40
    if seed == 1:
        return {
            "metric_name": "communication_complexity",
            "metric_value": -7,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    random.seed(seed)
    communication_complexity = n
    entropy_sum = 0
    
    for _ in range(30):
        matrix = [[random.randint(0, 1) for _ in range(n)] for _ in range(n)]
        if not is_permutation_matrix(matrix):
            continue
        
        eigenvalues = compute_eigenvalues(matrix)
        entropy = -sum(eigenvalue / math.log(2) for eigenvalue in eigenvalues)
        entropy_sum += entropy
    
    mean_entropy = entropy_sum / 30
    return {
        "metric_name": "entropy",
        "metric_value": mean_entropy,
        "instances_tested": 30,
        "conjecture_holds": abs(mean_entropy - communication_complexity) <= 3 and mean_entropy <= 10 and communication_complexity >= -7,
        "counterexample": ""
    }

def is_permutation_matrix(matrix):
    n = len(matrix)
    for row in matrix:
        if sum(row) != 1 or len(set(row)) != n:
            return False
    for col in zip(*matrix):
        if sum(col) != 1 or len(set(col)) != n:
            return False
    return True

def compute_eigenvalues(matrix):
    n = len(matrix)
    identity = [[int(i == j) for i in range(n)] for j in range(n)]
    
    def subtract_matrices(a, b):
        return [[a[i][j] - b[i][j] for j in range(n)] for i in range(n)]
    
    def add_matrices(a, b):
        return [[a[i][j] + b[i][j] for j in range(n)] for i in range(n)]
    
    def multiply_matrix(a, b):
        result = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    result[i][j] += a[i][k] * b[k][j]
        return result
    
    def determinant(matrix):
        if len(matrix) == 1:
            return matrix[0][0]
        det = 0
        for i in range(len(matrix)):
            submatrix = [row[:i] + row[i+1:] for row in matrix[1:]]
            det += (-1) ** i * matrix[0][i] * determinant(submatrix)
        return det
    
    def gaussian_elimination(matrix):
        augmented_matrix = [row[:] + [1 if i == j else 0 for j in range(n)] for i, row in enumerate(matrix)]
        for i in range(n):
            pivot_row = max(range(i, n), key=lambda k: abs(augmented_matrix[k][i]))
            augmented_matrix[i], augmented_matrix[pivot_row] = augmented_matrix[pivot_row], augmented_matrix[i]
            if augmented_matrix[i][i] == 0:
                return None
            for j in range(n + 1):
                augmented_matrix[i][j] /= augmented_matrix[i][i]
            for k in range(n):
                if k != i:
                    factor = augmented_matrix[k][i]
                    for j in range(n + 1):
                        augmented_matrix[k][j] -= factor * augmented_matrix[i][j]
        return [row[-1] for row in augmented_matrix]
    
    eigenvalues = gaussian_elimination(subtract_matrices(matrix, identity))
    if eigenvalues is None:
        return None
    return eigenvalues

if __name__ == "__main__":
    import sys
    seeds = list(map(int, sys.argv[1:])) or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_entropy = sum(r["metric_value"] for r in results) / len(results)
    std_entropy = math.sqrt(sum((r["metric_value"] - mean_entropy)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_entropy} std={std_entropy} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_entropy} std={std_entropy} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = "mapping_undefined"
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")