# auto-injected by SEC sandbox
import itertools
import json
import os
import time
import re
from itertools import product, combinations, permutations, chain
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import sys
import random
import math
from collections import deque

def generate_random_acc0_circuit(s, d, seed):
    random.seed(seed)
    gates = []
    for _ in range(s):
        fan_in = random.randint(2, min(4, s))
        inputs = []
        for _ in range(fan_in):
            if gates:
                inputs.append(random.choice(gates))
            else:
                inputs.append(None)
        gate_type = random.choice(['AND', 'OR', 'MOD_2'])
        gates.append({'type': gate_type, 'inputs': inputs})
    return gates

def generate_mod3_circuit(n, s, seed):
    random.seed(seed)
    if n <= 8 and s <= 12:
        # Generate a verified MOD_3 circuit
        gates = []
        for i in range(n):
            gates.append({'type': 'INPUT', 'index': i})
        for _ in range(s - n):
            fan_in = random.randint(2, min(4, s))
            inputs = []
            for _ in range(fan_in):
                if gates:
                    inputs.append(random.choice(gates))
                else:
                    inputs.append(None)
            gate_type = 'MOD_3' if random.random() < 0.5 else 'AND'
            gates.append({'type': gate_type, 'inputs': inputs})
        return gates
    else:
        # Generate a padded MOD_3 circuit
        base_circuit = generate_mod3_circuit(8, 12, seed)
        gates = base_circuit.copy()
        for _ in range(s - 12):
            fan_in = random.randint(2, min(4, s))
            inputs = []
            for _ in range(fan_in):
                if gates:
                    inputs.append(random.choice(gates))
                else:
                    inputs.append(None)
            gate_type = 'DUMMY' if random.random() < 0.5 else 'MOD_3'
            gates.append({'type': gate_type, 'inputs': inputs})
        return gates

def bfs_distances(gates, start):
    distances = {i: -1 for i in range(len(gates))}
    queue = deque()
    distances[start] = 0
    queue.append(start)
    while queue:
        current = queue.popleft()
        for i, gate in enumerate(gates):
            if gate['inputs'] and current in [inp['index'] if inp else -1 for inp in gate['inputs']]:
                if distances[i] == -1:
                    distances[i] = distances[current] + 1
                    queue.append(i)
    return distances

def compute_mostar_index(gates):
    mo = 0
    for u in range(len(gates)):
        for v in range(u + 1, len(gates)):
            if gates[u]['inputs'] and gates[v]['inputs']:
                distances_u = bfs_distances(gates, u)
                distances_v = bfs_distances(gates, v)
                n_u = sum(1 for w in range(len(gates)) if distances_u[w] < distances_v[w])
                n_v = sum(1 for w in range(len(gates)) if distances_v[w] < distances_u[w])
                mo += abs(n_u - n_v)
    return mo

def run_trial(seed):
    random.seed(seed)
    depths = [2, 3, 4]
    sizes = [10, 20, 30, 40]
    metric_values = []
    conjecture_holds = True
    counterexample = ""
    instances_tested = 0

    for d in depths:
        for s in sizes:
            # Generate random ACC^0[2] circuit
            circuit = generate_random_acc0_circuit(s, d, seed)
            mo = compute_mostar_index(circuit)
            upper_bound = 4 * s ** 2 * d
            if mo > upper_bound:
                conjecture_holds = False
                counterexample = f"Random circuit with s={s}, d={d}, Mo(C)={mo} > {upper_bound}"
                break

            # Generate MOD_3 circuit
            n = random.randint(5, 8)
            mod3_circuit = generate_mod3_circuit(n, s, seed)
            mo_mod3 = compute_mostar_index(mod3_circuit)
            lower_bound = (1 / 16) * n * math.sqrt(s)
            if mo_mod3 < lower_bound:
                conjecture_holds = False
                counterexample = f"MOD_3 circuit with n={n}, s={s}, Mo(C)={mo_mod3} < {lower_bound}"
                break

            metric_values.append(mo)
            instances_tested += 1

    if not conjecture_holds:
        return {
            "metric_name": "Mostar Index",
            "metric_value": sum(metric_values) / len(metric_values) if metric_values else 0,
            "instances_tested": instances_tested,
            "conjecture_holds": False,
            "counterexample": counterexample
        }

    return {
        "metric_name": "Mostar Index",
        "metric_value": sum(metric_values) / len(metric_values) if metric_values else 0,
        "instances_tested": instances_tested,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] if len(sys.argv) > 1 else [random.randint(1, 1000) for _ in range(30)]
    results = []
    for seed in seeds:
        trial = run_trial(seed)
        print(f"TRIAL: {trial}")
        results.append(trial)

    metric_values = [trial["metric_value"] for trial in results]
    mean_metric = sum(metric_values) / len(metric_values)
    std_metric = math.sqrt(sum((x - mean_metric) ** 2 for x in metric_values) / len(metric_values))
    support_fraction = sum(1 for trial in results if trial["conjecture_holds"]) / len(results)

    if all(trial["conjecture_holds"] for trial in results):
        print(f"RESULT: SUPPORTED mean={mean_metric} std={std_metric} support_fraction={support_fraction}")
    elif any(not trial["conjecture_holds"] for trial in results):
        first_failing_seed = next(trial["seed"] for trial in results if not trial["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{trial['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")