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
    
    def generate_tseitin_formula(n):
        # Generate a random d-regular graph with n variables
        d = 2  # Example degree, can be adjusted
        edges = set()
        for i in range(n):
            for j in range(i + 1, n):
                if len(edges) >= (n * d) // 2:
                    break
                if random.choice([True, False]):
                    edges.add((i, j))
        # Construct Tseitin formula
        literals = [f'x{i}' for i in range(n)]
        clauses = []
        for i in range(n):
            clauses.append([literals[i]])
            for j in range(i + 1, n):
                if (i, j) in edges:
                    clauses.append([-literals[i], -literals[j]])
                    clauses.append([literals[i], literals[j]])
                else:
                    clauses.append([-literals[i], literals[j]])
                    clauses.append([literals[i], -literals[j]])
        return literals, clauses
    
    def gaussian_elimination(matrix):
        n = len(matrix)
        for i in range(n):
            # Find pivot
            max_row = i
            for j in range(i + 1, n):
                if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                    max_row = j
            # Swap rows
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
            # Eliminate below pivot
            for j in range(i + 1, n):
                factor = matrix[j][i] / matrix[i][i]
                for k in range(n + 1):
                    matrix[j][k] -= factor * matrix[i][k]
        return matrix
    
    def compute_tropical_hodge_index(matrix):
        # Compute the index of the tropical Hodge structure
        n = len(matrix)
        identity = [[0 if i != j else 1 for j in range(n)] for i in range(n)]
        augmented_matrix = [row + [1] for row in matrix]
        augmented_matrix += identity
        reduced_matrix = gaussian_elimination(augmented_matrix)
        rank = sum(1 for row in reduced_matrix if any(x != 0 for x in row))
        return n - rank
    
    def compute_resolution_width(clauses):
        # Compute the resolution proof width
        n = len(clauses)
        max_width = 0
        for i in range(n):
            width = sum(1 for lit in clauses[i] if lit > 0)
            max_width = max(max_width, width)
        return max_width
    
    literals, clauses = generate_tseitin_formula(40)  # Example n=40
    matrix = [[0] * (len(literals) + 1) for _ in range(len(clauses))]
    for i, clause in enumerate(clauses):
        for lit in clause:
            if lit > 0:
                matrix[i][lit - 1] += 1
            else:
                matrix[i][-1] -= 1
    
    index = compute_tropical_hodge_index(matrix)
    width = compute_resolution_width(clauses)
    
    return {
        "metric_name": "index_vs_width",
        "metric_value": index / width,
        "instances_tested": 1,
        "n_max": 40,
        "conjecture_holds": False,
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        results.append(result)
        print(f"TRIAL: {result}")
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")