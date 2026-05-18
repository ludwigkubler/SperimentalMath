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

def generate_random_acc02_circuit(n, s):
    gate_types = ['AND', 'OR', 'MOD_2', 'NOT']
    gates = []
    for _ in range(s):
        gate_type = random.choice(gate_types)
        if gate_type == 'NOT':
            fanin = 1
        else:
            fanin = random.randint(2, min(4, int(math.log2(s)) + 2))
        inputs = random.sample(range(len(gates)), fanin) if len(gates) > 0 else []
        gates.append((gate_type, inputs))
    return gates

def dfs_labeling(gates):
    labeled = [False] * len(gates)
    labels = [0] * len(gates)
    current_label = 1
    stack = [(len(gates) - 1, False)]

    while stack:
        gate_idx, visited = stack.pop()
        if visited:
            labels[gate_idx] = current_label
            current_label += 1
            continue
        if not labeled[gate_idx]:
            labeled[gate_idx] = True
            stack.append((gate_idx, True))
            gate_type, inputs = gates[gate_idx]
            for input_idx in sorted(inputs, key=lambda x: (gates[x][0], x)):
                if not labeled[input_idx]:
                    stack.append((input_idx, False))
    return labels

def compute_spectrum_dimension(gate, labels, p):
    gate_type, inputs = gate
    if gate_type != 'MOD_2' or len(inputs) < 4:
        return 0
    count = 0
    for xi in range(1, p):
        sum_real = 0.0
        sum_imag = 0.0
        for a_j in inputs:
            angle = 2 * math.pi * labels[a_j] * xi / p
            sum_real += math.cos(angle)
            sum_imag += math.sin(angle)
        magnitude = math.sqrt(sum_real**2 + sum_imag**2)
        if magnitude >= len(inputs) / 2:
            count += 1
    return count

def run_trial(seed):
    random.seed(seed)
    n_values = [6, 8, 10, 12]
    s_values = [15, 30, 60]
    max_chi = 0
    instances_tested = 0
    counterexample = ""

    for n, s in itertools.product(n_values, s_values):
        for _ in range(30):
            circuit = generate_random_acc02_circuit(n, s)
            labels = dfs_labeling(circuit)
            p = next(p for p in range(s + 2, 2 * s + 3) if all(p % d != 0 for d in range(2, int(math.sqrt(p)) + 1)))
            chi_values = []
            for gate_idx, gate in enumerate(circuit):
                chi_g = compute_spectrum_dimension(gate, labels, p)
                chi_values.append(chi_g)
            chi_C = max(chi_values) / math.log2(p + 1) if chi_values else 0
            max_chi = max(max_chi, chi_C)
            instances_tested += 1
            if chi_C > 8 * math.log2(s + 1):
                counterexample = f"Random circuit with n={n}, s={s} has chi(C)={chi_C} > 8*log2(s+1)={8*math.log2(s+1)}"
                break
        if counterexample:
            break

    return {
        "metric_name": "max_chi_over_log2p",
        "metric_value": max_chi,
        "instances_tested": instances_tested,
        "conjecture_holds": not counterexample,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    metric_values = []
    conjecture_holds_all = True
    counterexample = ""

    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        metric_values.append(trial_result["metric_value"])
        if not trial_result["conjecture_holds"]:
            conjecture_holds_all = False
            counterexample = trial_result["counterexample"]
            break

    mean_metric = sum(metric_values) / len(metric_values)
    std_metric = math.sqrt(sum((x - mean_metric) ** 2 for x in metric_values) / len(metric_values))
    support_fraction = sum(1 for x in metric_values if x <= 8) / len(metric_values)

    if not conjecture_holds_all:
        print(f'RESULT: FALSIFIED counterexample="{counterexample}" first_failing_seed={seed}')
    elif support_fraction >= 0.8:
        print(f'RESULT: SUPPORTED mean={mean_metric} std={std_metric} support_fraction={support_fraction}')
    else:
        print('RESULT: INCONCLUSIVE reason=insufficient_support')