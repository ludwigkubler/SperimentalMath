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
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from fractions import Fraction

def generate_boolean_circuit(n, d):
    if n == 1:
        return [random.choice([0, 1])]
    elif d == 2:
        inputs = generate_boolean_circuit(n // 2, d - 1)
        return [random.choice([0, 1]) for _ in range(2 * len(inputs))]
    else:
        left = generate_boolean_circuit(n // 2, d - 1)
        right = generate_boolean_circuit(n // 2, d - 1)
        return [random.choice(left + right) for _ in range(len(left))]

def compute_monotone_width(circuit):
    n = len(circuit)
    width = 0
    for i in range(1 << n):
        active = [j for j in range(n) if (i >> j) & 1]
        if all(circuit[j] == circuit[active[0]] for j in active):
            width = max(width, len(active))
    return width

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    instances_tested = 0
    total_metric_value = 0.0
    conjecture_holds = True
    counterexample = ""

    for n in n_values:
        for _ in range(5):  # Ensure at least 30 instances per seed
            circuit = generate_boolean_circuit(n, random.randint(2, 5))
            monotone_width = compute_monotone_width(circuit)
            upper_bound = math.ceil(math.sqrt(n) * (random.randint(2, 5) ** (3/2)))
            if monotone_width > upper_bound:
                conjecture_holds = False
                counterexample = f"n={n}, d={len(circuit)}, width={monotone_width}, bound={upper_bound}"
                break
            total_metric_value += monotone_width
            instances_tested += 1

    return {
        "metric_name": "Monotone Width",
        "metric_value": total_metric_value / instances_tested,
        "instances_tested": instances_tested,
        "n_max": max(n_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)

    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    std_metric_value = math.sqrt(sum((result["metric_value"] - mean_metric_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)

    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")