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
from collections import defaultdict

def matrix_mult(A, B):
    return [[sum(a * b for a, b in zip(row, col)) for col in zip(*B)] for row in A]

def generate_random_circuit(n, s, depth):
    gates = []
    for i in range(s):
        gate_type = random.choice(['AND', 'OR', 'NOT', 'MOD_2'])
        inputs = []
        if gate_type == 'NOT':
            if i > 0:
                inputs = [random.randint(0, i-1)]
        else:
            if i > 1:
                num_inputs = random.randint(1, min(3, i))
                inputs = random.sample(range(i), num_inputs)
        gates.append({'type': gate_type, 'inputs': inputs})
    return gates

def evaluate_circuit(circuit, inp):
    values = list(inp)
    for gate in circuit:
        if gate['type'] == 'NOT':
            if gate['inputs']:
                values.append(1 - values[gate['inputs'][0]])
            else:
                values.append(0)
        elif gate['type'] == 'AND':
            val = 1
            for i in gate['inputs']:
                val *= values[i]
            values.append(val)
        elif gate['type'] == 'OR':
            val = 0
            for i in gate['inputs']:
                val = max(val, values[i])
            values.append(val)
        elif gate['type'] == 'MOD_2':
            val = sum(values[i] for i in gate['inputs']) % 2
            values.append(val)
    return values[-1] if values else 0

def compute_correlation(circuit, n, target_func):
    total = 0
    count = 0
    for inp in itertools.product([0, 1], repeat=n):
        if len(inp) != n:
            continue
        output = evaluate_circuit(circuit, inp)
        target = target_func(inp)
        total += output * target
        count += 1
    if count == 0:
        return 0.0
    return total / count

def compute_out_degrees(circuit):
    degrees = [0] * len(circuit)
    for gate in circuit:
        for i in gate['inputs']:
            degrees[i] += 1
    return degrees

def compute_additive_energy(degrees):
    s = len(degrees)
    if s == 0:
        return 0.0
    sum_counts = defaultdict(int)
    for i, j in itertools.product(range(s), repeat=2):
        sum_counts[degrees[i] + degrees[j]] += 1
    energy = 0
    for k, l in itertools.product(range(s), repeat=2):
        energy += sum_counts.get(degrees[k] + degrees[l], 0)
    return energy / (s ** 3)

def run_trial(seed):
    random.seed(seed)
    n = random.choice([6, 7, 8])
    s = random.choice([12, 20, 28, 36])
    depth = 3

    # Generate random circuits
    circuits = [generate_random_circuit(n, s, depth) for _ in range(50)]

    # Filter circuits with corr(f_C, MOD_3) ≥ 0.9
    filtered_circuits = []
    for circuit in circuits:
        corr_mod3 = compute_correlation(circuit, n, lambda x: sum(x) % 3)
        if corr_mod3 >= 0.9:
            filtered_circuits.append(circuit)

    if not filtered_circuits:
        return {
            'metric_name': 'additive_energy',
            'metric_value': 0.0,
            'instances_tested': 0,
            'conjecture_holds': False,
            'counterexample': 'No valid circuits generated'
        }

    # Compute additive energy for filtered circuits
    energies = []
    for circuit in filtered_circuits:
        degrees = compute_out_degrees(circuit)
        energy = compute_additive_energy(degrees)
        energies.append(energy)

    if not energies:
        return {
            'metric_name': 'additive_energy',
            'metric_value': 0.0,
            'instances_tested': 0,
            'conjecture_holds': False,
            'counterexample': 'No valid circuits generated'
        }

    metric_value = sum(energies) / len(energies)
    instances_tested = len(filtered_circuits)
    conjecture_holds = all(e * (math.log(s + 1) ** 2) >= 0.1 for e in energies)

    return {
        'metric_name': 'additive_energy',
        'metric_value': metric_value,
        'instances_tested': instances_tested,
        'conjecture_holds': conjecture_holds,
        'counterexample': '' if conjecture_holds else f'Found circuit with E(C) < 0.1 / log²(s+1)'
    }

if __name__ == '__main__':
    seeds = [int(arg) for arg in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]

    trials = []
    for seed in seeds:
        trial = run_trial(seed)
        print(f"TRIAL: {trial}")
        trials.append(trial)

    metric_values = [t['metric_value'] for t in trials if t['instances_tested'] > 0]
    if metric_values:
        mean = sum(metric_values) / len(metric_values)
        std = math.sqrt(sum((x - mean) ** 2 for x in metric_values) / len(metric_values))
    else:
        mean = 0.0
        std = 0.0

    support_fraction = sum(1 for t in trials if t['conjecture_holds']) / len(trials)

    if all(t['conjecture_holds'] for t in trials):
        print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
    elif any(not t['conjecture_holds'] for t in trials):
        first_failing_seed = next(t['seed'] for t in trials if not t['conjecture_holds'])
        print(f"RESULT: FALSIFIED counterexample='{trials[0]['counterexample']}' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_data")