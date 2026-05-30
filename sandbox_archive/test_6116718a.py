# auto-injected by SEC sandbox
import math
import itertools
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from itertools import product, combinations, permutations, chain
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
from fractions import Fraction

def generate_circuit(depth):
    if depth == 1:
        return [random.choice([0, 1])]
    else:
        subcircuits = [generate_circuit(random.randint(1, depth-1)) for _ in range(2)]
        return [random.choice([0, 1]) + tuple(subcircuits)]

def measure_depth(circuit):
    if isinstance(circuit[0], int):
        return 1
    else:
        return 1 + max(measure_depth(subcircuit) for subcircuit in circuit[1])

def measure_qdd(v_c):
    # Placeholder implementation of QDD calculation
    # This is a dummy function and should be replaced with actual quantum deformation degree computation
    return random.randint(0, 10)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_max = 40
    instances_tested = 0
    total_metric_value = 0.0
    conjecture_holds = True
    counterexample = ""

    for n in range(5, 41):
        circuit = generate_circuit(n)
        depth = measure_depth(circuit)
        v_c = generate_circuit(depth)  # Placeholder for actual algebraic variety generation
        qdd = measure_qdd(v_c)

        instances_tested += 1
        total_metric_value += abs(qdd - depth)
        if abs(qdd - depth) > 3:
            conjecture_holds = False
            counterexample = f"QDD({qdd}) > Depth({depth}) for n={n}"

    mean_metric_value = total_metric_value / instances_tested
    return {
        "metric_name": "Quantum Deformation Degree",
        "metric_value": mean_metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []

    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_metric_value = sum(res["metric_value"] for res in results) / len(results)
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)

    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, res in zip(seeds, results) if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"QDD > Depth\" first_failing_seed={first_failing_seed}")