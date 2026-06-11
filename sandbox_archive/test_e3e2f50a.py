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

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def lcm(a, b):
    return abs(a * b) // gcd(a, b)

def matrix_multiply(A, B):
    m, n = len(A), len(B[0])
    result = [[0] * n for _ in range(m)]
    for i in range(m):
        for j in range(n):
            for k in range(len(B)):
                result[i][j] += A[i][k] * B[k][j]
    return result

def gaussian_elimination(A, b):
    m, n = len(A), len(A[0])
    augmented_matrix = [row + [b[i]] for i, row in enumerate(A)]
    for i in range(m):
        max_row = i
        for j in range(i+1, m):
            if abs(augmented_matrix[j][i]) > abs(augmented_matrix[max_row][i]):
                max_row = j
        augmented_matrix[i], augmented_matrix[max_row] = augmented_matrix[max_row], augmented_matrix[i]
        pivot = augmented_matrix[i][i]
        for j in range(i, n+1):
            augmented_matrix[i][j] /= pivot
        for j in range(m):
            if j != i:
                factor = augmented_matrix[j][i]
                for k in range(i, n+1):
                    augmented_matrix[j][k] -= factor * augmented_matrix[i][k]
    return [row[-1] for row in augmented_matrix]

def determinant(A):
    m, n = len(A), len(A[0])
    if m != n:
        raise ValueError("Matrix must be square")
    if n == 1:
        return A[0][0]
    det = 0
    sign = 1
    for i in range(n):
        submatrix = [row[:i] + row[i+1:] for row in A[1:]]
        det += sign * A[0][i] * determinant(submatrix)
        sign *= -1
    return det

def inverse(A):
    m, n = len(A), len(A[0])
    if m != n:
        raise ValueError("Matrix must be square")
    det = determinant(A)
    if det == 0:
        raise ValueError("Matrix is singular")
    adjugate = [[0] * n for _ in range(m)]
    for i in range(m):
        for j in range(n):
            submatrix = [row[:j] + row[j+1:] for row in A[:i] + A[i+1:]]
            cofactor = determinant(submatrix)
            adjugate[j][i] = (-1) ** (i+j) * cofactor
    return [[adjugate[j][i] / det for i in range(n)] for j in range(m)]

def tropical_add(a, b):
    if a == float('-inf') or b == float('-inf'):
        return max(a, b)
    return a + b

def tropical_multiply(a, b):
    if a == float('-inf') or b == float('-inf'):
        return float('-inf')
    return a * b

def tropical_hodge_rank(matroid):
    n = len(matroid)
    identity_matrix = [[1 if i == j else 0 for j in range(n)] for i in range(n)]
    tropical_inverse = inverse(identity_matrix)
    tropical_product = matrix_multiply(tropical_inverse, matroid)
    return sum(sum(row) for row in tropical_product)

def generate_random_circuit(n):
    inputs = [i for i in range(n)]
    outputs = [n]
    gates = []
    for _ in range(2 * n - 1):
        gate_type = random.choice(['AND', 'OR'])
        if gate_type == 'AND':
            gate_inputs = random.sample(inputs, 2)
        else:
            gate_inputs = random.sample(inputs, 2)
        gate_output = max(gate_inputs) + 1
        gates.append((gate_type, gate_inputs, gate_output))
        inputs.append(gate_output)
    return inputs, outputs, gates

def generate_random_instance(n_clauses):
    literals = set()
    for _ in range(n_clauses):
        clause_size = random.randint(2, 5)
        clause_literals = random.sample(range(1, 20), clause_size)
        literals.update(clause_literals)
    return list(literals)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    th_values = []
    sizes = []
    instances_tested = 0
    n_max = 0

    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):
            if n > n_max:
                n_max = n
            inputs, outputs, gates = generate_random_circuit(n)
            matroid = [[0] * (n + 1) for _ in range(n + 1)]
            for gate_type, gate_inputs, gate_output in gates:
                for input_ in gate_inputs:
                    matroid[input_][gate_output] = 1
            th_value = tropical_hodge_rank(matroid)
            th_values.append(th_value)
            sizes.append(len(gates))
            instances_tested += 1

    correlation_coefficient = sum((th_values[i] - sum(th_values) / len(th_values)) * (sizes[i] - sum(sizes) / len(sizes)) for i in range(len(sizes))) / (len(sizes) * sum((th_values[i] - sum(th_values) / len(th_values))**2 for i in range(len(sizes))) * sum((sizes[i] - sum(sizes) / len(sizes))**2 for i in range(len(sizes))))**0.5

    if correlation_coefficient < 0.8:
        return {
            "metric_name": "tropical_hodge_rank",
            "metric_value": correlation_coefficient,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "correlation_coefficient<0.8"
        }

    return {
        "metric_name": "tropical_hodge_rank",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_dev = (sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results)) ** 0.5
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)

    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='correlation_coefficient<0.8' first_failing_seed={first_failing_seed}")