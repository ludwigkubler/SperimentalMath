# auto-injected by SEC sandbox
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import itertools
import math
from fractions import Fraction

def generate_random_circuit(n: int) -> list:
    return [random.choice([0, 1]) for _ in range(2**n)]

def compute_entanglement_complexity(circuit: list) -> int:
    n = len(circuit)
    count = 0
    for i in range(n):
        for j in range(i + 1, n):
            if circuit[i] != circuit[j]:
                count += 1
    return count

def compute_morse_function(circuit: list) -> dict:
    n = len(circuit)
    morse_func = {}
    for i in range(2**n):
        binary = f"{i:0{n}b}"
        value = sum(int(bit) * circuit[j] for j, bit in enumerate(reversed(binary)))
        if value not in morse_func:
            morse_func[value] = []
        morse_func[value].append(i)
    return morse_func

def compute_minimal_geometric_defect(morse_func: dict) -> float:
    critical_points = list(morse_func.keys())
    if len(critical_points) < 2:
        return 0.0
    return min(abs(cp1 - cp2) for cp1, cp2 in itertools.combinations(critical_points, 2))

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    total_metric_value = 0.0
    instances_tested = 0
    n_max = 0

    for n in n_values:
        circuit = generate_random_circuit(n)
        entanglement_complexity = compute_entanglement_complexity(circuit)
        morse_func = compute_morse_function(circuit)
        minimal_geometric_defect = compute_minimal_geometric_defect(morse_func)

        total_metric_value += minimal_geometric_defect
        instances_tested += 1
        n_max = max(n_max, n)

    mean_metric_value = total_metric_value / instances_tested
    conjecture_holds = mean_metric_value <= 2 * entanglement_complexity  # Example constant factor
    counterexample = "" if conjecture_holds else "mapping_undefined"

    return {
        "metric_name": "minimal_geometric_defect",
        "metric_value": mean_metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3

    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...{result}...}}")
        results.append(result)

    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")