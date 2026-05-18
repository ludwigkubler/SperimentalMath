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

def generate_acc0_circuit(seed, s, d, n_inputs):
    random.seed(seed)
    gates = []
    for i in range(s):
        gate_type = random.choice(['AND', 'OR', 'MOD_2'])
        fan_in = random.randint(2, min(4, math.ceil(math.log2(s))))
        inputs = []
        for _ in range(fan_in):
            if len(gates) > 0:
                input_gate = random.choice(gates)
                inputs.append({'index': input_gate['index'], 'type': input_gate['type']})
            else:
                input_gate = random.randint(0, n_inputs - 1)
                inputs.append({'index': input_gate, 'type': 'input'})
        gates.append({'index': i, 'type': gate_type, 'inputs': inputs})
    return gates

def bfs_distances(gates, start):
    distances = {gate['index']: -1 for gate in gates}
    queue = deque()
    distances[start] = 0
    queue.append(start)
    while queue:
        current = queue.popleft()
        for gate in gates:
            if gate['inputs'] and current in [inp['index'] if inp else -1 for inp in gate['inputs']]:
                if distances[gate['index']] == -1:
                    distances[gate['index']] = distances[current] + 1
                    queue.append(gate['index'])
    return distances

def compute_mostar_index(circuit):
    mo = 0
    for u in circuit:
        distances_u = bfs_distances(circuit, u['index'])
        for v in circuit:
            if u['index'] != v['index']:
                n_u = 0
                n_v = 0
                for w in circuit:
                    if distances_u[w['index']] < bfs_distances(circuit, v['index'])[w['index']]:
                        n_u += 1
                    if bfs_distances(circuit, v['index'])[w['index']] < distances_u[w['index']]:
                        n_v += 1
                mo += abs(n_u - n_v)
    return mo

def run_trial(seed):
    random.seed(seed)
    depths = [2, 3, 4]
    sizes = [10, 20, 30, 40]
    n_inputs = 5
    instances_tested = 0
    metric_values = []
    conjecture_holds = True
    counterexample = ""

    for d in depths:
        for s in sizes:
            circuit = generate_acc0_circuit(seed, s, d, n_inputs)
            mo = compute_mostar_index(circuit)
            bound = 4 * s * s * d
            if mo > bound:
                conjecture_holds = False
                counterexample = f"Random ACC^0[2] circuit with s={s}, d={d} violated bound: Mo(C)={mo} > {bound}"
                break
            metric_values.append(mo)
            instances_tested += 1
            if not conjecture_holds:
                break
        if not conjecture_holds:
            break

    if conjecture_holds:
        for s in [10, 12]:
            for n in range(5, 9):
                circuit = generate_acc0_circuit(seed, s, 2, n)
                mo = compute_mostar_index(circuit)
                bound = (1/16) * n * math.sqrt(s)
                if mo < bound:
                    conjecture_holds = False
                    counterexample = f"MOD_3 ACC^0[2] circuit with s={s}, n={n} violated bound: Mo(C)={mo} < {bound}"
                    break
                metric_values.append(mo)
                instances_tested += 1
                if not conjecture_holds:
                    break
            if not conjecture_holds:
                break

    return {
        "metric_name": "Mostar Index",
        "metric_value": sum(metric_values) / len(metric_values) if metric_values else 0,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] if len(sys.argv) > 1 else [random.randint(1, 1000000) for _ in range(30)]
    trials = []
    for seed in seeds:
        trial = run_trial(seed)
        trials.append(trial)
        print(f"TRIAL: {trial}")

    metric_values = [trial["metric_value"] for trial in trials]
    mean_metric = sum(metric_values) / len(metric_values)
    std_metric = math.sqrt(sum((x - mean_metric) ** 2 for x in metric_values) / len(metric_values))
    support_fraction = sum(1 for trial in trials if trial["conjecture_holds"]) / len(trials)

    if all(trial["conjecture_holds"] for trial in trials):
        print(f"RESULT: SUPPORTED mean={mean_metric} std={std_metric} support_fraction={support_fraction}")
    elif any(not trial["conjecture_holds"] for trial in trials):
        first_failing_seed = next(trial["seed"] for trial in trials if not trial["conjecture_holds"])
        counterexample = next(trial["counterexample"] for trial in trials if not trial["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")