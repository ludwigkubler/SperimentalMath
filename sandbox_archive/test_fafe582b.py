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

def xor(a, b):
    return a ^ b

def matrix_rank(matrix):
    if not matrix:
        return 0
    n = len(matrix)
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
                matrix[row] = [xor(matrix[row][i], matrix[rank][i]) for i in range(m)]
        rank += 1
    return rank

def is_linearly_independent(vectors):
    if not vectors:
        return True
    n = len(vectors[0])
    matrix = [[0] * n for _ in range(len(vectors))]
    for i, vec in enumerate(vectors):
        for j, bit in enumerate(vec):
            matrix[i][j] = bit
    return matrix_rank(matrix) == len(vectors)

def build_random_acc02_circuit(n, d, m_C, seed):
    random.seed(seed)
    circuit = []
    for _ in range(d):
        layer = []
        for _ in range(m_C):
            gate_type = random.choice(['AND', 'OR', 'MOD_2'])
            fan_in = 4
            inputs = random.sample(range(n), fan_in)
            negations = [random.choice([True, False]) for _ in range(fan_in)]
            layer.append((gate_type, inputs, negations))
        circuit.append(layer)
    return circuit

def evaluate_gate(gate_type, inputs, negations, input_values):
    values = [input_values[i] ^ negations[i] for i in range(len(inputs))]
    if gate_type == 'AND':
        return all(values)
    elif gate_type == 'OR':
        return any(values)
    elif gate_type == 'MOD_2':
        return sum(values) % 2 == 1
    else:
        raise ValueError(f"Unknown gate type: {gate_type}")

def evaluate_circuit(circuit, input_values):
    outputs = []
    for layer in circuit:
        layer_outputs = []
        for gate in layer:
            gate_type, inputs, negations = gate
            output = evaluate_gate(gate_type, inputs, negations, input_values)
            layer_outputs.append(output)
        outputs.append(layer_outputs)
    return outputs

def run_trial(seed):
    random.seed(seed)
    n_values = [16, 24, 32]
    d_values = [2, 3, 4]
    m_C_values = [8, 16, 24]
    N = 1024

    metric_values = []
    conjecture_holds_all = True
    counterexample = ""

    for n in n_values:
        for d in d_values:
            for m_C in m_C_values:
                circuit = build_random_acc02_circuit(n, d, m_C, seed)
                vectors = []
                for _ in range(N):
                    input_values = [random.choice([0, 1]) for _ in range(n)]
                    outputs = evaluate_circuit(circuit, input_values)
                    for layer in outputs:
                        for output in layer:
                            vectors.append(output)

                if not is_linearly_independent(vectors):
                    continue

                xor_counts = Counter()
                for a, b in itertools.product(vectors, repeat=2):
                    xor_counts[xor(a, b)] += 1

                r_star = max(xor_counts.values()) if xor_counts else 0
                sd = r_star - 2
                bound = math.ceil(math.sqrt(m_C))

                if sd > bound:
                    conjecture_holds_all = False
                    counterexample = f"seed={seed}, d={d}, m_C={m_C}, n={n}, r*={r_star}, sd={sd}, bound={bound}"

                metric_values.append(sd)

    if not metric_values:
        return {
            "metric_name": "sd(C)",
            "metric_value": 0,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "No valid circuits found"
        }

    metric_value = sum(metric_values) / len(metric_values)
    instances_tested = len(metric_values)

    return {
        "metric_name": "sd(C)",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds_all,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]

    metric_values = []
    conjecture_holds_counts = 0
    total_instances = 0

    for seed in seeds:
        trial = run_trial(seed)
        print(f"TRIAL: {trial}")
        metric_values.append(trial["metric_value"])
        if trial["conjecture_holds"]:
            conjecture_holds_counts += 1
        total_instances += trial["instances_tested"]

    if not metric_values:
        print("RESULT: INCONCLUSIVE reason=no_metric_values")
        sys.exit(0)

    mean_metric = sum(metric_values) / len(metric_values)
    std_metric = math.sqrt(sum((x - mean_metric) ** 2 for x in metric_values) / len(metric_values))
    support_fraction = conjecture_holds_counts / len(seeds)

    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric} std={std_metric} support_fraction={support_fraction}")
    else:
        print(f"RESULT: FALSIFIED counterexample={trial['counterexample']} first_failing_seed={seeds[conjecture_holds_counts]}")