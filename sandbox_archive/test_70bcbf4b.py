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

def generate_random_circuit(n, s, d, seed):
    random.seed(seed)
    gates = []
    for _ in range(s):
        if d == 2:
            fan_in = random.randint(1, min(3, n))
            inputs = random.sample(range(n), fan_in)
            op = random.choice(['AND', 'OR', 'MOD_2'])
            gates.append((op, inputs))
        else:
            fan_in = random.randint(1, min(4, n))
            inputs = random.sample(range(n), fan_in)
            op = random.choice(['AND', 'OR', 'MOD_2'])
            gates.append((op, inputs))
    return gates

def build_poset(gates, n):
    poset = defaultdict(set)
    poset[0] = set(range(n))
    for i, gate in enumerate(gates):
        poset[0].add(i + n)
        for j in gate[1]:
            poset[j].add(i + n)
    return poset

def compute_mobius(poset, s, n):
    mobius = {}
    mobius[0] = 1
    for i in range(n, n + s):
        mobius[i] = 0
    for i in range(n, n + s):
        for j in poset[i]:
            mobius[j] = mobius.get(j, 0) - mobius[i]
    return mobius

def evaluate_circuit(circuit, inputs):
    values = list(inputs)
    for gate in circuit:
        op, inputs = gate
        if op == 'AND':
            values.append(all(values[i] for i in inputs))
        elif op == 'OR':
            values.append(any(values[i] for i in inputs))
        elif op == 'MOD_2':
            values.append(sum(values[i] for i in inputs) % 2)
    return values[-1]

def is_mod3_circuit(circuit, n):
    for inputs in itertools.product([0, 1], repeat=n):
        output = evaluate_circuit(circuit, inputs)
        if output != (sum(inputs) % 3):
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
                circuit = generate_random_circuit(n, s, d, seed)
                poset = build_poset(circuit, n)
                mobius = compute_mobius(poset, s, n)
                M_C = abs(mobius.get(0, 0))
                metric_values.append(M_C)
                instances_tested += 1

                if M_C > (s + 1) ** d:
                    conjecture_a_holds = False
                    counterexample = f"M(C) = {M_C} > (s+1)^d = {(s+1)**d} for n={n}, d={d}, s={s}"

                if is_mod3_circuit(circuit, n):
                    threshold = 2 ** (n ** (1 / (d + 1)) / 8)
                    if M_C < threshold:
                        conjecture_b_holds = False
                        counterexample = f"M(C) = {M_C} < threshold = {threshold} for MOD_3 circuit with n={n}, d={d}, s={s}"

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
    mean_metric = sum(metric_values) / len(metric_values)
    std_metric = math.sqrt(sum((x - mean_metric) ** 2 for x in metric_values) / len(metric_values))
    support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric} std={std_metric} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        counterexample = next(r["counterexample"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")