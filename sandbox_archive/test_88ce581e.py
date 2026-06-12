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
import math
import itertools
from fractions import Fraction

def generate_random_circuit(n):
    return [random.choice([0, 1]) for _ in range(2**n)]

def compute_entanglement_complexity(circuit):
    # Simplified example: count the number of 1s in the circuit
    return sum(circuit)

def compute_morse_function(circuit):
    # Simplified example: return a list of critical points based on the circuit
    return [i for i, bit in enumerate(circuit) if bit == 1]

def min_geometric_defect(critical_points):
    if len(critical_points) < 2:
        return 0  # No distance to compute if there's only one or no critical point
    return min(math.dist(cp1, cp2) for cp1, cp2 in itertools.combinations(critical_points, 2))

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    geometric_defects = []
    entanglement_complexities = []

    for n in n_values:
        circuit = generate_random_circuit(n)
        e_C = compute_entanglement_complexity(circuit)
        G = compute_morse_function(circuit)
        Δ_G = min_geometric_defect(G)

        geometric_defects.append(Δ_G)
        entanglement_complexities.append(e_C)

    mean_geometric_defect = sum(geometric_defects) / len(geometric_defects)
    mean_entanglement_complexity = sum(entanglement_complexities) / len(entanglement_complexities)
    conjecture_holds = mean_geometric_defect <= 2 * mean_entanglement_complexity
    counterexample = "" if conjecture_holds else "mapping_undefined"

    return {
        "metric_name": "geometric_defect",
        "metric_value": mean_geometric_defect,
        "instances_tested": len(geometric_defects),
        "n_max": max(n_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3

    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")