# auto-injected by SEC sandbox
import itertools
import json
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
from collections import deque

def matrix_mult(a, b):
    return [[sum(a[i][k] * b[k][j] for k in range(len(b))) for j in range(len(b[0]))] for i in range(len(a))]

def matrix_pow(mat, power):
    result = [[0] * len(mat) for _ in range(len(mat))]
    for i in range(len(mat)):
        result[i][i] = 1
    while power > 0:
        if power % 2 == 1:
            result = matrix_mult(result, mat)
        mat = matrix_mult(mat, mat)
        power //= 2
    return result

def compute_delta(graph):
    n = len(graph)
    if n == 0:
        return 0.0

    # Compute all-pairs shortest paths using Floyd-Warshall
    dist = [[float('inf')] * n for _ in range(n)]
    for i in range(n):
        dist[i][i] = 0
        for j in graph[i]:
            dist[i][j] = 1

    for k in range(n):
        for i in range(n):
            for j in range(n):
                if dist[i][k] + dist[k][j] < dist[i][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]

    max_delta = 0.0
    for a in range(n):
        for b in range(n):
            for c in range(n):
                for e in range(n):
                    if a == b or a == c or a == e or b == c or b == e or c == e:
                        continue
                    d_ac = dist[a][c]
                    d_be = dist[b][e]
                    d_ab = dist[a][b]
                    d_ce = dist[c][e]
                    d_ae = dist[a][e]
                    d_bc = dist[b][c]
                    delta = 0.5 * (d_ac + d_be - max(d_ab + d_ce, d_ae + d_bc))
                    if delta > max_delta:
                        max_delta = delta
    return max_delta

def generate_circuit(d, s, n):
    layers = [[] for _ in range(d + 1)]
    for i in range(n):
        layers[0].append(('input', i))

    gate_types = ['AND', 'OR', 'NOT', 'MOD_2']
    for layer in range(1, d + 1):
        num_gates = min(s, random.randint(2, 4))
        for _ in range(num_gates):
            gate_type = random.choice(gate_types)
            fan_in = random.randint(2, min(4, len(layers[layer - 1])))
            inputs = random.sample(layers[layer - 1], fan_in)
            layers[layer].append((gate_type, inputs))

    output_layer = layers[-1]
    if not output_layer:
        return None, None

    output_gate = random.choice(output_layer)
    return layers, output_gate

def evaluate_circuit(circuit, x):
    if not circuit:
        return 0

    layers, output_gate = circuit
    values = [x]

    for layer in range(1, len(layers)):
        layer_values = []
        for gate in layers[layer]:
            gate_type, inputs = gate
            input_values = [values[prev_layer][i] for prev_layer, i in inputs]
            if gate_type == 'AND':
                val = all(input_values)
            elif gate_type == 'OR':
                val = any(input_values)
            elif gate_type == 'NOT':
                val = not input_values[0]
            elif gate_type == 'MOD_2':
                val = sum(input_values) % 2
            else:
                val = 0
            layer_values.append(val)
        values.append(layer_values)

    output_layer = len(layers) - 1
    output_index = layers[output_layer].index(output_gate)
    return values[output_layer][output_index]

def compute_bias(circuit, n):
    if not circuit:
        return 0.0

    total = 0
    count = 0
    for _ in range(2 ** n):
        x = [random.randint(0, 1) for _ in range(n)]
        mod3 = sum(x) % 3
        output = evaluate_circuit(circuit, x)
        if output == mod3:
            total += 1
        count += 1

    if count == 0:
        return 0.0
    return 2.0 * (total / count) - 1.0

def build_graph(circuit):
    if not circuit:
        return []

    layers, _ = circuit
    nodes = []
    node_indices = {}
    index = 0

    for layer in layers:
        for gate in layer:
            nodes.append(gate)
            node_indices[gate] = index
            index += 1

    graph = [[] for _ in range(len(nodes))]
    for i, gate in enumerate(nodes):
        if isinstance(gate[1], list):
            for input_gate in gate[1]:
                j = node_indices[input_gate]
                graph[i].append(j)
                graph[j].append(i)

    return graph

def run_trial(seed):
    random.seed(seed)
    d_values = [2, 3, 4]
    s_values = [12, 18, 24]
    n_values = [8, 10, 12]

    metric_values = []
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""

    for d in d_values:
        for s in s_values:
            for n in n_values:
                for _ in range(6):
                    circuit = generate_circuit(d, s, n)
                    if not circuit:
                        continue

                    graph = build_graph(circuit)
                    delta = compute_delta(graph)
                    bias = compute_bias(circuit, n)

                    lhs = (bias ** 2) * n
                    rhs = (1 + delta) * (2 ** d)

                    if rhs == 0:
                        continue

                    ratio = lhs / rhs
                    metric_values.append(ratio)
                    instances_tested += 1

                    if ratio > 1.0:
                        conjecture_holds = False
                        counterexample = f"d={d}, s={s}, n={n}, ratio={ratio:.4f}"

    if not metric_values:
        return {
            "metric_name": "max_LHS/RHS_ratio",
            "metric_value": 0.0,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }

    max_ratio = max(metric_values)
    if max_ratio > 1.0:
        conjecture_holds = False

    return {
        "metric_name": "max_LHS/RHS_ratio",
        "metric_value": max_ratio,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = sys.argv[1:]
    if not seeds:
        seeds = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]

    metric_values = []
    instances_tested = 0
    conjecture_holds_all = True
    counterexample = ""

    for seed in seeds:
        trial = run_trial(int(seed))
        print(f"TRIAL: {trial}")
        metric_values.append(trial["metric_value"])
        instances_tested += trial["instances_tested"]
        if not trial["conjecture_holds"]:
            conjecture_holds_all = False
            if not counterexample:
                counterexample = trial["counterexample"]

    if not metric_values:
        print("RESULT: INCONCLUSIVE reason=no_metric_values")
        sys.exit(0)

    mean = sum(metric_values) / len(metric_values)
    variance = sum((x - mean) ** 2 for x in metric_values) / len(metric_values)
    std = math.sqrt(variance)

    support_fraction = sum(1 for x in metric_values if x <= 1.0) / len(metric_values)

    if not conjecture_holds_all:
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={seeds[0]}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean:.4f} std={std:.4f} support_fraction={support_fraction:.4f}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_support")