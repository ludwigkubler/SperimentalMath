# auto-injected by SEC sandbox
import itertools
import os
import time
import re
from itertools import product, combinations, permutations, chain
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import sys
import random
import math
import json
from collections import defaultdict

def matrix_mult(A, B):
    """Multiply two matrices A and B."""
    return [[sum(a * b for a, b in zip(row, col)) for col in zip(*B)] for row in A]

def matrix_transpose(A):
    """Transpose a matrix A."""
    return [list(row) for row in zip(*A)]

def gaussian_elimination(A, b):
    """Solve the system Ax = b using Gaussian elimination."""
    n = len(b)
    for i in range(n):
        max_row = max(range(i, n), key=lambda r: abs(A[r][i]))
        A[i], A[max_row] = A[max_row], A[i]
        b[i], b[max_row] = b[max_row], b[i]
        for j in range(i + 1, n):
            factor = A[j][i] / A[i][i]
            for k in range(i, n):
                A[j][k] -= factor * A[i][k]
            b[j] -= factor * b[i]
    x = [0] * n
    for i in range(n - 1, -1, -1):
        x[i] = (b[i] - sum(A[i][j] * x[j] for j in range(i + 1, n))) / A[i][i]
    return x

def compute_chamber_count(C, n):
    """Compute the chamber count for a circuit C on n inputs."""
    gate_outputs = defaultdict(int)
    for x in range(2**n):
        x_bin = bin(x)[2:].zfill(n)
        output_vector = []
        for gate in C:
            if gate['type'] == 'AND':
                output = all(int(x_bin[i]) for i in gate['inputs'])
            else:
                output = any(int(x_bin[i]) for i in gate['inputs'])
            output_vector.append(int(output))
        gate_outputs[tuple(output_vector)] += 1
    return len(gate_outputs)

def construct_dnf_parity(n):
    """Construct a depth-2 DNF circuit for PARITY_n."""
    C = []
    for i in range(2**(n-1)):
        inputs = [j for j in range(n) if (i >> (n-1-j-1)) & 1]
        C.append({'type': 'AND', 'inputs': inputs})
    C.append({'type': 'OR', 'inputs': list(range(len(C)))})
    return C

def construct_hastad_parity(n, d):
    """Construct a depth-d PARITY circuit using Hastad's method."""
    if d == 2:
        return construct_dnf_parity(n)
    C = []
    for i in range(n):
        C.append({'type': 'AND', 'inputs': [i]})
    for _ in range(d - 2):
        new_gates = []
        for i in range(0, len(C), 2):
            if i + 1 < len(C):
                new_gates.append({'type': 'AND', 'inputs': [i, i+1]})
            else:
                new_gates.append({'type': 'AND', 'inputs': [i]})
        C = new_gates
    C.append({'type': 'OR', 'inputs': list(range(len(C)))})
    return C

def construct_random_dnf(n, size):
    """Construct a random depth-2 DNF circuit of given size."""
    C = []
    for _ in range(size):
        inputs = random.sample(range(n), random.randint(1, n))
        C.append({'type': 'AND', 'inputs': inputs})
    C.append({'type': 'OR', 'inputs': list(range(len(C)))})
    return C

def run_trial(seed):
    random.seed(seed)
    n_values = [6, 8, 10, 12, 14, 16]
    d_values = [2, 3]
    metric_values = []
    conjecture_holds = True
    counterexample = ""
    instances_tested = 0

    for n in n_values:
        for d in d_values:
            # Construct PARITY circuits
            dnf_parity = construct_dnf_parity(n)
            hastad_parity = construct_hastad_parity(n, d)

            # Compute chamber counts
            ch_dnf = compute_chamber_count(dnf_parity, n)
            ch_hastad = compute_chamber_count(hastad_parity, n)

            # Compute metric values
            metric_dnf = math.log2(ch_dnf) / (n ** (1 / (d - 1)))
            metric_hastad = math.log2(ch_hastad) / (n ** (1 / (d - 1)))

            # Check conjecture
            if metric_dnf < 0.25 or metric_hastad < 0.25:
                conjecture_holds = False
                counterexample = f"n={n}, d={d}, ch_dnf={ch_dnf}, ch_hastad={ch_hastad}, seed={seed}"

            metric_values.append(metric_dnf)
            metric_values.append(metric_hastad)
            instances_tested += 2

            # Construct negative control
            size = len(dnf_parity) + len(hastad_parity)
            random_dnf = construct_random_dnf(n, size)
            ch_random = compute_chamber_count(random_dnf, n)
            metric_random = math.log2(ch_random) / (n ** (1 / (d - 1)))

            if metric_random >= metric_dnf or metric_random >= metric_hastad:
                conjecture_holds = False
                counterexample = f"Negative control failed: n={n}, d={d}, ch_random={ch_random}, seed={seed}"

            instances_tested += 1

    if not conjecture_holds:
        return {
            "metric_name": "log2_chamber_count / n^(1/(d-1))",
            "metric_value": sum(metric_values) / len(metric_values),
            "instances_tested": instances_tested,
            "conjecture_holds": False,
            "counterexample": counterexample
        }
    else:
        return {
            "metric_name": "log2_chamber_count / n^(1/(d-1))",
            "metric_value": sum(metric_values) / len(metric_values),
            "instances_tested": instances_tested,
            "conjecture_holds": True,
            "counterexample": ""
        }

if __name__ == "__main__":
    seeds = sys.argv[1:] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    metric_values = []
    conjecture_holds_counts = 0
    counterexamples = []

    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {json.dumps({'seed': seed, **result})}")
        metric_values.append(result["metric_value"])
        if result["conjecture_holds"]:
            conjecture_holds_counts += 1
        if result["counterexample"]:
            counterexamples.append(result["counterexample"])

    mean_metric = sum(metric_values) / len(metric_values)
    std_metric = math.sqrt(sum((x - mean_metric) ** 2 for x in metric_values) / len(metric_values))
    support_fraction = conjecture_holds_counts / len(seeds)

    if counterexamples:
        print(f'RESULT: FALSIFIED counterexample="{counterexamples[0]}" first_failing_seed={seeds[0]}')
    elif support_fraction >= 0.8:
        print(f'RESULT: SUPPORTED mean={mean_metric} std={std_metric} support_fraction={support_fraction}')
    else:
        print('RESULT: INCONCLUSIVE reason=insufficient_support')