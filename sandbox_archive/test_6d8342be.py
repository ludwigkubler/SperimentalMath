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

def matrix_add(A, B):
    n = len(A)
    m = len(A[0])
    result = [[0.0 for _ in range(m)] for _ in range(n)]
    for i in range(n):
        for j in range(m):
            result[i][j] = A[i][j] + B[i][j]
    return result

def matrix_scalar_multiply(A, scalar):
    n = len(A)
    m = len(A[0])
    result = [[0.0 for _ in range(m)] for _ in range(n)]
    for i in range(n):
        for j in range(m):
            result[i][j] = A[i][j] * scalar
    return result

def matrix_transpose(A):
    n = len(A)
    m = len(A[0])
    result = [[0.0 for _ in range(n)] for _ in range(m)]
    for i in range(n):
        for j in range(m):
            result[j][i] = A[i][j]
    return result

def matrix_row_normalize(A):
    n = len(A)
    m = len(A[0])
    result = [[0.0 for _ in range(m)] for _ in range(n)]
    for i in range(n):
        row_sum = sum(A[i])
        if row_sum == 0:
            row_sum = 1.0
        for j in range(m):
            result[i][j] = A[i][j] / row_sum
    return result

def matrix_col_normalize(A):
    A_T = matrix_transpose(A)
    A_T_normalized = matrix_row_normalize(A_T)
    return matrix_transpose(A_T_normalized)

def sinkhorn(A, num_iterations=25):
    n = len(A)
    u = [1.0 for _ in range(n)]
    v = [1.0 for _ in range(n)]
    for _ in range(num_iterations):
        u = [1.0 / sum(A[i][j] * v[j] for j in range(n)) for i in range(n)]
        v = [1.0 / sum(A[i][j] * u[i] for i in range(n)) for j in range(n)]
    D = [[u[i] * A[i][j] * v[j] for j in range(n)] for i in range(n)]
    return D

def power_iteration(A, num_iterations=100):
    n = len(A)
    b_k = [random.random() for _ in range(n)]
    for _ in range(num_iterations):
        b_k1 = [sum(A[i][j] * b_k[j] for j in range(n)) for i in range(n)]
        norm = math.sqrt(sum(x**2 for x in b_k1))
        b_k = [x / norm for x in b_k1]
    lambda_2 = sum(b_k[i] * sum(A[i][j] * b_k[j] for j in range(n)) for i in range(n))
    return lambda_2

def generate_ac0_circuit(n, d, s, seed):
    random.seed(seed)
    circuit = []
    for _ in range(d):
        layer = []
        for _ in range(s):
            gate_type = random.choice(['AND', 'OR'])
            inputs = random.sample(range(n), random.randint(1, min(3, n)))
            layer.append((gate_type, inputs))
        circuit.append(layer)
    return circuit

def compute_input_cones(circuit, n):
    cones = [set([i]) for i in range(n)]
    for layer in circuit:
        new_cones = [set() for _ in range(n)]
        for gate_type, inputs in layer:
            for i in range(n):
                if any(i in cones[j] for j in inputs):
                    new_cones[i].update(cones[i])
                    new_cones[i].update(inputs)
        cones = new_cones
    return cones

def build_cooccurrence_matrix(cones, n):
    A = [[0 for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(n):
            count = 0
            for cone in cones:
                if i in cone and j in cone:
                    count += 1
            A[i][j] = count
    return A

def compute_g(C, n):
    cones = compute_input_cones(C, n)
    A = build_cooccurrence_matrix(cones, n)
    J = [[1.0 for _ in range(n)] for _ in range(n)]
    A_plus = matrix_add(A, matrix_scalar_multiply(J, 1e-3))
    D = sinkhorn(A_plus)
    lambda_2 = power_iteration(D)
    g = 1.0 - abs(lambda_2)
    return g

def compute_parity_correlation(C, n):
    def evaluate_circuit(x):
        for layer in C:
            new_x = [0] * len(layer)
            for i, (gate_type, inputs) in enumerate(layer):
                if gate_type == 'AND':
                    new_x[i] = all(x[j] for j in inputs)
                else:
                    new_x[i] = any(x[j] for j in inputs)
            x = new_x
        return x[0] if len(x) == 1 else x[-1]

    total = 0.0
    for x in itertools.product([0, 1], repeat=n):
        C_x = evaluate_circuit(list(x))
        parity_x = sum(x) % 2
        total += (-1) ** (C_x ^ parity_x)
    return abs(total) / (2 ** n)

def run_trial(seed):
    n = random.choice([8, 12, 16])
    d = random.choice([2, 3])
    s = random.choice([6, 12, 24, 48])
    C = generate_ac0_circuit(n, d, s, seed)
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
    seeds = [int(arg) for arg in sys.argv[1:]] if len(sys.argv) > 1 else [i for i in range(30)]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    metric_values = [r["metric_value"] for r in results]
    mean_metric = sum(metric_values) / len(metric_values)
    std_metric = math.sqrt(sum((x - mean_metric) ** 2 for x in metric_values) / len(metric_values))
    support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric} std={std_metric} support_fraction={support_fraction}")
    else:
        for r in results:
            if not r["conjecture_holds"]:
                print(f"RESULT: FALSIFIED counterexample=\"{r['counterexample']}\" first_failing_seed={seeds[results.index(r)]}")
                break