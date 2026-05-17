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
    circuit = []
    layers = [[] for _ in range(d + 1)]

    # Input layer
    layers[0] = list(range(n))

    for _ in range(N):
        depth = random.randint(1, d)
        gate_type = random.choice(gate_types)
        inputs = []
        for _ in range(2):
            if depth == 1:
                inputs.append(random.choice(layers[0]))
            else:
                inputs.append(random.choice(layers[depth - 1]))
        gate_id = n + len(circuit)
        circuit.append((gate_type, inputs, depth))
        layers[depth].append(gate_id)

    return circuit

def evaluate_circuit(circuit, n):
    truth_table = {}
    for x in itertools.product([0, 1], repeat=n):
        x = list(x)
        values = {i: x[i] for i in range(n)}
        for gate_type, inputs, _ in circuit:
            gate_id = n + list(values.keys()).index(inputs[0]) if len(values) > n else n + len(values) - n
            if gate_type == 'AND':
                values[gate_id] = values[inputs[0]] and values[inputs[1]]
            elif gate_type == 'OR':
                values[gate_id] = values[inputs[0]] or values[inputs[1]]
            elif gate_type == 'MOD-2':
                values[gate_id] = (values[inputs[0]] + values[inputs[1]]) % 2
        truth_table[tuple(x)] = values[max(values.keys())]
    return truth_table

def compute_sensitivity(truth_table, n):
    sensitivity = 0
    for x in truth_table:
        f_x = truth_table[x]
        for i in range(n):
            x_flipped = list(x)
            x_flipped[i] = 1 - x_flipped[i]
            f_x_flipped = truth_table[tuple(x_flipped)]
            if f_x != f_x_flipped:
                sensitivity += 1
    return sensitivity / (2 ** n)

def build_quiver(circuit, n):
    quiver = defaultdict(lambda: defaultdict(int))
    for gate_id, (gate_type, inputs, depth) in enumerate(circuit, start=n):
        for i in inputs:
            quiver[i][gate_id] += 1
    return quiver

def mutate_quiver(quiver, v):
    mutated = defaultdict(lambda: defaultdict(int))
    for u in list(quiver.keys()):
        for w in list(quiver[u].keys()):
            if u == v or w == v:
                continue
            if u == v or w == v:
                mutated[w][u] += quiver[u][w]
            else:
                mutated[u][w] += quiver[u][w]
    for u in list(quiver.keys()):
        if u == v:
            continue
        for w in list(quiver[u].keys()):
            if w == v:
                continue
            for z in list(quiver[w].keys()):
                if z == v:
                    continue
                mutated[u][z] += quiver[u][w] * quiver[w][z]
    for u in list(mutated.keys()):
        for w in list(mutated[u].keys()):
            if mutated[u][w] == mutated[w][u]:
                del mutated[u][w]
                del mutated[w][u]
    return mutated

def weisfeiler_lehman(quiver, max_iter=3):
    colors = {}
    for v in quiver:
        colors[v] = 0
    for _ in range(max_iter):
        new_colors = {}
        for v in quiver:
            neighbors = []
            for u in quiver:
                if v in quiver[u]:
                    neighbors.append((u, quiver[u][v]))
            neighbors.sort()
            color = (colors[v], tuple(neighbors))
            new_colors[v] = color
        if new_colors == colors:
            break
        colors = new_colors
    return colors

def count_distinct_mutations(quiver):
    distinct = set()
    for v in quiver:
        mutated = mutate_quiver(quiver, v)
        colors = weisfeiler_lehman(mutated)
        signature = tuple(sorted(colors.items()))
        distinct.add(signature)
    return len(distinct)

def run_trial(seed):
    n = random.choice([4, 5, 6])
    d = random.choice([2, 3])
    N = random.randint(n, min(3 * n, 25))

    circuit = generate_circuit(n, d, N, seed)
    truth_table = evaluate_circuit(circuit, n)
    I_f = compute_sensitivity(truth_table, n)
    quiver = build_quiver(circuit, n)
    nbhd_size = count_distinct_mutations(quiver)

    bound = math.ceil(I_f / (4 * (d + 1)))
    conjecture_holds = nbhd_size >= bound

    counterexample = ""
    if not conjecture_holds:
        counterexample = f"n={n}, d={d}, N={N}, seed={seed}, nbhd_size={nbhd_size}, I(f)={I_f}"

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
        print(f"TRIAL: {result}")
        results.append(result)

    metric_values = [r["metric_value"] for r in results]
    mean = sum(metric_values) / len(metric_values)
    std = math.sqrt(sum((x - mean) ** 2 for x in metric_values) / len(metric_values))
    support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)

    if support_fraction >= 0.98 and all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
    else:
        for r in results:
            if not r["conjecture_holds"]:
                print(f"RESULT: FALSIFIED counterexample=\"{r['counterexample']}\" first_failing_seed={seeds[results.index(r)]}")
                break