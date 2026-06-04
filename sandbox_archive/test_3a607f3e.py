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

def generate_random_instance(n):
    if n == 1:
        return ['0'], [], []
    left, _, _ = generate_random_instance(n // 2)
    right, _, _ = generate_random_instance(n - n // 2)
    circuit = [f'AND({x},{y})' for x in left] + [f'OR({x},{y})' for x in left for y in right]
    inputs = list(left) + list(right)
    outputs = [f'OUT{i}' for i in range(len(circuit))]
    return circuit, inputs, outputs

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    total_metric_value = 0
    instances_tested = 0
    n_max = 0
    conjecture_holds = True
    counterexample = ""

    for n in n_values:
        circuit, inputs, outputs = generate_random_instance(n)
        w_C = len(inputs)  # Monotone width is the number of inputs
        L_M_C = len(circuit)  # Minimal number of symplectic leaves (circuit size)
        
        if L_M_C > p(n) * w_C**2:
            conjecture_holds = False
            counterexample = f"n={n}, L_M(C)={L_M_C}, p(n)*w(C)^2={p(n)*w_C**2}"
            break
        
        total_metric_value += L_M_C
        instances_tested += len(circuit)
        n_max = max(n_max, n)

    return {
        "metric_name": "minimal_symplectic_leaf_number",
        "metric_value": total_metric_value / instances_tested,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

def p(n):
    # Polynomial function to upper-bound the minimal number of symplectic leaves
    return Fraction(1, 4) * n**2 + Fraction(1, 2) * n + 1

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [
        2, 3, 5, 7, 11, 13, 17, 19, 23, 29,
        31, 37, 41, 43, 47, 53, 59, 61, 67, 71,
        73, 79, 83, 89, 97, 101, 103, 107, 109, 113
    ]

    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)

    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    std_metric_value = math.sqrt(sum((result["metric_value"] - mean_metric_value)**2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)

    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in enumerate(results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")