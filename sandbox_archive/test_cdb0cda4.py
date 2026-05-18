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

def generate_random_circuit(n, s):
    circuit = []
    for _ in range(s):
        gate_type = random.choice(['AND', 'OR', 'NOT', 'MOD_2'])
        if gate_type == 'NOT':
            inputs = [random.randint(0, len(circuit) - 1)] if circuit else []
        else:
            min_inputs = 2 if gate_type in ['AND', 'OR', 'MOD_2'] else 1
            max_inputs = min(4, len(circuit)) if circuit else 0
            if max_inputs < min_inputs:
                inputs = []
            else:
                num_inputs = random.randint(min_inputs, max_inputs)
                inputs = random.sample(range(len(circuit)), num_inputs) if circuit else []
        circuit.append({'type': gate_type, 'inputs': inputs})
    return circuit

def compute_out_degrees(circuit):
    out_degrees = [0] * len(circuit)
    for gate in circuit:
        for input_idx in gate['inputs']:
            out_degrees[input_idx] += 1
    return out_degrees

def compute_additive_energy(out_degrees):
    s = len(out_degrees)
    if s == 0:
        return 0.0
    sum_counts = defaultdict(int)
    for i, j in itertools.product(range(s), repeat=2):
        sum_counts[out_degrees[i] + out_degrees[j]] += 1
    energy = 0
    for count in sum_counts.values():
        energy += count * count
    return energy / (s * s * s)

def compute_correlation(circuit, n, target_func):
    if n > 8:
        return 0.0
    inputs = list(itertools.product([0, 1], repeat=n))
    corr = 0.0
    for input_tuple in inputs:
        output = evaluate_circuit(circuit, input_tuple)
        corr += output * target_func(input_tuple)
    corr /= (2 ** n)
    return corr

def evaluate_circuit(circuit, input_tuple):
    values = list(input_tuple)
    for gate in circuit:
        if gate['type'] == 'NOT':
            values.append(1 - values[gate['inputs'][0]])
        elif gate['type'] == 'AND':
            val = 1
            for idx in gate['inputs']:
                val &= values[idx]
            values.append(val)
        elif gate['type'] == 'OR':
            val = 0
            for idx in gate['inputs']:
                val |= values[idx]
            values.append(val)
        elif gate['type'] == 'MOD_2':
            val = sum(values[idx] for idx in gate['inputs']) % 2
            values.append(val)
    return values[-1] if values else 0

def run_trial(seed):
    random.seed(seed)
    n = random.choice([6, 7, 8])
    s = random.choice([12, 20, 28, 36])
    circuits = []
    for _ in range(50):
        circuit = generate_random_circuit(n, s)
        circuits.append(circuit)
    mod3_circuits = []
    and_circuits = []
    for circuit in circuits:
        corr_mod3 = compute_correlation(circuit, n, lambda x: sum(x) % 3)
        corr_and = compute_correlation(circuit, n, lambda x: all(x))
        if corr_mod3 >= 0.9:
            mod3_circuits.append(circuit)
        if corr_and >= 0.9:
            and_circuits.append(circuit)
    if not mod3_circuits:
        return {
            "metric_name": "E(C)*log²(s+1)",
            "metric_value": 0.0,
            "instances_tested": len(circuits),
            "conjecture_holds": False,
            "counterexample": "No MOD_3-correlated circuits found"
        }
    min_mod3_energy = float('inf')
    for circuit in mod3_circuits:
        out_degrees = compute_out_degrees(circuit)
        energy = compute_additive_energy(out_degrees)
        min_mod3_energy = min(min_mod3_energy, energy * math.log(s + 1) ** 2)
    random_energy_values = []
    for circuit in circuits:
        out_degrees = compute_out_degrees(circuit)
        energy = compute_additive_energy(out_degrees)
        random_energy_values.append(energy * math.sqrt(s) / math.log(s + 1))
    fraction_random = sum(1 for x in random_energy_values if x <= 1) / len(random_energy_values)
    corr_values = []
    energy_values = []
    for circuit in circuits + mod3_circuits + and_circuits:
        corr_mod3 = compute_correlation(circuit, n, lambda x: sum(x) % 3)
        out_degrees = compute_out_degrees(circuit)
        energy = compute_additive_energy(out_degrees)
        corr_values.append(corr_mod3)
        energy_values.append(math.log(energy * math.log(s + 1) ** 2))
    pearson_r = compute_pearson(corr_values, energy_values)
    conjecture_holds = (min_mod3_energy >= 0.1) and (fraction_random >= 0.9) and (pearson_r >= 0.4)
    counterexample = ""
    if not conjecture_holds:
        if min_mod3_energy < 0.1:
            counterexample = f"MOD_3-correlated circuit with E(C)*log²(s+1) = {min_mod3_energy}"
        elif fraction_random < 0.9:
            counterexample = f"Random circuit with E(C)*s^1/2/log(s+1) > 1"
        else:
            counterexample = f"Pearson r = {pearson_r} < 0.4"
    return {
        "metric_name": "E(C)*log²(s+1)",
        "metric_value": min_mod3_energy,
        "instances_tested": len(circuits),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

def compute_pearson(x, y):
    n = len(x)
    if n == 0:
        return 0.0
    mean_x = sum(x) / n
    mean_y = sum(y) / n
    cov = sum((xi - mean_x) * (yi - mean_y) for xi, yi in zip(x, y)) / n
    std_x = math.sqrt(sum((xi - mean_x) ** 2 for xi in x) / n)
    std_y = math.sqrt(sum((yi - mean_y) ** 2 for yi in y) / n)
    if std_x == 0 or std_y == 0:
        return 0.0
    return cov / (std_x * std_y)

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    trials = []
    for seed in seeds:
        trial = run_trial(seed)
        print(f"TRIAL: {trial}")
        trials.append(trial)
    metric_values = [trial["metric_value"] for trial in trials]
    mean_metric = sum(metric_values) / len(metric_values)
    std_metric = math.sqrt(sum((x - mean_metric) ** 2 for x in metric_values) / len(metric_values))
    support_fraction = sum(1 for trial in trials if trial["conjecture_holds"]) / len(trials)
    if all(trial["conjecture_holds"] for trial in trials):
        print(f"RESULT: SUPPORTED mean={mean_metric} std={std_metric} support_fraction={support_fraction}")
    elif any(not trial["conjecture_holds"] for trial in trials):
        first_failing_seed = next(seed for seed, trial in zip(seeds, trials) if not trial["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{trials[seeds.index(first_failing_seed)]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=all_trials_failed")