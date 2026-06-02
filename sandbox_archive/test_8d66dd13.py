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

def generate_random_boolean_circuit(n):
    circuit = []
    for _ in range(2**(n-1)):
        gate = random.choice(['AND', 'OR'])
        inputs = [random.randint(0, 1) for _ in range(n)]
        circuit.append((gate, inputs))
    return circuit

def compute_minimal_local_coherence(circuit):
    mlc = 0
    for gate, inputs in circuit:
        if gate == 'AND':
            mlc += sum(inputs)
        elif gate == 'OR':
            mlc += max(inputs)
    return mlc / len(circuit)

def compute_depth(circuit):
    depth = 0
    for gate, _ in circuit:
        if gate == 'AND' or gate == 'OR':
            depth += 1
    return depth

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    mlc_sum = 0
    d_sum = 0
    instances_tested = 0
    n_max = 0

    for n in n_values:
        circuit = generate_random_boolean_circuit(n)
        mlc = compute_minimal_local_coherence(circuit)
        d = compute_depth(circuit)
        mlc_sum += mlc
        d_sum += d
        instances_tested += len(circuit)
        if n > n_max:
            n_max = n

    mean_mlc = mlc_sum / instances_tested
    mean_d = d_sum / instances_tested
    correlation_coefficient = (instances_tested * sum(mlc * d for mlc, d in zip([compute_minimal_local_coherence(generate_random_boolean_circuit(n)) for n in n_values], [compute_depth(generate_random_boolean_circuit(n)) for n in n_values])) - mean_mlc * mean_d) / math.sqrt((instances_tested * sum(mlc**2 for mlc in [compute_minimal_local_coherence(generate_random_boolean_circuit(n)) for n in n_values]) - mean_mlc**2) * (instances_tested * sum(d**2 for d in [compute_depth(generate_random_boolean_circuit(n)) for n in n_values]) - mean_d**2))

    conjecture_holds = 0.8 <= correlation_coefficient <= 1.2
    counterexample = "" if conjecture_holds else f"Correlation coefficient outside range: {correlation_coefficient}"

    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 7 for i in range(5, 30)]
    results = []

    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...{result}...}}")
        results.append(result)

    mean_mlc = sum(r["metric_value"] for r in results) / len(results)
    std_mlc = math.sqrt(sum((r["metric_value"] - mean_mlc)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if 0.8 <= r["metric_value"] <= 1.2) / len(results)

    if all(0.8 <= r["metric_value"] <= 1.2 for r in results):
        print(f"RESULT: SUPPORTED mean={mean_mlc} std={std_mlc} support_fraction={support_fraction}")
    elif any(not (0.8 <= r["metric_value"] <= 1.2) for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not (0.8 <= result["metric_value"] <= 1.2))
        print(f"RESULT: FALSIFIED counterexample=\"Correlation coefficient outside range\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unsupported_operation")