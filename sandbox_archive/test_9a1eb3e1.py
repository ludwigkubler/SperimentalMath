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

def bfs(graph, start):
    distances = {node: -1 for node in graph}
    queue = deque([start])
    distances[start] = 0
    while queue:
        current = queue.popleft()
        for neighbor in graph[current]:
            if distances[neighbor] == -1:
                distances[neighbor] = distances[current] + 1
                queue.append(neighbor)
    return distances

def compute_delta(graph):
    nodes = list(graph.keys())
    max_delta = 0
    for a in nodes:
        distances_a = bfs(graph, a)
        for b in nodes:
            distances_b = bfs(graph, b)
            for c in nodes:
                distances_c = bfs(graph, c)
                for e in nodes:
                    d_ac = distances_a[c]
                    d_be = distances_b[e]
                    d_ab = distances_a[b]
                    d_ce = distances_c[e]
                    d_ae = distances_a[e]
                    d_bc = distances_b[c]
                    delta = (d_ac + d_be - max(d_ab + d_ce, d_ae + d_bc)) / 2
                    if delta > max_delta:
                        max_delta = delta
    return max_delta

def evaluate_circuit(circuit, inputs):
    values = {gate: None for gate in circuit}
    for gate in sorted(circuit.keys()):
        if gate.startswith('input'):
            values[gate] = inputs[int(gate.split('_')[1])]
        else:
            gate_type, *operands = circuit[gate]
            if gate_type == 'NOT':
                values[gate] = 1 - values[operands[0]]
            elif gate_type == 'MOD_2':
                values[gate] = values[operands[0]] ^ values[operands[1]]
            else:
                op_values = [values[op] for op in operands]
                if gate_type == 'AND':
                    values[gate] = all(op_values)
                elif gate_type == 'OR':
                    values[gate] = any(op_values)
    return values['output']

def generate_circuit(d, s, n):
    circuit = {}
    layers = [[] for _ in range(d + 1)]
    for i in range(n):
        circuit[f'input_{i}'] = ('input',)
        layers[0].append(f'input_{i}')

    gate_types = ['AND', 'OR', 'NOT', 'MOD_2']
    for layer in range(1, d + 1):
        num_gates = min(s, len(layers[layer - 1]) * 2)
        for i in range(num_gates):
            gate_type = random.choice(gate_types)
            if gate_type == 'NOT':
                fan_in = 1
            else:
                fan_in = random.randint(2, min(4, len(layers[layer - 1])))
            operands = random.sample(layers[layer - 1], fan_in)
            gate_name = f'gate_{layer}_{i}'
            circuit[gate_name] = (gate_type,) + tuple(operands)
            layers[layer].append(gate_name)

    circuit['output'] = ('AND', layers[-1][0]) if layers[-1] else ('input',)
    return circuit

def compute_bias(circuit, n):
    correct = 0
    total = 2 ** n
    for i in range(total):
        inputs = [(i >> j) & 1 for j in range(n)]
        output = evaluate_circuit(circuit, inputs)
        mod3 = sum(inputs) % 3
        if output == mod3:
            correct += 1
    bias = 2 * (correct / total) - 1
    return bias

def build_graph(circuit):
    graph = {gate: [] for gate in circuit}
    for gate in circuit:
        if not gate.startswith('input'):
            for operand in circuit[gate][1:]:
                graph[operand].append(gate)
                graph[gate].append(operand)
    return graph

def run_trial(seed):
    random.seed(seed)
    d_values = [2, 3, 4]
    s_values = [12, 18, 24]
    n_values = [8, 10, 12]
    max_ratio = 0.0
    counterexample = ""
    instances_tested = 0

    for d in d_values:
        for s in s_values:
            for n in n_values:
                for _ in range(6):
                    circuit = generate_circuit(d, s, n)
                    graph = build_graph(circuit)
                    delta = compute_delta(graph)
                    bias = compute_bias(circuit, n)
                    lhs = (bias ** 2) * n
                    rhs = (1 + delta) * (2 ** d)
                    ratio = lhs / rhs if rhs != 0 else float('inf')
                    if ratio > max_ratio:
                        max_ratio = ratio
                    if ratio > 1.0:
                        counterexample = f"d={d}, s={s}, n={n}, seed={seed}, ratio={ratio}"
                    instances_tested += 1

    conjecture_holds = max_ratio <= 1.0
    return {
        "metric_name": "max_LHS/RHS_ratio",
        "metric_value": max_ratio,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    metric_values = []
    support_counts = 0
    counterexample = ""

    for seed in seeds:
        trial = run_trial(seed)
        print(f"TRIAL: {trial}")
        metric_values.append(trial["metric_value"])
        if trial["conjecture_holds"]:
            support_counts += 1
        if trial["counterexample"]:
            counterexample = trial["counterexample"]

    mean = sum(metric_values) / len(metric_values)
    std = math.sqrt(sum((x - mean) ** 2 for x in metric_values) / len(metric_values))
    support_fraction = support_counts / len(seeds)

    if counterexample:
        print(f'RESULT: FALSIFIED counterexample="{counterexample}" first_failing_seed={seeds[0]}')
    elif support_fraction >= 0.8:
        print(f'RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}')
    else:
        print('RESULT: INCONCLUSIVE reason=insufficient_support')