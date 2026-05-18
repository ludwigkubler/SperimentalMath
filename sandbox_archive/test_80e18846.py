# auto-injected by SEC sandbox
import json
import os
import time
import re
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import sys
import random
import math
import itertools
from collections import defaultdict

def matrix_multiply(A, B):
    n = len(A)
    result = [[0.0 for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for k in range(n):
            if A[i][k] == 0:
                continue
            for j in range(n):
                result[i][j] += A[i][k] * B[k][j]
    return result

def matrix_add(A, B):
    n = len(A)
    return [[A[i][j] + B[i][j] for j in range(n)] for i in range(n)]

def matrix_scale(A, scalar):
    n = len(A)
    return [[A[i][j] * scalar for j in range(n)] for i in range(n)]

def matrix_normalize_rows(A):
    n = len(A)
    result = [[0.0 for _ in range(n)] for _ in range(n)]
    for i in range(n):
        row_sum = sum(A[i])
        if row_sum == 0:
            result[i] = [1.0 / n for _ in range(n)]
        else:
            result[i] = [x / row_sum for x in A[i]]
    return result

def matrix_normalize_cols(A):
    n = len(A)
    result = [[0.0 for _ in range(n)] for _ in range(n)]
    for j in range(n):
        col_sum = sum(A[i][j] for i in range(n))
        if col_sum == 0:
            for i in range(n):
                result[i][j] = 1.0 / n
        else:
            for i in range(n):
                result[i][j] = A[i][j] / col_sum
    return result

def sinkhorn(A, iterations=25):
    n = len(A)
    K = A
    for _ in range(iterations):
        K = matrix_normalize_rows(K)
        K = matrix_normalize_cols(K)
    return K

def power_iteration(A, num_iterations=100):
    n = len(A)
    b_k = [random.random() for _ in range(n)]
    for _ in range(num_iterations):
        b_k1 = [sum(A[i][j] * b_k[j] for j in range(n)) for i in range(n)]
        norm = math.sqrt(sum(x**2 for x in b_k1))
        if norm == 0:
            break
        b_k = [x / norm for x in b_k1]
    return sum(b_k[i] * sum(A[i][j] * b_k[j] for j in range(n)) for i in range(n))

def compute_g(C, n):
    A = [[0 for _ in range(n)] for _ in range(n)]
    for g in C:
        inputs = g['inputs']
        for i in inputs:
            for j in inputs:
                A[i][j] += 1
    J = [[1.0 for _ in range(n)] for _ in range(n)]
    A_plus = matrix_add(A, matrix_scale(J, 1e-3))
    D = sinkhorn(A_plus)
    lambda_2 = power_iteration(D)
    return 1 - abs(lambda_2)

def evaluate_circuit(circuit, x):
    n = len(x)
    values = x.copy()
    for gate in circuit:
        inputs = gate['inputs']
        if len(inputs) == 0:
            continue
        if gate['type'] == 'AND':
            values[gate['output']] = all(values[i] for i in inputs)
        elif gate['type'] == 'OR':
            values[gate['output']] = any(values[i] for i in inputs)
    return values[-1]

def compute_parity_correlation(C, n):
    total = 0.0
    count = 0
    for x in itertools.product([False, True], repeat=n):
        C_x = evaluate_circuit(C, list(x))
        parity = sum(x) % 2 == 0
        total += (-1) ** (C_x ^ parity)
        count += 1
    return abs(total / count)

def generate_random_circuit(n, d, s):
    circuit = []
    for layer in range(d):
        num_gates = min(s, n)
        for i in range(num_gates):
            gate_type = random.choice(['AND', 'OR'])
            inputs = random.sample(range(n), random.randint(1, min(3, n)))
            output = n + layer * num_gates + i
            circuit.append({'type': gate_type, 'inputs': inputs, 'output': output})
    return circuit

def run_trial(seed):
    random.seed(seed)
    n = random.choice([8, 12, 16])
    d = random.choice([2, 3])
    s = random.choice([6, 12, 24, 48])
    C = generate_random_circuit(n, d, s)
    g_val = compute_g(C, n)
    kappa = compute_parity_correlation(C, n)
    bound = math.exp(-n * g_val / (8 * d))
    conjecture_holds = kappa <= bound
    counterexample = "" if conjecture_holds else f"n={n}, d={d}, s={s}, kappa={kappa}, bound={bound}"
    return {
        "metric_name": "kappa_bound_ratio",
        "metric_value": kappa / bound if bound > 0 else float('inf'),
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    metric_values = [r["metric_value"] for r in results]
    mean = sum(metric_values) / len(metric_values)
    std = math.sqrt(sum((x - mean) ** 2 for x in metric_values) / len(metric_values))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
    elif any(r["counterexample"] for r in results):
        first_failing_seed = seeds[next(i for i, r in enumerate(results) if r["counterexample"])]
        counterexample = next(r["counterexample"] for r in results if r["counterexample"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=metric_saturation")