# auto-injected by SEC sandbox
import itertools
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from itertools import product, combinations, permutations, chain
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math

def generate_circuit(n, m):
    # Generate a random boolean circuit with n inputs and m outputs
    if n == 1:
        return [[0] * m]
    else:
        circuits = []
        for i in range(2 ** (n - 1)):
            subcircuits = [generate_circuit(n - 1, m) for _ in range(2)]
            circuit = []
            for j in range(m):
                gate = random.choice([0, 1])
                if gate == 0:
                    circuit.append(subcircuits[0][i] + subcircuits[1][i])
                else:
                    circuit.append(subcircuits[1][i] + subcircuits[0][i])
            circuits.append(circuit)
        return circuits

def compute_braid_relations(circuit):
    # Compute the minimal number of braid relations required to represent the circuit
    n = len(circuit[0])
    m = len(circuit)
    if n == 1:
        return 0
    else:
        relations = 0
        for i in range(m):
            for j in range(n - 1):
                if circuit[i][j] != circuit[i][j + 1]:
                    relations += 1
        return relations

def run_trial(seed: int) -> dict:
    random.seed(seed)
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        for m in [5, 10, 15, 20, 30, 40]:
            circuit = generate_circuit(n, m)
            relations = compute_braid_relations(circuit)
            results.append((n, m, relations))
    if len(results) < 30:
        return {
            "metric_name": "braid_relations_per_lognm",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max(n for n, m, _ in results),
            "conjecture_holds": False,
            "counterexample": "insufficient_instances"
        }
    log_nm = [math.log(n) * math.log(m) for n, m, _ in results]
    ratio = [r / lnm for r, lnm in zip(results, log_nm)]
    mean_ratio = sum(ratio) / len(ratio)
    std_ratio = (sum((x - mean_ratio) ** 2 for x in ratio) / len(ratio)) ** 0.5
    support_fraction = sum(1 for r in ratio if abs(r - 1) <= 0.1) / len(ratio)
    return {
        "metric_name": "braid_relations_per_lognm",
        "metric_value": mean_ratio,
        "instances_tested": len(results),
        "n_max": max(n for n, m, _ in results),
        "conjecture_holds": support_fraction >= 0.9,
        "counterexample": "" if support_fraction >= 0.9 else "support_fraction < 0.9"
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{trial_result['metric_name']}\", \"metric_value\": {trial_result['metric_value']}, \"instances_tested\": {trial_result['instances_tested']}, \"n_max\": {trial_result['n_max']}, \"conjecture_holds\": {trial_result['conjecture_holds']}, \"counterexample\": \"{trial_result['counterexample']}\"}}")
        results.append(trial_result)
    mean_metric_value = sum(r['metric_value'] for r in results if r['metric_value'] is not None) / len(results)
    std_metric_value = (sum((r['metric_value'] - mean_metric_value) ** 2 for r in results if r['metric_value'] is not None) / len(results)) ** 0.5
    support_fraction = sum(1 for r in results if r['conjecture_holds']) / len(results)
    if all(r['conjecture_holds'] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result['conjecture_holds'])
        print(f"RESULT: FALSIFIED counterexample=\"support_fraction < 0.8\" first_failing_seed={first_failing_seed}")