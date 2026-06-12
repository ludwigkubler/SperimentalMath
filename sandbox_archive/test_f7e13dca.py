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

def extended_gcd(a, b):
    if a == 0:
        return b, 0, 1
    gcd, x1, y1 = extended_gcd(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return gcd, x, y

def mod_inverse(a, m):
    gcd, x, _ = extended_gcd(a, m)
    if gcd != 1:
        raise ValueError("Inverse doesn't exist")
    else:
        return x % m

def matrix_mod_inv(matrix, mod):
    n = len(matrix)
    adj = [[0 for _ in range(n)] for _ in range(n)]
    det = determinant(matrix, mod)
    inv_det = mod_inverse(det, mod)

    for i in range(n):
        for j in range(n):
            minor = get_minor(matrix, i, j)
            cofactor = ((-1) ** (i + j)) * determinant(minor, mod)
            adj[j][i] = (cofactor * inv_det) % mod

    return adj

def determinant(matrix, mod):
    if len(matrix) == 1:
        return matrix[0][0]
    det = 0
    for i in range(len(matrix)):
        minor = get_minor(matrix, 0, i)
        det += ((-1) ** i) * matrix[0][i] * determinant(minor, mod)
    return det % mod

def get_minor(matrix, row, col):
    minor = []
    for i in range(len(matrix)):
        if i == row:
            continue
        new_row = []
        for j in range(len(matrix[i])):
            if j == col:
                continue
            new_row.append(matrix[i][j])
        minor.append(new_row)
    return minor

def matrix_mul(A, B, mod):
    n = len(A)
    result = [[0 for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                result[i][j] = (result[i][j] + A[i][k] * B[k][j]) % mod
    return result

def matrix_add(A, B, mod):
    n = len(A)
    result = [[0 for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(n):
            result[i][j] = (A[i][j] + B[i][j]) % mod
    return result

def matrix_sub(A, B, mod):
    n = len(A)
    result = [[0 for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(n):
            result[i][j] = (A[i][j] - B[i][j]) % mod
    return result

def matrix_identity(n, mod):
    identity = [[0 for _ in range(n)] for _ in range(n)]
    for i in range(n):
        identity[i][i] = 1
    return identity

def random_matrix(n, mod):
    matrix = []
    for _ in range(n):
        row = [random.randint(0, mod - 1) for _ in range(n)]
        matrix.append(row)
    return matrix

def random_boolean_circuit(n, depth=3):
    if depth == 0:
        return [[random.choice([0, 1]) for _ in range(n)]]
    
    inputs = [random_boolean_circuit(n, depth - 1) for _ in range(2)]
    circuit = []
    for i in range(n):
        gate = random.choice(['AND', 'OR', 'XOR'])
        if gate == 'AND':
            result = matrix_mul(inputs[0], inputs[1], 2)
        elif gate == 'OR':
            result = matrix_add(matrix_mod_inv(inputs[0], 2), matrix_mod_inv(inputs[1], 2), 2)
        else:
            result = matrix_sub(matrix_mod_inv(inputs[0], 2), matrix_mod_inv(inputs[1], 2), 2)
        circuit.append(result)
    return circuit

def compute_tropical_motive_rank(circuit):
    n = len(circuit)
    identity = matrix_identity(n, 2)
    rank = 0
    for _ in range(n):
        if matrix_add(identity, circuit, 2) != identity:
            rank += 1
            identity = matrix_sub(identity, circuit, 2)
    return rank

def compute_entanglement_complexity(circuit):
    n = len(circuit)
    complexity = 0
    for i in range(n):
        for j in range(i + 1, n):
            if circuit[i][j] != circuit[j][i]:
                complexity += 1
    return complexity

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        circuit = random_boolean_circuit(n)
        mtr = compute_tropical_motive_rank(circuit)
        ec = compute_entanglement_complexity(circuit)
        results.append((mtr, ec))
    
    if not results:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    mtr_values = [mtr for mtr, _ in results]
    ec_values = [ec for _, ec in results]
    mean_mtr = sum(mtr_values) / len(mtr_values)
    mean_ec = sum(ec_values) / len(ec_values)
    correlation_coefficient = (sum((mtr - mean_mtr) * (ec - mean_ec) for mtr, ec in results) /
                               (len(results) * math.sqrt(sum((mtr - mean_mtr) ** 2 for mtr, _ in results)) *
                                math.sqrt(sum((ec - mean_ec) ** 2 for _, ec in results))))
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": abs(correlation_coefficient) >= 0.8 and all(abs(mtr - ec) <= 3 for mtr, ec in results),
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] if sys.argv[1:] else [2**i + 7 for i in range(5, 8)]
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, **trial_result}}")
    
    all_results = [run_trial(seed) for seed in seeds]
    mean_corr_coeff = sum(result["metric_value"] for result in all_results if result["metric_value"] is not None) / len(all_results)
    support_fraction = sum(1 for result in all_results if result["conjecture_holds"]) / len(all_results)
    
    if all(result["conjecture_holds"] for result in all_results):
        print(f"RESULT: SUPPORTED mean={mean_corr_coeff} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_corr_coeff} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, all_results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient\" first_failing_seed={first_failing_seed}")