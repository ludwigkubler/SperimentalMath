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
from collections import Counter

def matrix_multiply(A, B):
    return [[sum(a * b for a, b in zip(row, col)) for col in zip(*B)] for row in A]

def gaussian_elimination(matrix):
    n = len(matrix)
    for i in range(n):
        if matrix[i][i] == 0:
            for j in range(i + 1, n):
                if matrix[j][i] != 0:
                    matrix[i], matrix[j] = matrix[j], matrix[i]
                    break
        if matrix[i][i] == 0:
            continue
        for j in range(i + 1, n):
            factor = matrix[j][i] / matrix[i][i]
            for k in range(i, n):
                matrix[j][k] -= factor * matrix[i][k]
    return matrix

def is_linearly_independent(vectors):
    if not vectors:
        return True
    n = len(vectors[0])
    m = len(vectors)
    if m > n:
        return False
    matrix = [[0] * m for _ in range(n)]
    for i in range(n):
        for j in range(m):
            matrix[i][j] = vectors[j][i]
    reduced = gaussian_elimination(matrix)
    for i in range(min(n, m)):
        if reduced[i][i] == 0:
            return False
    return True

def evaluate_gate(gate_type, inputs, negations, input_values):
    if gate_type == 'AND':
        values = [input_values[i] ^ negations[i] for i in range(len(inputs))]
        return int(all(values))
    elif gate_type == 'OR':
        values = [input_values[i] ^ negations[i] for i in range(len(inputs))]
        return int(any(values))
    elif gate_type == 'MOD_2':
        values = [input_values[i] ^ negations[i] for i in range(len(inputs))]
        return sum(values) % 2
    else:
        raise ValueError("Unknown gate type")

def build_circuit(n, d, m_C):
    layers = []
    for _ in range(d):
        layer = []
        for _ in range(m_C):
            gate_type = random.choice(['AND', 'OR', 'MOD_2'])
            inputs = random.sample(range(n), 4)
            negations = [random.randint(0, 1) for _ in range(4)]
            layer.append((gate_type, inputs, negations))
        layers.append(layer)
    return layers

def run_trial(seed):
    random.seed(seed)
    n_values = [16, 24, 32]
    d_values = [2, 3, 4]
    m_C_values = [8, 16, 24]
    N = 1024
    metric_values = []
    conjecture_holds_list = []
    counterexamples = []

    for n in n_values:
        for d in d_values:
            for m_C in m_C_values:
                circuit = build_circuit(n, d, m_C)
                input_values = [random.randint(0, 1) for _ in range(N)]
                gate_outputs = []
                for layer in circuit:
                    new_outputs = []
                    for gate_type, inputs, negations in layer:
                        output = [evaluate_gate(gate_type, inputs, negations, [input_values[i] for i in range(N)])]
                        new_outputs.append(output)
                    gate_outputs.extend(new_outputs)
                mod_gates = [output for output in gate_outputs if len(output) == 1]
                if len(mod_gates) < m_C:
                    continue
                vectors = [output[0] for output in mod_gates[:m_C]]
                if not is_linearly_independent(vectors):
                    continue
                xor_counts = Counter()
                for a, b in itertools.product(vectors, repeat=2):
                    xor_counts[a ^ b] += 1
                r_star = max(xor_counts.values()) if xor_counts else 0
                sd = r_star - 2
                bound = math.ceil(math.sqrt(m_C))
                conjecture_holds = sd <= bound
                metric_values.append(sd)
                conjecture_holds_list.append(conjecture_holds)
                if not conjecture_holds:
                    counterexamples.append(f"seed={seed}, d={d}, m_C={m_C}, n={n}, r*={r_star}")

    if not metric_values:
        return {
            "metric_name": "sd(C)",
            "metric_value": 0,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "No valid circuits found"
        }

    metric_value = sum(metric_values) / len(metric_values)
    support_fraction = sum(conjecture_holds_list) / len(conjecture_holds_list)
    counterexample = counterexamples[0] if counterexamples else ""

    return {
        "metric_name": "sd(C)",
        "metric_value": metric_value,
        "instances_tested": len(metric_values),
        "conjecture_holds": all(conjecture_holds_list),
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    metric_values = []
    conjecture_holds_list = []
    counterexamples = []

    for seed in seeds:
        trial = run_trial(seed)
        print(f"TRIAL: {trial}")
        metric_values.append(trial["metric_value"])
        conjecture_holds_list.append(trial["conjecture_holds"])
        if trial["counterexample"]:
            counterexamples.append(trial["counterexample"])

    mean_metric = sum(metric_values) / len(metric_values)
    std_metric = math.sqrt(sum((x - mean_metric) ** 2 for x in metric_values) / len(metric_values))
    support_fraction = sum(conjecture_holds_list) / len(conjecture_holds_list)

    if counterexamples:
        print(f'RESULT: FALSIFIED counterexample="{counterexamples[0]}" first_failing_seed={seeds[conjecture_holds_list.index(False)]}')
    elif support_fraction >= 0.8:
        print(f'RESULT: SUPPORTED mean={mean_metric} std={std_metric} support_fraction={support_fraction}')
    else:
        print('RESULT: INCONCLUSIVE reason=insufficient_support')