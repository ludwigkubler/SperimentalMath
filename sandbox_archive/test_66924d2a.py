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
import collections

def matrix_multiply(A, B):
    """Multiply two matrices over F_2."""
    n = len(A)
    m = len(B[0])
    p = len(B)
    result = [[0 for _ in range(m)] for _ in range(n)]
    for i in range(n):
        for j in range(m):
            for k in range(p):
                result[i][j] ^= A[i][k] & B[k][j]
    return result

def gaussian_elimination(matrix):
    """Perform Gaussian elimination over F_2."""
    n = len(matrix)
    if n == 0:
        return matrix
    m = len(matrix[0])
    rank = 0
    for col in range(m):
        pivot = -1
        for row in range(rank, n):
            if matrix[row][col] == 1:
                pivot = row
                break
        if pivot == -1:
            continue
        matrix[rank], matrix[pivot] = matrix[pivot], matrix[rank]
        for row in range(n):
            if row != rank and matrix[row][col] == 1:
                for c in range(col, m):
                    matrix[row][c] ^= matrix[rank][c]
        rank += 1
    return matrix

def is_linearly_independent(vectors):
    """Check if vectors are linearly independent over F_2."""
    if not vectors:
        return True
    n = len(vectors[0])
    matrix = [[0 for _ in range(n)] for _ in range(len(vectors))]
    for i, vec in enumerate(vectors):
        for j, val in enumerate(vec):
            matrix[i][j] = val
    reduced = gaussian_elimination(matrix)
    for i in range(len(reduced)):
        if all(reduced[i][j] == 0 for j in range(len(reduced[i]))):
            return False
    return True

def build_random_acc0_circuit(n, d, m_C, seed):
    """Build a random ACC⁰[2] circuit with alternating layers."""
    random.seed(seed)
    layers = []
    for _ in range(d):
        layer_type = random.choice(['AND', 'OR', 'MOD_2'])
        layer = []
        for _ in range(m_C):
            gate_type = random.choice(['AND', 'OR', 'MOD_2']) if layer_type != 'MOD_2' else 'MOD_2'
            fan_in = 4
            inputs = random.sample(range(n), fan_in)
            negations = [random.choice([True, False]) for _ in range(fan_in)]
            layer.append((gate_type, inputs, negations))
        layers.append(layer)
    return layers

def evaluate_circuit(circuit, inputs):
    """Evaluate the circuit on the given inputs."""
    gate_outputs = []
    for layer in circuit:
        layer_outputs = []
        for gate_type, inputs_idx, negations in layer:
            gate_input = [inputs[i] ^ negations[i] for i in inputs_idx]
            if gate_type == 'AND':
                output = all(gate_input)
            elif gate_type == 'OR':
                output = any(gate_input)
            elif gate_type == 'MOD_2':
                output = sum(gate_input) % 2
            layer_outputs.append(output)
        gate_outputs.extend(layer_outputs)
    return gate_outputs

def run_trial(seed):
    """Run one trial of the experiment."""
    random.seed(seed)
    n = random.choice([16, 24, 32])
    d = random.choice([2, 3, 4])
    m_C = random.choice([8, 16, 24])
    N = 1024

    # Build a random ACC⁰[2] circuit
    circuit = build_random_acc0_circuit(n, d, m_C, seed)

    # Generate random inputs
    inputs = [[random.choice([0, 1]) for _ in range(n)] for _ in range(N)]

    # Evaluate the circuit on the inputs
    gate_outputs = []
    for input_vec in inputs:
        gate_outputs.append(evaluate_circuit(circuit, input_vec))

    # Extract MOD_2 gate outputs
    mod2_outputs = []
    for i in range(len(circuit)):
        for j in range(len(circuit[i])):
            if circuit[i][j][0] == 'MOD_2':
                mod2_outputs.append([gate_outputs[k][i * len(circuit[i]) + j] for k in range(N)])

    # Check linear independence
    if not is_linearly_independent(mod2_outputs):
        return {
            "metric_name": "r*(C,s) - 2",
            "metric_value": 0,
            "instances_tested": 1,
            "conjecture_holds": True,
            "counterexample": ""
        }

    # Compute pairwise XORs and find r*(C,s)
    xor_counts = collections.Counter()
    for a in mod2_outputs:
        for b in mod2_outputs:
            xor_vec = [a[i] ^ b[i] for i in range(N)]
            xor_counts[tuple(xor_vec)] += 1

    r_star = max(xor_counts.values()) if xor_counts else 0
    metric_value = r_star - 2
    bound = math.ceil(math.sqrt(m_C))

    conjecture_holds = metric_value <= bound
    counterexample = f"seed={seed}, d={d}, m_C={m_C}, n={n}, r*={r_star}" if not conjecture_holds else ""

    return {
        "metric_name": "r*(C,s) - 2",
        "metric_value": metric_value,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]

    metric_values = []
    conjecture_holds_counts = 0
    counterexamples = []

    for seed in seeds:
        trial = run_trial(seed)
        print(f"TRIAL: {trial}")
        metric_values.append(trial["metric_value"])
        if trial["conjecture_holds"]:
            conjecture_holds_counts += 1
        if trial["counterexample"]:
            counterexamples.append(trial["counterexample"])

    mean_metric = sum(metric_values) / len(metric_values) if metric_values else 0
    std_metric = math.sqrt(sum((x - mean_metric) ** 2 for x in metric_values) / len(metric_values)) if metric_values else 0
    support_fraction = conjecture_holds_counts / len(seeds)

    if counterexamples:
        print(f'RESULT: FALSIFIED counterexample="{counterexamples[0]}" first_failing_seed={seeds[0]}')
    elif support_fraction >= 0.8:
        print(f'RESULT: SUPPORTED mean={mean_metric} std={std_metric} support_fraction={support_fraction}')
    else:
        print('RESULT: INCONCLUSIVE reason=insufficient_support')