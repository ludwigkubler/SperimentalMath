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

def generate_random_circuit(n, d, N):
    gate_types = ['AND', 'OR', 'MOD-2']
    circuit = []
    for _ in range(N):
        depth = random.randint(1, d)
        gate_type = random.choice(gate_types)
        inputs = []
        if depth > 1:
            possible_inputs = [i for i in range(len(circuit)) if circuit[i][0] < depth]
            if len(possible_inputs) >= 2:
                inputs = random.sample(possible_inputs, 2)
        circuit.append((depth, gate_type, inputs))
    return circuit

def compute_truth_table(circuit, n):
    truth_table = {}
    for x in range(2**n):
        inputs = [(x >> i) & 1 for i in range(n)]
        values = inputs.copy()
        for depth, gate_type, ins in circuit:
            if gate_type == 'AND':
                values.append(values[ins[0]] & values[ins[1]])
            elif gate_type == 'OR':
                values.append(values[ins[0]] | values[ins[1]])
            elif gate_type == 'MOD-2':
                values.append(values[ins[0]] ^ values[ins[1]])
        truth_table[x] = values[-1]
    return truth_table

def compute_sensitivity(truth_table, n):
    sensitivity = 0
    for x in truth_table:
        for i in range(n):
            x_flipped = x ^ (1 << i)
            if truth_table[x] != truth_table.get(x_flipped, truth_table[x]):
                sensitivity += 1
    return sensitivity / (2**n)

def build_quiver(circuit, n):
    quiver = defaultdict(lambda: defaultdict(int))
    for i in range(n):
        quiver[i] = defaultdict(int)
    for j, (depth, gate_type, inputs) in enumerate(circuit, start=n):
        for i in inputs:
            quiver[i][j] += 1
    return quiver

def mutate_quiver(quiver, v):
    mutated = defaultdict(lambda: defaultdict(int))
    for i in quiver:
        for j in quiver[i]:
            if i == v or j == v:
                continue
            if i in quiver[v] and j in quiver[v]:
                mutated[i][j] += quiver[i][v] * quiver[v][j]
            if i in quiver and v in quiver[i]:
                mutated[i][j] += quiver[i][v]
            if v in quiver and j in quiver[v]:
                mutated[i][j] += quiver[v][j]
    return mutated

def weisfeiler_lehman(quiver, labels, rounds=3):
    for _ in range(rounds):
        new_labels = {}
        for v in quiver:
            neighbors = []
            for u in quiver[v]:
                neighbors.extend([(u, quiver[v][u])] * quiver[v][u])
            neighbors.sort()
            new_label = (labels[v], tuple(neighbors))
            new_labels[v] = new_label
        labels = new_labels
    return labels

def compute_nbhd_size(quiver, labels):
    nbhd = set()
    for v in quiver:
        mutated = mutate_quiver(quiver, v)
        mutated_labels = weisfeiler_lehman(mutated, labels)
        signature = tuple(sorted(mutated_labels.values()))
        nbhd.add(signature)
    return len(nbhd)

def run_trial(seed):
    random.seed(seed)
    n = random.choice([4, 5, 6])
    d = random.choice([2, 3])
    N = random.randint(n, min(3*n, 25))
    circuit = generate_random_circuit(n, d, N)
    truth_table = compute_truth_table(circuit, n)
    I_f = compute_sensitivity(truth_table, n)
    quiver = build_quiver(circuit, n)
    labels = {i: ('input',) for i in range(n)}
    for j, (depth, gate_type, _) in enumerate(circuit, start=n):
        labels[j] = (gate_type, depth)
    nbhd_size = compute_nbhd_size(quiver, labels)
    bound = math.ceil(I_f / (4 * (d + 1)))
    conjecture_holds = nbhd_size >= bound
    counterexample = ""
    if not conjecture_holds:
        counterexample = f"n={n}, d={d}, N={N}, seed={seed}, nbhd_size={nbhd_size}, I_f={I_f}, circuit={circuit}"
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
    if support_fraction >= 0.98:
        print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
    else:
        counterexamples = [r["counterexample"] for r in results if not r["conjecture_holds"]]
        if counterexamples:
            print(f"RESULT: FALSIFIED counterexample={counterexamples[0]} first_failing_seed={seeds[results.index([r for r in results if not r['conjecture_holds']][0])]}")
        else:
            print("RESULT: INCONCLUSIVE reason=insufficient_support")