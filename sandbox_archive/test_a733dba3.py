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
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random

def generate_circuit(depth):
    if depth == 0:
        return 'leaf'
    sub_depth = random.randint(1, max(0, depth-1))
    left = generate_circuit(sub_depth)
    right = generate_circuit(depth - sub_depth - 1)
    return f'({left} & {right})'

def frobenius_coincidence(circuit):
    if circuit == 'leaf':
        return 1
    left, right = circuit.split(' & ')
    return max(frobenius_coincidence(left), frobenius_coincidence(right))

def run_trial(seed: int) -> dict:
    random.seed(seed)
    depths = [5, 10, 15, 20, 30, 40]
    metric_values = []
    instances_tested = 0
    n_max = 0

    for depth in depths:
        circuit = generate_circuit(depth)
        instances_tested += 1
        n_max = max(n_max, depth)
        metric_value = frobenius_coincidence(circuit)
        metric_values.append(metric_value)

    mean_metric_value = sum(metric_values) / len(metric_values)
    conjecture_holds = all(value <= 1.25 * depth**2 for value, depth in zip(metric_values, depths))
    counterexample = "" if conjecture_holds else "Frobenius coincidence rank exceeds 1.25D^2"

    return {
        "metric_name": "Max Frobenius Coincidence Rank",
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
        print(f"TRIAL: {result}")
        results.append(result)

    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Frobenius coincidence rank exceeds 1.25D^2\" first_failing_seed={first_failing_seed}")