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
from collections import defaultdict, deque

def generate_circuit(n, d, N, seed):
    random.seed(seed)
    gate_types = ['AND', 'OR', 'MOD-2']
    layers = [[] for _ in range(d + 1)]
    inputs = [f'x{i}' for i in range(n)]
    layers[0] = inputs.copy()

    for depth in range(1, d + 1):
        for _ in range(N // d):
            if not layers[depth - 1]:
                break
            gate_type = random.choice(gate_types)
            input1 = random.choice(layers[depth - 1])
            input2 = random.choice(layers[depth - 1])
            gate_name = f'{gate_type}_{depth}_{_}'
            layers[depth].append(gate_name)

    circuit = {'inputs': inputs, 'layers': layers, 'output': layers[-1][0] if layers[-1] else None}
    return circuit

def build_quiver(circuit):
    quiver = defaultdict(lambda: defaultdict(int))
    layers = circuit['layers']

    for depth in range(1, len(layers)):
        for gate in layers[depth]:
            gate_type, _, _ = gate.split('_')
            for input_gate in layers[depth - 1]:
                quiver[input_gate][gate] += 1

    return quiver

def mutate_quiver(quiver, vertex):
    new_quiver = defaultdict(lambda: defaultdict(int))

    for u in quiver:
        for v in quiver[u]:
            if u == vertex or v == vertex:
                continue
            new_quiver[u][v] = quiver[u][v]

    for u in quiver:
        for v in quiver[u]:
            if u == vertex:
                for w in quiver[v]:
                    if w != vertex:
                        new_quiver[w][v] += quiver[u][v] * quiver[v][w]

    for u in new_quiver:
        for v in new_quiver[u]:
            if u == v:
                del new_quiver[u][v]

    return new_quiver

def weisfeiler_lehman(quiver, max_rounds=3):
    color = {}
    for u in quiver:
        color[u] = u.split('_')[0] if '_' in u else u

    for _ in range(max_rounds):
        new_color = {}
        for u in quiver:
            neighbors = sorted([(v, quiver[u][v]) for v in quiver[u]], key=lambda x: x[0])
            color_str = f"{color[u]}_{tuple(neighbors)}"
            new_color[u] = color_str
        color = new_color

    return frozenset(color.values())

def compute_sensitivity(circuit, n):
    inputs = circuit['inputs']
    layers = circuit['layers']
    output_gate = circuit['output']

    if not output_gate:
        return 0.0

    truth_table = {}
    for x in itertools.product([0, 1], repeat=n):
        x = list(x)
        values = {g: 0 for layer in layers for g in layer}
        for i, val in enumerate(x):
            values[inputs[i]] = val

        for depth in range(1, len(layers)):
            for gate in layers[depth]:
                gate_type, _, _ = gate.split('_')
                input1 = layers[depth - 1][0] if layers[depth - 1] else None
                input2 = layers[depth - 1][1] if len(layers[depth - 1]) > 1 else None
                if input1 and input2:
                    if gate_type == 'AND':
                        values[gate] = values[input1] and values[input2]
                    elif gate_type == 'OR':
                        values[gate] = values[input1] or values[input2]
                    elif gate_type == 'MOD-2':
                        values[gate] = values[input1] ^ values[input2]

        truth_table[tuple(x)] = values[output_gate]

    sensitivity = 0.0
    for x in truth_table:
        for i in range(n):
            x_flipped = list(x)
            x_flipped[i] = 1 - x_flipped[i]
            sensitivity += truth_table[x] != truth_table[tuple(x_flipped)]

    return sensitivity / (2 ** n)

def run_trial(seed):
    random.seed(seed)
    n = random.choice([4, 5, 6])
    d = random.choice([2, 3])
    N = random.randint(n, min(3 * n, 25))

    circuit = generate_circuit(n, d, N, seed)
    quiver = build_quiver(circuit)

    mutation_neighborhood = set()
    for vertex in quiver:
        mutated_quiver = mutate_quiver(quiver, vertex)
        signature = weisfeiler_lehman(mutated_quiver)
        mutation_neighborhood.add(signature)

    nbhd_size = len(mutation_neighborhood)
    sensitivity = compute_sensitivity(circuit, n)
    bound = math.ceil(sensitivity / (4 * (d + 1)))

    conjecture_holds = nbhd_size >= bound
    counterexample = f"n={n}, d={d}, N={N}, seed={seed}, nbhd_size={nbhd_size}, sensitivity={sensitivity}" if not conjecture_holds else ""

    return {
        "metric_name": "NbhdSize",
        "metric_value": nbhd_size,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]

    results = []
    for seed in seeds:
        result = run_trial(seed)
        result["seed"] = seed
        print(f"TRIAL: {result}")
        results.append(result)

    metric_values = [r["metric_value"] for r in results]
    mean = sum(metric_values) / len(metric_values)
    std = math.sqrt(sum((x - mean) ** 2 for x in metric_values) / len(metric_values))
    support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
    else:
        failing_trials = [r for r in results if not r["conjecture_holds"]]
        first_failing_seed = failing_trials[0]["seed"]
        counterexample = failing_trials[0]["counterexample"]
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")