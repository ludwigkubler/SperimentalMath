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

def generate_random_circuit(n, s, d, seed):
    random.seed(seed)
    gates = []
    for i in range(s):
        if i < n:
            gates.append({'type': 'input', 'inputs': []})
        else:
            gate_type = random.choice(['AND', 'OR', 'MOD_2'])
            fan_in = random.randint(1, min(3, i))
            inputs = random.sample(range(i), fan_in)
            gates.append({'type': gate_type, 'inputs': inputs})
    output_gate = random.randint(n, s-1)
    return gates, output_gate

def build_poset(gates, output_gate):
    poset = defaultdict(set)
    poset[output_gate] = set()
    for i in range(len(gates)-1, -1, -1):
        for j in range(i+1, len(gates)):
            if i in gates[j]['inputs']:
                poset[i].add(j)
    return poset

def compute_mobius(poset, output_gate):
    mobius = {}
    mobius[output_gate] = 1
    for i in sorted(poset.keys(), reverse=True):
        if i == output_gate:
            continue
        mobius[i] = -sum(mobius[j] for j in poset[i])
    return mobius

def evaluate_circuit(gates, output_gate, inputs):
    values = [0] * len(gates)
    for i in range(len(gates)):
        if gates[i]['type'] == 'input':
            values[i] = inputs[i]
        else:
            gate_inputs = gates[i]['inputs']
            if gates[i]['type'] == 'AND':
                values[i] = all(values[g] for g in gate_inputs)
            elif gates[i]['type'] == 'OR':
                values[i] = any(values[g] for g in gate_inputs)
            elif gates[i]['type'] == 'MOD_2':
                values[i] = sum(values[g] for g in gate_inputs) % 2
    return values[output_gate]

def is_mod3_circuit(gates, output_gate, n):
    for inputs in itertools.product([0, 1], repeat=n):
        result = evaluate_circuit(gates, output_gate, inputs)
        expected = sum(inputs) % 3
        if result != expected:
            return False
    return True

def run_trial(seed):
    n_values = [6, 8, 10, 12, 14, 16]
    d_values = [2, 3]
    s_values = [10, 20, 30, 40]
    instances_tested = 0
    metric_values = []
    conjecture_a_holds = True
    conjecture_b_holds = True
    counterexample = ""

    for n in n_values:
        for d in d_values:
            for s in s_values:
                gates, output_gate = generate_random_circuit(n, s, d, seed)
                poset = build_poset(gates, output_gate)
                mobius = compute_mobius(poset, output_gate)
                M_C = abs(mobius[output_gate])
                metric_values.append(M_C)
                instances_tested += 1

                if M_C > (s + 1) ** d:
                    conjecture_a_holds = False
                    counterexample = f"M(C) = {M_C} > (s+1)^d = {(s+1)**d} for n={n}, d={d}, s={s}"

                if is_mod3_circuit(gates, output_gate, n):
                    threshold = 2 ** (n ** (1 / (d + 1)) / 8)
                    if M_C < threshold:
                        conjecture_b_holds = False
                        counterexample = f"M(C) = {M_C} < threshold = {threshold} for MOD_3 circuit with n={n}, d={d}, s={s}"

    metric_value = sum(metric_values) / len(metric_values) if metric_values else 0
    return {
        "metric_name": "M(C)",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_a_holds": conjecture_a_holds,
        "conjecture_b_holds": conjecture_b_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] if len(sys.argv) > 1 else [random.randint(1, 1000) for _ in range(30)]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    metric_values = [r["metric_value"] for r in results]
    mean_metric = sum(metric_values) / len(metric_values) if metric_values else 0
    std_metric = math.sqrt(sum((x - mean_metric) ** 2 for x in metric_values) / len(metric_values)) if metric_values else 0

    a_support = sum(r["conjecture_a_holds"] for r in results) / len(results)
    b_support = sum(r["conjecture_b_holds"] for r in results) / len(results)

    if all(r["conjecture_a_holds"] for r in results) and b_support >= 0.9:
        print(f"RESULT: SUPPORTED mean={mean_metric} std={std_metric} support_fraction={a_support}")
    elif any(not r["conjecture_a_holds"] for r in results):
        first_failing_seed = seeds[next(i for i, r in enumerate(results) if not r["conjecture_a_holds"])]
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_support")