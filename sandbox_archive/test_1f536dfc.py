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

def generate_random_circuit(n, d, s, seed):
    random.seed(seed)
    circuit = []
    for _ in range(d):
        layer = []
        for _ in range(s):
            gate_type = random.choice(['AND', 'OR'])
            inputs = random.sample(range(n), random.randint(1, n))
            layer.append((gate_type, inputs))
        circuit.append(layer)
    return circuit

def evaluate_circuit(circuit, x):
    for layer in circuit:
        new_x = [False] * len(layer)
        for i, (gate_type, inputs) in enumerate(layer):
            if gate_type == 'AND':
                new_x[i] = all(x[j] for j in inputs)
            else:
                new_x[i] = any(x[j] for j in inputs)
        x = new_x
    return x[0] if x else False

def compute_parity_correlation(circuit, n):
    total = 0
    for x in itertools.product([False, True], repeat=n):
        C_x = evaluate_circuit(circuit, list(x))
        parity_x = sum(x) % 2 == 0
        total += (-1) ** (C_x ^ parity_x)
    return abs(total) / (2 ** n)

def build_cooccurrence_matrix(circuit, n):
    A = [[0] * n for _ in range(n)]
    for layer in circuit:
        for gate_type, inputs in layer:
            for i in range(n):
                for j in range(n):
                    if i in inputs and j in inputs:
                        A[i][j] += 1
    return A

def add_small_perturbation(A, epsilon):
    n = len(A)
    for i in range(n):
        for j in range(n):
            A[i][j] += epsilon
    return A

def sinkhorn_scaling(A, iterations=25):
    n = len(A)
    D = [1.0] * n
    for _ in range(iterations):
        for i in range(n):
            D[i] = 1.0 / sum(A[i][j] * D[j] for j in range(n))
    for i in range(n):
        for j in range(n):
            A[i][j] *= D[i] * D[j]
    return A

def power_iteration(A, num_iterations=100):
    n = len(A)
    b_k = [random.random() for _ in range(n)]
    for _ in range(num_iterations):
        b_k1 = [sum(A[i][j] * b_k[j] for j in range(n)) for i in range(n)]
        norm = math.sqrt(sum(x**2 for x in b_k1))
        b_k = [x / norm for x in b_k1]
    lambda_2 = sum(A[i][j] * b_k[j] for i in range(n) for j in range(n))
    return lambda_2

def compute_g(C, n):
    A = build_cooccurrence_matrix(C, n)
    A = add_small_perturbation(A, 1e-3)
    D = sinkhorn_scaling(A)
    lambda_2 = power_iteration(D)
    return 1 - abs(lambda_2)

def run_trial(seed):
    n = random.choice([8, 12, 16])
    d = random.choice([2, 3])
    s = random.choice([6, 12, 24, 48])
    C = generate_random_circuit(n, d, s, seed)
    g_val = compute_g(C, n)
    kappa = compute_parity_correlation(C, n)
    bound = math.exp(-n * g_val / (8 * d))
    ratio = kappa / bound if bound > 0 else 0
    conjecture_holds = ratio <= 1.05
    counterexample = f"n={n}, d={d}, s={s}, kappa={kappa}, bound={bound}" if not conjecture_holds else ""
    return {
        "metric_name": "kappa_bound_ratio",
        "metric_value": ratio,
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
    mean = sum(metric_values) / len(metric_values) if metric_values else 0
    std = math.sqrt(sum((x - mean) ** 2 for x in metric_values) / len(metric_values)) if metric_values else 0
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results) if results else 0

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["counterexample"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{first_failing_seed}\" first_failing_seed={seeds[results.index(next(r for r in results if not r['conjecture_holds']))]}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")