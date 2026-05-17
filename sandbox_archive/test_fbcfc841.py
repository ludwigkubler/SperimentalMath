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
    for _ in range(s):
        if len(gates) < 2:
            gate_type = random.choice(['AND', 'OR', 'MOD_2'])
        else:
            gate_type = random.choice(['AND', 'OR', 'MOD_2', 'INPUT'])
        if gate_type == 'INPUT':
            inputs = []
        else:
            num_inputs = random.randint(2, min(3, len(gates)))
            inputs = random.sample(gates, num_inputs)
        gates.append((gate_type, inputs))
    return gates

def build_poset(circuit):
    poset = defaultdict(list)
    poset[0] = []
    for i, (gate_type, inputs) in enumerate(circuit):
        poset[i+1] = [0] + [j+1 for j, _ in enumerate(circuit) if any(j+1 in inp for inp in inputs)]
    return poset

def compute_mobius(poset, output_gate):
    mobius = {0: 1}
    for i in range(1, output_gate+1):
        if i not in poset:
            continue
        mobius[i] = -sum(mobius.get(j, 0) for j in poset[i] if j != i)
    return mobius

def is_mod3_circuit(circuit, n):
    for inputs in itertools.product([0, 1], repeat=n):
        output = evaluate_circuit(circuit, inputs)
        expected = sum(inputs) % 3
        if output != expected:
            return False
    return True

def evaluate_circuit(circuit, inputs):
    values = list(inputs)
    for gate_type, gate_inputs in circuit:
        if gate_type == 'AND':
            values.append(int(all(values[i] for i in gate_inputs)))
        elif gate_type == 'OR':
            values.append(int(any(values[i] for i in gate_inputs)))
        elif gate_type == 'MOD_2':
            values.append(sum(values[i] for i in gate_inputs) % 2)
        else:
            values.append(0)
    return values[-1]

def run_trial(seed):
    n_values = [6, 8, 10, 12, 14, 16]
    d_values = [2, 3]
    s_values = [10, 20, 30, 40]
    metric_values = []
    conjecture_holds = True
    counterexample = ""
    instances_tested = 0

    for n, d, s in itertools.product(n_values, d_values, s_values):
        circuit = generate_random_circuit(n, s, d, seed)
        poset = build_poset(circuit)
        output_gate = len(circuit)
        mobius = compute_mobius(poset, output_gate)
        m_c = abs(mobius.get(output_gate, 0))

        if m_c > (s + 1) ** d:
            conjecture_holds = False
            counterexample = f"M(C) = {m_c} > (s+1)^d = {(s+1)**d} for n={n}, d={d}, s={s}"
            break

        if is_mod3_circuit(circuit, n):
            threshold = 2 ** (n ** (1 / (d + 1)) / 8)
            if m_c < threshold:
                conjecture_holds = False
                counterexample = f"M(C) = {m_c} < threshold = {threshold} for MOD_3 circuit with n={n}, d={d}, s={s}"
                break

        metric_values.append(m_c)
        instances_tested += 1

    if not metric_values:
        return {
            "metric_name": "M(C)",
            "metric_value": 0.0,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "No valid instances generated"
        }

    return {
        "metric_name": "M(C)",
        "metric_value": sum(metric_values) / len(metric_values),
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    metric_values = []
    conjecture_holds_counts = 0

    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
        metric_values.append(result["metric_value"])
        if result["conjecture_holds"]:
            conjecture_holds_counts += 1

    if not metric_values:
        print("RESULT: INCONCLUSIVE reason=no_metric_values")
        sys.exit(0)

    mean_metric = sum(metric_values) / len(metric_values)
    std_metric = math.sqrt(sum((x - mean_metric) ** 2 for x in metric_values) / len(metric_values))
    support_fraction = conjecture_holds_counts / len(seeds)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric} std={std_metric} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")