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

def matrix_mult(a, b):
    return [[sum(a[i][k] * b[k][j] for k in range(len(b))) for j in range(len(b[0]))] for i in range(len(a))]

def matrix_pow(mat, power):
    result = [[1 if i == j else 0 for j in range(len(mat))] for i in range(len(mat))]
    while power > 0:
        if power % 2 == 1:
            result = matrix_mult(result, mat)
        mat = matrix_mult(mat, mat)
        power //= 2
    return result

def bfs(graph, start):
    distances = {node: -1 for node in graph}
    distances[start] = 0
    queue = deque([start])
    while queue:
        current = queue.popleft()
        for neighbor in graph[current]:
            if distances[neighbor] == -1:
                distances[neighbor] = distances[current] + 1
                queue.append(neighbor)
    return distances

def generate_acc0_circuit(seed, s, d, n=0, is_mod3=False):
    random.seed(seed)
    gates = []
    adj = {i: set() for i in range(s)}
    gate_types = ['AND', 'OR', 'MOD_2'] if not is_mod3 else ['AND', 'OR', 'MOD_2', 'MOD_3']

    for i in range(s):
        gate_type = random.choice(gate_types)
        fan_in = random.randint(2, min(3, math.ceil(math.log2(s))))
        inputs = []
        for _ in range(fan_in):
            if i == 0:
                inputs.append(random.randint(0, n-1))
            else:
                inputs.append(random.randint(0, i-1))
        gates.append((gate_type, inputs))
        for inp in inputs:
            adj[i].add(inp)
            adj[inp].add(i)

    return gates, adj

def compute_mostar_index(gates, adj):
    s = len(gates)
    mo = 0
    for u in range(s):
        distances_u = bfs(adj, u)
        for v in adj[u]:
            if v > u:
                distances_v = bfs(adj, v)
                n_u = sum(1 for w in range(s) if distances_u[w] < distances_v[w])
                n_v = sum(1 for w in range(s) if distances_v[w] < distances_u[w])
                mo += abs(n_u - n_v)
    return mo

def run_trial(seed):
    random.seed(seed)
    trials = []
    sizes = [10, 20, 30, 40]
    depths = [2, 3, 4]

    for s in sizes:
        for d in depths:
            gates, adj = generate_acc0_circuit(seed, s, d)
            mo = compute_mostar_index(gates, adj)
            bound = 4 * s * s * d
            conjecture_holds = mo <= bound
            counterexample = f"Random ACC^0[2] circuit with s={s}, d={d} violated bound: Mo(C)={mo} > {bound}" if not conjecture_holds else ""

            trials.append({
                "seed": seed,
                "metric_name": "Mostar Index",
                "metric_value": mo,
                "instances_tested": 1,
                "conjecture_holds": conjecture_holds,
                "counterexample": counterexample,
                "s": s,
                "d": d
            })

    # Add MOD_3 circuits
    mod3_circuits = []
    for s in [10, 20, 30, 40]:
        for n in [5, 6, 7, 8]:
            gates, adj = generate_acc0_circuit(seed, s, 2, n, is_mod3=True)
            mo = compute_mostar_index(gates, adj)
            bound = (1/16) * n * math.sqrt(s)
            conjecture_holds = mo >= bound
            counterexample = f"MOD_3 ACC^0[2] circuit with s={s}, n={n} violated bound: Mo(C)={mo} < {bound}" if not conjecture_holds else ""

            mod3_circuits.append({
                "seed": seed,
                "metric_name": "Mostar Index",
                "metric_value": mo,
                "instances_tested": 1,
                "conjecture_holds": conjecture_holds,
                "counterexample": counterexample,
                "s": s,
                "n": n
            })

    # Combine trials
    all_trials = trials + mod3_circuits

    # Calculate statistics
    metric_values = [trial["metric_value"] for trial in all_trials]
    mean = sum(metric_values) / len(metric_values)
    std = math.sqrt(sum((x - mean) ** 2 for x in metric_values) / len(metric_values))
    support_fraction = sum(1 for trial in all_trials if trial["conjecture_holds"]) / len(all_trials)

    # Check for counterexamples
    counterexamples = [trial for trial in all_trials if not trial["conjecture_holds"]]
    if counterexamples:
        first_failing_seed = counterexamples[0]["seed"]
        return {
            "metric_name": "Mostar Index",
            "metric_value": mean,
            "instances_tested": len(all_trials),
            "conjecture_holds": False,
            "counterexample": counterexamples[0]["counterexample"],
            "first_failing_seed": first_failing_seed
        }

    return {
        "metric_name": "Mostar Index",
        "metric_value": mean,
        "instances_tested": len(all_trials),
        "conjecture_holds": True,
        "counterexample": "",
        "mean": mean,
        "std": std,
        "support_fraction": support_fraction
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    trials = []

    for seed in seeds:
        trial = run_trial(seed)
        print(f"TRIAL: {trial}")
        trials.append(trial)

    # Calculate overall statistics
    metric_values = [trial["metric_value"] for trial in trials]
    mean = sum(metric_values) / len(metric_values)
    std = math.sqrt(sum((x - mean) ** 2 for x in metric_values) / len(metric_values))
    support_fraction = sum(1 for trial in trials if trial["conjecture_holds"]) / len(trials)

    # Check for counterexamples
    counterexamples = [trial for trial in trials if not trial["conjecture_holds"]]
    if counterexamples:
        first_failing_seed = counterexamples[0]["seed"]
        print(f'RESULT: FALSIFIED counterexample="{counterexamples[0]["counterexample"]}" first_failing_seed={first_failing_seed}')
    elif support_fraction >= 0.8:
        print(f'RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}')
    else:
        print('RESULT: INCONCLUSIVE reason=insufficient_support')