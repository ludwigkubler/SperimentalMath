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
    m = len(B[0])
    p = len(B)
    result = [[0.0 for _ in range(m)] for _ in range(n)]
    for i in range(n):
        for j in range(m):
            for k in range(p):
                result[i][j] += A[i][k] * B[k][j]
    return result

def matrix_transpose(A):
    return [list(row) for row in zip(*A)]

def matrix_add(A, B):
    return [[A[i][j] + B[i][j] for j in range(len(A[0]))] for i in range(len(A))]

def matrix_scale(A, scalar):
    return [[A[i][j] * scalar for j in range(len(A[0]))] for i in range(len(A))]

def matrix_normalize_rows(A):
    row_sums = [sum(row) for row in A]
    return [[A[i][j] / row_sums[i] if row_sums[i] != 0 else 0.0 for j in range(len(A[0]))] for i in range(len(A))]

def matrix_normalize_cols(A):
    A_T = matrix_transpose(A)
    A_T_normalized = matrix_normalize_rows(A_T)
    return matrix_transpose(A_T_normalized)

def sinkhorn(A, iterations=25):
    for _ in range(iterations):
        A = matrix_normalize_rows(A)
        A = matrix_normalize_cols(A)
    return A

def power_iteration(A, num_iterations=100):
    n = len(A)
    b = [1.0 / n for _ in range(n)]
    for _ in range(num_iterations):
        b_new = [sum(A[i][j] * b[j] for j in range(n)) for i in range(n)]
        norm = math.sqrt(sum(x**2 for x in b_new))
        b = [x / norm for x in b_new]
    return b

def compute_eigenvalue(A, b):
    Ab = [sum(A[i][j] * b[j] for j in range(len(b))) for i in range(len(A))]
    return sum(Ab[i] * b[i] for i in range(len(b)))

def compute_second_eigenvalue(A):
    n = len(A)
    b1 = power_iteration(A)
    lambda1 = compute_eigenvalue(A, b1)
    A_shifted = [[A[i][j] - lambda1 * (i == j) for j in range(n)] for i in range(n)]
    b2 = power_iteration(A_shifted)
    lambda2 = compute_eigenvalue(A_shifted, b2)
    return lambda2

def build_co_occurrence_matrix(C, n):
    A = [[0 for _ in range(n)] for _ in range(n)]
    for gate in C:
        inputs = gate['inputs']
        for i in range(len(inputs)):
            for j in range(i + 1, len(inputs)):
                x_i = inputs[i]
                x_j = inputs[j]
                A[x_i][x_j] += 1
                A[x_j][x_i] += 1
    return A

def compute_g(C, n):
    A = build_co_occurrence_matrix(C, n)
    J = [[1.0 for _ in range(n)] for _ in range(n)]
    A_tilde = matrix_add(A, matrix_scale(J, 1e-3))
    D = sinkhorn(A_tilde)
    lambda2 = compute_second_eigenvalue(D)
    return 1.0 - abs(lambda2)

def evaluate_circuit(C, x):
    values = list(x)
    for gate in C:
        inputs = gate['inputs']
        if gate['type'] == 'AND':
            values.append(all(values[i] for i in inputs))
        elif gate['type'] == 'OR':
            values.append(any(values[i] for i in inputs))
    return values[-1]

def compute_parity_correlation(C, n):
    total = 0.0
    for x in itertools.product([0, 1], repeat=n):
        parity = sum(x) % 2
        C_x = evaluate_circuit(C, x)
        total += (-1) ** (C_x ^ parity)
    return abs(total) / (2 ** n)

def generate_random_circuit(n, d, s):
    C = []
    for _ in range(s):
        layer = random.randint(0, d - 1)
        gate_type = random.choice(['AND', 'OR'])
        num_inputs = random.randint(1, min(n, 2))
        inputs = random.sample(range(n), num_inputs)
        C.append({'type': gate_type, 'inputs': inputs})
    return C

def run_trial(seed):
    random.seed(seed)
    n = random.choice([8, 12, 16])
    d = random.choice([2, 3])
    s = random.choice([6, 12, 24, 48])
    C = generate_random_circuit(n, d, s)
    g = compute_g(C, n)
    kappa = compute_parity_correlation(C, n)
    bound = math.exp(-n * g / (8 * d))
    conjecture_holds = kappa <= bound
    counterexample = "" if conjecture_holds else f"n={n}, d={d}, s={s}, kappa={kappa}, bound={bound}"
    return {
        "metric_name": "kappa_bound_ratio",
        "metric_value": kappa / bound if bound > 0 else float('inf'),
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample,
        "n": n,
        "d": d,
        "s": s,
        "g": g,
        "kappa": kappa,
        "bound": bound
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    metric_values = [r["metric_value"] for r in results]
    mean_metric = sum(metric_values) / len(metric_values) if metric_values else 0.0
    std_metric = math.sqrt(sum((x - mean_metric) ** 2 for x in metric_values) / len(metric_values)) if metric_values else 0.0
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results) if results else 0.0

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric} std={std_metric} support_fraction={support_fraction}")
    else:
        failing_trials = [r for r in results if not r["conjecture_holds"]]
        if failing_trials:
            first_failing_seed = seeds[results.index(failing_trials[0])]
            print(f"RESULT: FALSIFIED counterexample=\"{failing_trials[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
        else:
            print("RESULT: INCONCLUSIVE reason=empty_results")