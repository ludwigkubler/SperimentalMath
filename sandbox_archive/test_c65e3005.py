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

def generate_circuit(n):
    if n == 1:
        return ['input']
    elif n == 2:
        return ['and', 'input', 'input']
    else:
        left_size = random.randint(1, n-3)
        right_size = n - 1 - left_size
        left = generate_circuit(left_size)
        right = generate_circuit(right_size)
        gate = random.choice(['and', 'or'])
        return [gate] + left + right

def evaluate_circuit(circuit):
    if circuit[0] == 'input':
        return random.choice([0, 1])
    elif circuit[0] == 'and':
        return evaluate_circuit(circuit[1]) and evaluate_circuit(circuit[2])
    elif circuit[0] == 'or':
        return evaluate_circuit(circuit[1]) or evaluate_circuit(circuit[2])

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    correlation_sum = 0
    instances_tested = 0
    n_max = 0

    for n in n_values:
        for _ in range(5):
            circuit = generate_circuit(n)
            monotone_width = len(circuit) - 1
            value = evaluate_circuit(circuit)
            if value != 0:
                instances_tested += 1
                n_max = max(n_max, n)
                correlation_sum += monotone_width

    mean_correlation = correlation_sum / instances_tested if instances_tested > 0 else 0
    conjecture_holds = mean_correlation >= 0.9 * n_values[-1]
    counterexample = "" if conjecture_holds else "mean_correlation < 0.9 * n_max"

    return {
        "metric_name": "Mean Monotone Width",
        "metric_value": mean_correlation,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []

    for seed in seeds:
        trial_result = run_trial(seed)
        results.append(trial_result)
        print(f"TRIAL: {trial_result}")

    total_metric_value = sum(result["metric_value"] for result in results if result["instances_tested"] > 0)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)

    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={total_metric_value/len(results)} std=0.0 support_fraction=1.0")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mean_correlation < 0.9 * n_max\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")