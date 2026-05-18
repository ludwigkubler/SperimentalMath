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

def generate_random_circuit(n, s, depth):
    gates = []
    for i in range(s):
        gate_type = random.choice(['AND', 'OR', 'NOT', 'MOD_2'])
        inputs = []
        if i > 0:
            max_inputs = min(i, 5)  # Limit fan-in to avoid excessive complexity
            num_inputs = random.randint(1, max_inputs)
            inputs = random.sample(range(i), num_inputs)
        gates.append((gate_type, inputs))
    return gates

def compute_out_degrees(circuit):
    out_degrees = [0] * len(circuit)
    for i, (gate_type, inputs) in enumerate(circuit):
        for j in inputs:
            out_degrees[j] += 1
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
        return 0.0  # Avoid excessive computation for large n
    inputs = list(itertools.product([0, 1], repeat=n))
    correct = 0
    for inp in inputs:
        output = evaluate_circuit(circuit, inp)
        if output == target_func(inp):
            correct += 1
    return correct / (2 ** n)

def evaluate_circuit(circuit, input_values):
    values = list(input_values)
    for gate_type, inputs in circuit:
        if gate_type == 'AND':
            val = 1
            for i in inputs:
                val &= values[i]
            values.append(val)
        elif gate_type == 'OR':
            val = 0
            for i in inputs:
                val |= values[i]
            values.append(val)
        elif gate_type == 'NOT':
            val = 1 - values[inputs[0]]
            values.append(val)
        elif gate_type == 'MOD_2':
            val = sum(values[i] for i in inputs) % 2
            values.append(val)
    return values[-1]

def run_trial(seed):
    random.seed(seed)
    n_values = [6, 7, 8]
    s_values = [12, 20, 28, 36]
    trials_per_config = 12  # 30 seeds × 4 n × 2 s = 240 total trials
    metric_values = []
    conjecture_holds = True
    counterexample = ""
    instances_tested = 0

    for n in n_values:
        for s in s_values:
            for _ in range(trials_per_config):
                circuit = generate_random_circuit(n, s, 3)
                out_degrees = compute_out_degrees(circuit)
                energy = compute_additive_energy(out_degrees)
                corr_mod3 = compute_correlation(circuit, n, lambda x: sum(x) % 3)
                corr_and = compute_correlation(circuit, n, lambda x: all(x))

                if corr_mod3 >= 0.9:
                    if energy * math.log(s + 1) ** 2 < 0.1:
                        conjecture_holds = False
                        counterexample = f"MOD_3-correlated circuit with E·log²(s) < 0.1: n={n}, s={s}, seed={seed}"
                        break
                elif corr_and >= 0.9:
                    pass  # Control case, no action needed
                else:
                    if energy * math.sqrt(s) / math.log(s + 1) > 1:
                        conjecture_holds = False
                        counterexample = f"Random circuit with E·sqrt(s)/log(s) > 1: n={n}, s={s}, seed={seed}"
                        break

                metric_values.append(energy)
                instances_tested += 1

            if not conjecture_holds:
                break
        if not conjecture_holds:
            break

    if not metric_values:
        return {
            "metric_name": "additive_energy",
            "metric_value": 0.0,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "No valid circuits generated"
        }

    mean_metric = sum(metric_values) / len(metric_values)
    return {
        "metric_name": "additive_energy",
        "metric_value": mean_metric,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    trials = []
    total_instances = 0
    total_metric = 0.0
    support_count = 0

    for seed in seeds:
        trial = run_trial(seed)
        print(f"TRIAL: {trial}")
        trials.append(trial)
        total_instances += trial["instances_tested"]
        total_metric += trial["metric_value"]
        if trial["conjecture_holds"]:
            support_count += 1

    if not trials:
        print("RESULT: INCONCLUSIVE reason=no_trials_executed")
        sys.exit(0)

    mean_metric = total_metric / len(trials)
    std_metric = math.sqrt(sum((trial["metric_value"] - mean_metric) ** 2 for trial in trials) / len(trials))
    support_fraction = support_count / len(trials)

    if any(not trial["conjecture_holds"] for trial in trials):
        first_failure = next(trial for trial in trials if not trial["conjecture_holds"])
        print(f'RESULT: FALSIFIED counterexample="{first_failure["counterexample"]}" first_failing_seed={seeds[trials.index(first_failure)]}')
    elif support_fraction >= 0.8:
        print(f'RESULT: SUPPORTED mean={mean_metric:.4f} std={std_metric:.4f} support_fraction={support_fraction:.4f}')
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_support")