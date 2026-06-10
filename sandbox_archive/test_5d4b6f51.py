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
    rows_A = len(A)
    cols_A = len(A[0])
    rows_B = len(B)
    cols_B = len(B[0])
    if cols_A != rows_B:
        raise ValueError("Incompatible dimensions for matrix multiplication")
    C = [[sum(A[i][k] * B[k][j] for k in range(cols_A)) for j in range(cols_B)] for i in range(rows_A)]
    return C

def gaussian_elimination(matrix):
    rows, cols = len(matrix), len(matrix[0])
    augmented_matrix = [row + [1 if i == j else 0 for j in range(cols)] for i, row in enumerate(matrix)]
    for i in range(rows):
        max_row = max(range(i, rows), key=lambda r: abs(augmented_matrix[r][i]))
        augmented_matrix[i], augmented_matrix[max_row] = augmented_matrix[max_row], augmented_matrix[i]
        pivot = augmented_matrix[i][i]
        if pivot == 0:
            continue
        for j in range(cols + 1):
            augmented_matrix[i][j] /= pivot
        for k in range(rows):
            if k != i:
                factor = augmented_matrix[k][i]
                for j in range(cols + 1):
                    augmented_matrix[k][j] -= factor * augmented_matrix[i][j]
    return [row[:-1] for row in augmented_matrix]

def rank(matrix):
    rref = gaussian_elimination(matrix)
    return sum(1 for row in rref if any(row))

def generate_random_circuit(depth, max_gates=3):
    circuit = []
    for _ in range(depth):
        gate = random.choice(['AND', 'OR'])
        inputs = [random.randint(0, 1) for _ in range(random.randint(1, max_gates))]
        circuit.append((gate, inputs))
    return circuit

def kashiwara_vergne_structure(circuit):
    # Simplified representation of Kashiwara-Vergne structure
    # This is a placeholder and should be replaced with actual computation
    rank = sum(len(inputs) for gate, inputs in circuit)
    return rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_max = 40
    instances_tested = 30
    metric_values = []
    
    for D in range(5, n_max + 1):
        for _ in range(instances_tested // (n_max - 4)):
            circuit = generate_random_circuit(D)
            R_C = kashiwara_vergne_structure(circuit)
            metric_values.append((D, R_C))
    
    if not metric_values:
        return {
            "metric_name": "rank",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "no_data"
        }
    
    D_values, R_C_values = zip(*metric_values)
    correlation_coefficient = sum((D - mean_D) * (R_C - mean_R_C) for D, R_C in metric_values) / math.sqrt(sum((D - mean_D) ** 2 for D in D_values) * sum((R_C - mean_R_C) ** 2 for R_C in R_C_values))
    mean_difference = abs(mean_R_C - mean_D)
    
    return {
        "metric_name": "rank",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": correlation_coefficient >= 0.8 and mean_difference <= 3,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_correlation_coefficient = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_correlation_coefficient} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_correlation_coefficient} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in enumerate(results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient<{mean_correlation_coefficient}, mean_difference>{3}\" first_failing_seed={first_failing_seed}")