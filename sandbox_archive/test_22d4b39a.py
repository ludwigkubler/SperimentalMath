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

def matmul(A, B):
    return [[sum(a * b for a, b in zip(row, col)) for col in zip(*B)] for row in A]

def gauss_elim(matrix):
    n = len(matrix)
    for i in range(n):
        if matrix[i][i] == 0:
            for j in range(i+1, n):
                if matrix[j][i] != 0:
                    matrix[i], matrix[j] = matrix[j], matrix[i]
                    break
        if matrix[i][i] == 0:
            continue
        for j in range(i+1, n):
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
    matrix = [list(vec) for vec in vectors]
    reduced = gauss_elim(matrix)
    for i in range(min(m, n)):
        if all(reduced[i][j] == 0 for j in range(n)):
            return False
    return True

def build_random_acc02_circuit(n, d, m_C, seed):
    random.seed(seed)
    layers = []
    for _ in range(d):
        layer_type = random.choice(['AND', 'OR', 'MOD_2'])
        layer = []
        for _ in range(m_C):
            gate_type = random.choice(['AND', 'OR', 'MOD_2']) if layer_type == 'MIXED' else layer_type
            inputs = random.sample(range(n), 4)
            negations = [random.choice([True, False]) for _ in range(4)]
            layer.append((gate_type, inputs, negations))
        layers.append(layer)
    return layers

def evaluate_gate(gate_type, inputs, negations, input_values):
    values = [input_values[i] ^ negations[i] for i in range(4)]
    if gate_type == 'AND':
        return all(values)
    elif gate_type == 'OR':
        return any(values)
    elif gate_type == 'MOD_2':
        return sum(values) % 2
    else:
        raise ValueError(f"Unknown gate type: {gate_type}")

def run_trial(seed):
    n_values = [16, 24, 32]
    d_values = [2, 3, 4]
    m_C_values = [8, 16, 24]
    N = 1024
    metric_values = []
    conjecture_holds = True
    counterexample = ""

    for n, d, m_C in itertools.product(n_values, d_values, m_C_values):
        circuit = build_random_acc02_circuit(n, d, m_C, seed)
        input_values = [random.randint(0, 1) for _ in range(N)]
        gate_outputs = []
        for layer in circuit:
            new_outputs = []
            for gate_type, inputs, negations in layer:
                output = [evaluate_gate(gate_type, inputs, negations, input_values[i]) for i in range(N)]
                new_outputs.append(output)
            gate_outputs.extend(new_outputs)

        mod2_outputs = [output for output in gate_outputs if len(output) == N]
        if len(mod2_outputs) < m_C:
            continue

        if not is_linearly_independent(mod2_outputs):
            continue

        xor_counts = Counter()
        for a, b in itertools.product(mod2_outputs, repeat=2):
            xor = [a[i] ^ b[i] for i in range(N)]
            xor_counts[tuple(xor)] += 1

        r_star = max(xor_counts.values()) if xor_counts else 0
        sd = r_star - 2
        bound = math.ceil(math.sqrt(m_C))

        if sd > bound:
            conjecture_holds = False
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

    mean_sd = sum(metric_values) / len(metric_values)
    std_sd = math.sqrt(sum((x - mean_sd) ** 2 for x in metric_values) / len(metric_values))

    return {
        "metric_name": "sd(C)",
        "metric_value": mean_sd,
        "instances_tested": len(metric_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    trials = []
    for seed in seeds:
        trial = run_trial(seed)
        print(f"TRIAL: {trial}")
        trials.append(trial)

    metric_values = [trial["metric_value"] for trial in trials if trial["instances_tested"] > 0]
    if not metric_values:
        print("RESULT: INCONCLUSIVE reason=no_valid_circuits")
        sys.exit(0)

    mean = sum(metric_values) / len(metric_values)
    std = math.sqrt(sum((x - mean) ** 2 for x in metric_values) / len(metric_values))
    support_fraction = sum(1 for trial in trials if trial["conjecture_holds"]) / len(trials)

    if all(trial["conjecture_holds"] for trial in trials):
        print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
    else:
        counterexamples = [trial["counterexample"] for trial in trials if not trial["conjecture_holds"]]
        first_failing_seed = next((trial["seed"] for trial in trials if not trial["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample={counterexamples[0]} first_failing_seed={first_failing_seed}")