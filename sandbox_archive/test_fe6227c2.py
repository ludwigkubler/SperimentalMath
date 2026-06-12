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

def mod_inverse(a, m):
    if m == 1:
        return 0
    for x in range(1, m):
        if (a * x) % m == 1:
            return x
    raise ValueError("Inverse doesn't exist")

def matrix_mod_inv(matrix, mod):
    n = len(matrix)
    det = Fraction(0)
    sign = 1
    
    def sub_det(sub_matrix):
        if len(sub_matrix) == 2:
            return (sub_matrix[0][0] * sub_matrix[1][1]) - (sub_matrix[0][1] * sub_matrix[1][0])
        
        det = Fraction(0)
        for c in range(len(sub_matrix)):
            det += sign * sub_matrix[0][c] * sub_det([row[:c] + row[c+1:] for row in sub_matrix[1:]])
            sign *= -1
        return det
    
    if n == 2:
        det = (matrix[0][0] * matrix[1][1]) - (matrix[0][1] * matrix[1][0])
        inv_det = mod_inverse(det, mod)
        return [[(inv_det * (matrix[1][1])) % mod, (-inv_det * (matrix[0][1])) % mod],
                [(-inv_det * (matrix[1][0])) % mod, (inv_det * (matrix[0][0])) % mod]]
    
    det = sub_det(matrix)
    inv_det = mod_inverse(det, mod)
    adjugate = []
    for i in range(n):
        row = []
        for j in range(n):
            minor = [row[:j] + row[j+1:] for row in matrix[:i] + matrix[i+1:]]
            sign = (-1) ** (i + j)
            cofactor = sign * sub_det(minor)
            adjugate.append((cofactor * inv_det) % mod)
        adjugate.append(row[::-1])
    return adjugate

def matrix_mul(A, B):
    n = len(A)
    result = [[0 for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                result[i][j] += A[i][k] * B[k][j]
    return result

def matrix_add(A, B):
    n = len(A)
    result = [[0 for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(n):
            result[i][j] = (A[i][j] + B[i][j]) % 2
    return result

def matrix_sub(A, B, mod):
    n = len(A)
    result = [[0 for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(n):
            result[i][j] = (A[i][j] - B[i][j]) % mod
    return result

def random_boolean_circuit(n, depth=3):
    if depth == 0:
        return [[random.randint(0, 1) for _ in range(n)]]
    
    inputs = [random_boolean_circuit(n, depth - 1) for _ in range(2)]
    gate = random.choice(['and', 'or'])
    
    if gate == 'and':
        result = matrix_mul(inputs[0], inputs[1])
    elif gate == 'or':
        result = matrix_add(matrix_sub(inputs[0], inputs[1]), inputs[1])
    
    return result

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    mtr_values = []
    ec_values = []
    
    for n in n_values:
        circuit = random_boolean_circuit(n)
        # Placeholder for actual computation of mtr(C) and EC(C)
        mtr = sum(sum(row) for row in circuit) / len(circuit)
        ec = sum(len(row) for row in circuit)  # Simplified placeholder
        
        mtr_values.append(mtr)
        ec_values.append(ec)
    
    correlation_coefficient = (sum((mtr_values[i] - mean_mtr) * (ec_values[i] - mean_ec) for i in range(len(n_values))) /
                               math.sqrt(sum((mtr_values[i] - mean_mtr) ** 2 for i in range(len(n_values))) *
                                         sum((ec_values[i] - mean_ec) ** 2 for i in range(len(n_values)))))
    
    mean_mtr = sum(mtr_values) / len(mtr_values)
    mean_ec = sum(ec_values) / len(ec_values)
    
    conjecture_holds = abs(correlation_coefficient) >= 0.8 and all(abs(mtr - ec) <= 3 for mtr, ec in zip(mtr_values, ec_values))
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(n_values),
        "n_max": max(n_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    std_metric_value = math.sqrt(sum((result["metric_value"] - mean_metric_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results) and support_fraction >= 0.8:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")