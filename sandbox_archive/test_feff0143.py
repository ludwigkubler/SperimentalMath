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
        if d == 2:
            fan_in = random.randint(2, min(4, n))
        else:
            fan_in = random.randint(2, min(3, n))
        inputs = random.sample(range(n), fan_in)
        op = random.choice(['AND', 'OR', 'MOD_2'])
        gates.append((op, inputs))
    output_gate = random.choice(range(s))
    return gates, output_gate

def build_poset(gates, output_gate, n):
    poset = defaultdict(set)
    poset[0] = set(range(n))
    for i, (op, inputs) in enumerate(gates):
        poset[i] = set(inputs)
    poset[output_gate].add(0)
    return poset

def compute_mobius(poset, output_gate):
    mobius = {0: 1}
    for h in range(1, len(poset)):
        mobius[h] = -sum(mobius[z] for z in poset[h] if z in mobius)
    return abs(mobius[output_gate])

def is_mod3_circuit(gates, output_gate, n):
    for inputs in itertools.product([0, 1], repeat=n):
        result = evaluate_circuit(gates, output_gate, inputs)
        expected = sum(inputs) % 3
        if result != expected:
            return False
    return True

def evaluate_circuit(gates, output_gate, inputs):
    values = list(inputs)
    for i, (op, gate_inputs) in enumerate(gates):
        if op == 'AND':
            values[i] = all(values[g] for g in gate_inputs)
        elif op == 'OR':
            values[i] = any(values[g] for g in gate_inputs)
        elif op == 'MOD_2':
            values[i] = sum(values[g] for g in gate_inputs) % 2
    return values[output_gate]

def run_trial(seed):
    random.seed(seed)
    n_values = [6, 8, 10, 12, 14, 16]
    d_values = [2, 3]
    s_values = [10, 20, 30, 40]
    metric_values = []
    instances_tested = 0
    conjecture_a_holds = True
    conjecture_b_holds = True
    counterexample = ""

    for n in n_values:
        for d in d_values:
            for s in s_values:
                gates, output_gate = generate_random_circuit(n, s, d, seed)
                poset = build_poset(gates, output_gate, n)
                m = compute_mobius(poset, output_gate)
                metric_values.append(m)
                instances_tested += 1

                if m > (s + 1) ** d:
                    conjecture_a_holds = False
                    counterexample = f"Conjecture A violated: M(C) = {m} > (s+1)^d = {(s+1)**d} for n={n}, d={d}, s={s}"

                if is_mod3_circuit(gates, output_gate, n):
                    threshold = 2 ** (n ** (1 / (d + 1)) / 8)
                    if m < threshold:
                        conjecture_b_holds = False
                        counterexample = f"Conjecture B violated: M(C) = {m} < threshold = {threshold} for MOD_3 circuit with n={n}, d={d}, s={s}"

    metric_value = sum(metric_values) / len(metric_values) if metric_values else 0
    conjecture_holds = conjecture_a_holds and conjecture_b_holds

    return {
        "metric_name": "M(C)",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
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
    mean_metric = sum(metric_values) / len(metric_values) if metric_values else 0
    std_metric = math.sqrt(sum((x - mean_metric) ** 2 for x in metric_values) / len(metric_values)) if metric_values else 0
    support_fraction = sum(r["conjecture_holds"] for r in results) / len(results) if results else 0

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric} std={std_metric} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        counterexample = next(r["counterexample"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")