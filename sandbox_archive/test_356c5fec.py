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

def generate_circuit(d, s, n):
    layers = [[] for _ in range(d + 1)]
    gates = {}
    gate_types = ['AND', 'OR', 'NOT', 'MOD_2']
    input_gates = list(range(n))

    for i in range(n):
        gates[i] = {'type': 'INPUT', 'layer': 0}
        layers[0].append(i)

    for layer in range(1, d + 1):
        num_gates = min(s, random.randint(2, 4) * len(layers[layer - 1]))
        for _ in range(num_gates):
            gate_type = random.choice(gate_types)
            fan_in = random.randint(2, 4)
            operands = random.sample(layers[layer - 1], min(fan_in, len(layers[layer - 1])))
            gate_id = len(gates)
            gates[gate_id] = {'type': gate_type, 'operands': operands, 'layer': layer}
            layers[layer].append(gate_id)

    output_gate = random.choice(layers[d])
    return gates, output_gate

def evaluate_circuit(circuit, inputs):
    values = [None] * len(circuit)
    for gate_id, gate in circuit.items():
        if gate['type'] == 'INPUT':
            values[gate_id] = inputs[gate_id]
        elif gate['type'] == 'NOT':
            values[gate_id] = 1 - values[gate['operands'][0]]
        elif gate['type'] == 'AND':
            values[gate_id] = values[gate['operands'][0]] & values[gate['operands'][1]]
        elif gate['type'] == 'OR':
            values[gate_id] = values[gate['operands'][0]] | values[gate['operands'][1]]
        elif gate['type'] == 'MOD_2':
            values[gate_id] = (values[gate['operands'][0]] + values[gate['operands'][1]]) % 2
    return values

def compute_bias(circuit, n):
    total = 0
    count = 0
    for _ in range(2**n):
        inputs = [random.randint(0, 1) for _ in range(n)]
        values = evaluate_circuit(circuit, inputs)
        output = values[max(circuit.keys())]
        mod3 = sum(inputs) % 3
        if output == mod3:
            total += 1
        count += 1
    if count == 0:
        return 0.0
    bias = 2 * (total / count) - 1
    return bias

def build_adjacency_matrix(circuit):
    n = len(circuit)
    adj = [[0] * n for _ in range(n)]
    for gate_id, gate in circuit.items():
        if gate['type'] != 'INPUT':
            for operand in gate['operands']:
                adj[gate_id][operand] = 1
                adj[operand][gate_id] = 1
    return adj

def bfs(adj, start):
    n = len(adj)
    distances = [-1] * n
    queue = deque()
    distances[start] = 0
    queue.append(start)
    while queue:
        current = queue.popleft()
        for neighbor in range(n):
            if adj[current][neighbor] == 1 and distances[neighbor] == -1:
                distances[neighbor] = distances[current] + 1
                queue.append(neighbor)
    return distances

def compute_delta(circuit):
    adj = build_adjacency_matrix(circuit)
    n = len(adj)
    max_delta = 0
    for a in range(n):
        for b in range(n):
            for c in range(n):
                for e in range(n):
                    if a == b or a == c or a == e or b == c or b == e or c == e:
                        continue
                    distances_a = bfs(adj, a)
                    distances_b = bfs(adj, b)
                    distances_c = bfs(adj, c)
                    distances_e = bfs(adj, e)
                    if -1 in distances_a or -1 in distances_b or -1 in distances_c or -1 in distances_e:
                        continue
                    term1 = distances_a[c] + distances_b[e]
                    term2 = max(distances_a[b] + distances_c[e], distances_a[e] + distances_b[c])
                    delta = term1 - term2
                    if delta > max_delta:
                        max_delta = delta
    return max_delta / 2

def run_trial(seed):
    random.seed(seed)
    d = random.choice([2, 3, 4])
    s = random.choice([12, 18, 24])
    n = random.choice([8, 10, 12])
    circuit, output_gate = generate_circuit(d, s, n)
    bias = compute_bias(circuit, n)
    delta = compute_delta(circuit)
    lhs = (bias ** 2) * n
    rhs = (1 + delta) * (2 ** d)
    if rhs == 0:
        return {
            "metric_name": "LHS/RHS ratio",
            "metric_value": 0.0,
            "instances_tested": 1,
            "conjecture_holds": True,
            "counterexample": ""
        }
    ratio = lhs / rhs
    conjecture_holds = ratio <= 1.0
    counterexample = f"seed={seed}, d={d}, s={s}, n={n}, ratio={ratio}" if not conjecture_holds else ""
    return {
        "metric_name": "LHS/RHS ratio",
        "metric_value": ratio,
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

    mean_metric = sum(metric_values) / len(metric_values) if metric_values else 0.0
    std_metric = math.sqrt(sum((x - mean_metric) ** 2 for x in metric_values) / len(metric_values)) if metric_values else 0.0
    support_fraction = conjecture_holds_counts / len(seeds) if seeds else 0.0

    if counterexamples:
        print(f"RESULT: FALSIFIED counterexample=\"{counterexamples[0]}\" first_failing_seed={seeds[counterexamples.index(counterexamples[0])]}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric} std={std_metric} support_fraction={support_fraction}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_support")