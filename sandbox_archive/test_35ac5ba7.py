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

def compute_truth_table(circuit, n):
    truth_table = []
    for x in range(2**n):
        inputs = [(x >> i) & 1 for i in range(n)]
        values = inputs.copy()
        for gate in circuit:
            ins = gate['inputs']
            if ins[0] >= len(values) or ins[1] >= len(values):
                raise IndexError("Input index out of range")
            if gate['type'] == 'AND':
                values.append(values[ins[0]] & values[ins[1]])
            elif gate['type'] == 'OR':
                values.append(values[ins[0]] | values[ins[1]])
            elif gate['type'] == 'MOD-2':
                values.append(values[ins[0]] ^ values[ins[1]])
        truth_table.append(values[-1])
    return truth_table

def compute_sensitivity(truth_table, n):
    sensitivity = 0
    for x in range(2**n):
        base = truth_table[x]
        for i in range(n):
            flipped = x ^ (1 << i)
            if truth_table[flipped] != base:
                sensitivity += 1
    return sensitivity / (2**n)

def build_quiver(circuit, n):
    quiver = defaultdict(lambda: defaultdict(int))
    for i in range(n):
        quiver[i] = defaultdict(int)
    for idx, gate in enumerate(circuit, start=n):
        for inp in gate['inputs']:
            quiver[inp][idx] += 1
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
            elif v == vertex:
                for w in quiver[u]:
                    if w != vertex:
                        new_quiver[u][w] += quiver[u][v] * quiver[v][w]
    for u in new_quiver:
        for v in new_quiver[u]:
            if u in new_quiver[v] and new_quiver[v][u] > 0:
                cancel = min(new_quiver[u][v], new_quiver[v][u])
                new_quiver[u][v] -= cancel
                new_quiver[v][u] -= cancel
                if new_quiver[u][v] == 0:
                    del new_quiver[u][v]
                if new_quiver[v][u] == 0:
                    del new_quiver[v][u]
    return new_quiver

def weisfeiler_lehman(quiver, max_iter=3):
    colors = {}
    for u in quiver:
        colors[u] = 0
    for _ in range(max_iter):
        new_colors = {}
        for u in quiver:
            neighbors = []
            for v in quiver[u]:
                neighbors.append((colors[v], quiver[u][v]))
            for v in quiver:
                if u in quiver[v]:
                    neighbors.append((colors[v], quiver[v][u]))
            neighbors.sort()
            new_colors[u] = hash(tuple(neighbors))
        if new_colors == colors:
            break
        colors = new_colors
    return colors

def run_trial(seed):
    random.seed(seed)
    n = random.choice([4, 5, 6])
    d = random.choice([2, 3])
    N = random.randint(n, min(3*n, 25))

    gate_types = ['AND', 'OR', 'MOD-2']
    circuit = []
    for _ in range(N):
        if len(circuit) < 2:
            inputs = [random.randint(0, n-1), random.randint(0, n-1)]
        else:
            inputs = [random.randint(0, n + len(circuit) - 1),
                      random.randint(0, n + len(circuit) - 1)]
        gate_type = random.choice(gate_types)
        circuit.append({'type': gate_type, 'inputs': inputs})

    truth_table = compute_truth_table(circuit, n)
    I_f = compute_sensitivity(truth_table, n)

    quiver = build_quiver(circuit, n)
    mutated_quivers = []
    for v in quiver:
        mutated = mutate_quiver(quiver, v)
        mutated_quivers.append(mutated)

    signatures = set()
    for mq in mutated_quivers:
        colors = weisfeiler_lehman(mq)
        signature = tuple(sorted(colors.values()))
        signatures.add(signature)

    NbhdSize = len(signatures)
    bound = math.ceil(I_f / (4 * (d + 1)))

    conjecture_holds = NbhdSize >= bound
    counterexample = ""
    if not conjecture_holds:
        counterexample = f"n={n}, d={d}, N={N}, seed={seed}, NbhdSize={NbhdSize}, I(f)={I_f}"

    return {
        "metric_name": "NbhdSize",
        "metric_value": NbhdSize,
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

    if support_fraction >= 0.98:
        print(f"RESULT: SUPPORTED mean={mean:.2f} std={std:.2f} support_fraction={support_fraction:.2f}")
    else:
        failing = [r for r in results if not r["conjecture_holds"]]
        if failing:
            first_failing = failing[0]
            print(f"RESULT: FALSIFIED counterexample=\"{first_failing['counterexample']}\" first_failing_seed={first_failing['seed']}")
        else:
            print("RESULT: INCONCLUSIVE reason=unknown")