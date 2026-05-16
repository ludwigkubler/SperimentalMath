# auto-injected by SEC sandbox
import itertools
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
import json
from collections import defaultdict

def generate_dnf_parity(n):
    circuit = []
    for i in range(2 ** (n - 1)):
        gate = [0] * n
        for j in range(n):
            if (i >> (n - 1 - j)) & 1:
                gate[j] = 1
        circuit.append(gate)
    return circuit

def generate_hastad_parity(n):
    if n == 1:
        return [[1]]
    m = int(math.sqrt(n))
    circuit = []
    for i in range(m):
        sub_circuit = generate_hastad_parity(m)
        for gate in sub_circuit:
            new_gate = [0] * n
            for j in range(len(gate)):
                if gate[j]:
                    new_gate[i * m + j] = 1
            circuit.append(new_gate)
    return circuit

def generate_random_dnf(n, size):
    circuit = []
    for _ in range(size):
        gate = [random.randint(0, 1) for _ in range(n)]
        circuit.append(gate)
    return circuit

def compute_ch(circuit, n):
    chamber_count = defaultdict(int)
    for x in range(2 ** n):
        output_vector = []
        for gate in circuit:
            if all(gate[i] == ((x >> (n - 1 - i)) & 1) for i in range(n)):
                output_vector.append(1)
            else:
                output_vector.append(0)
        chamber_count[tuple(output_vector)] += 1
    return len(chamber_count)

def run_trial(seed):
    random.seed(seed)
    n_values = [6, 8, 10, 12, 14, 16]
    results = []
    for n in n_values:
        # Generate PARITY circuits
        dnf_circuit = generate_dnf_parity(n)
        hastad_circuit = generate_hastad_parity(n)

        # Generate negative control
        size = len(dnf_circuit)
        random_circuit = generate_random_dnf(n, size)

        # Compute chamber counts
        dnf_ch = compute_ch(dnf_circuit, n)
        hastad_ch = compute_ch(hastad_circuit, n)
        random_ch = compute_ch(random_circuit, n)

        # Compute metric values
        dnf_metric = math.log2(dnf_ch) / (n ** (1 / 1))  # d=2
        hastad_metric = math.log2(hastad_ch) / (n ** (1 / 2))  # d=3
        random_metric = math.log2(random_ch) / (n ** (1 / 1))  # d=2

        # Check conjecture
        dnf_holds = dnf_metric >= 0.25
        hastad_holds = hastad_metric >= 0.25
        random_holds = random_metric < dnf_metric

        # Prepare results
        results.append({
            "n": n,
            "dnf_metric": dnf_metric,
            "hastad_metric": hastad_metric,
            "random_metric": random_metric,
            "dnf_holds": dnf_holds,
            "hastad_holds": hastad_holds,
            "random_holds": random_holds,
            "counterexample": "" if dnf_holds and hastad_holds else f"n={n}, d=2, size={len(dnf_circuit)}, ch={dnf_ch}, seed={seed}"
        })

    # Aggregate results
    dnf_metrics = [r["dnf_metric"] for r in results]
    hastad_metrics = [r["hastad_metric"] for r in results]
    random_metrics = [r["random_metric"] for r in results]

    dnf_holds = all(r["dnf_holds"] for r in results)
    hastad_holds = all(r["hastad_holds"] for r in results)
    random_holds = all(r["random_holds"] for r in results)

    counterexamples = [r["counterexample"] for r in results if r["counterexample"]]

    return {
        "metric_name": "log2(ch(C)) / n^{1/(d-1)}",
        "metric_value": sum(dnf_metrics + hastad_metrics) / (2 * len(n_values)),
        "instances_tested": len(n_values),
        "conjecture_holds": dnf_holds and hastad_holds and random_holds,
        "counterexample": counterexamples[0] if counterexamples else ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    trials = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {json.dumps({'seed': seed, **result})}")
        trials.append(result)

    # Compute statistics
    metric_values = [t["metric_value"] for t in trials]
    mean_metric = sum(metric_values) / len(metric_values)
    std_metric = math.sqrt(sum((x - mean_metric) ** 2 for x in metric_values) / len(metric_values))
    support_fraction = sum(1 for t in trials if t["conjecture_holds"]) / len(trials)

    # Determine result
    if all(t["conjecture_holds"] for t in trials):
        print(f"RESULT: SUPPORTED mean={mean_metric:.4f} std={std_metric:.4f} support_fraction={support_fraction:.4f}")
    elif any(t["counterexample"] for t in trials):
        first_failing_seed = next(t["seed"] for t in trials if t["counterexample"])
        print(f"RESULT: FALSIFIED counterexample=\"{trials[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_support")