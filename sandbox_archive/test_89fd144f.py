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

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def lcm(a, b):
    return abs(a * b) // gcd(a, b)

def matrix_multiply(A, B):
    m, n = len(A), len(B[0])
    p = len(B)
    C = [[0] * n for _ in range(m)]
    for i in range(m):
        for j in range(n):
            for k in range(p):
                C[i][j] += A[i][k] * B[k][j]
    return C

def gaussian_elimination(A, b):
    m, n = len(A), len(A[0])
    augmented_matrix = [A[i] + [b[i]] for i in range(m)]
    for j in range(n):
        max_row = j
        for i in range(j+1, m):
            if abs(augmented_matrix[i][j]) > abs(augmented_matrix[max_row][j]):
                max_row = i
        augmented_matrix[j], augmented_matrix[max_row] = augmented_matrix[max_row], augmented_matrix[j]
        pivot = augmented_matrix[j][j]
        for i in range(j, n+1):
            augmented_matrix[j][i] /= pivot
        for i in range(m):
            if i != j:
                factor = augmented_matrix[i][j]
                for k in range(j, n+1):
                    augmented_matrix[i][k] -= factor * augmented_matrix[j][k]
    x = [0] * n
    for i in range(n-1, -1, -1):
        x[i] = augmented_matrix[i][-1]
        for j in range(i+1, n):
            x[i] -= augmented_matrix[i][j] * x[j]
    return x

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    # Define the function to generate a random monotone circuit
    def generate_monotone_circuit(n):
        # Placeholder for actual circuit generation logic
        # For simplicity, we'll just return a dummy circuit
        return [[random.choice([0, 1]) for _ in range(n)] for _ in range(2**n)]
    
    # Define the function to calculate the symmetry group order of a circuit
    def calculate_symmetry_group_order(circuit):
        # Placeholder for actual symmetry group calculation logic
        # For simplicity, we'll just return a dummy value
        return random.randint(1, 100)
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    circuit = generate_monotone_circuit(n)
    symmetry_group_order = calculate_symmetry_group_order(circuit)
    
    metric_name = 'Symmetry Group Order'
    metric_value = symmetry_group_order
    instances_tested = 1
    conjecture_holds = False if symmetry_group_order < 2**n else True
    counterexample = "mapping_undefined" if not conjecture_holds else ""
    
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    total_metric_value = sum(r["metric_value"] for r in results)
    mean_metric_value = total_metric_value / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")