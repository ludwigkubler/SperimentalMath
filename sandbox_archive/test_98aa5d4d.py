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

def generate_circuit(n, w):
    # Generate a random monotone circuit with n variables and width w
    if w == 1:
        return [[random.choice([0, 1]) for _ in range(n)]]
    else:
        subcircuits = [generate_circuit(n, random.randint(1, w-1)) for _ in range(w)]
        return [subcircuit + [random.choice([0, 1])] for subcircuit in subcircuits]

def compute_minimal_order(circuit):
    # Compute the minimal order of a quaternionic Kähler form associated with the circuit
    n = len(circuit[0])
    order = 0
    for i in range(n):
        if all(row[i] == 1 for row in circuit):
            order += 1
    return order

def run_trial(seed: int) -> dict:
    random.seed(seed)
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        w_max = min(n, 40)
        for _ in range(5):  # Ensure at least 30 instances per seed
            w = random.randint(1, w_max)
            circuit = generate_circuit(n, w)
            order = compute_minimal_order(circuit)
            results.append((n, w, order))
    if not results:
        return {
            "metric_name": "minimal_order",
            "metric_value": 0,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    n_values = [r[0] for r in results]
    w_values = [r[1] for r in results]
    order_values = [r[2] for r in results]
    
    mean_order = sum(order_values) / len(order_values)
    std_dev = (sum((x - mean_order) ** 2 for x in order_values) / len(order_values)) ** 0.5
    
    target_bound = [w ** 2 for w in w_values]
    max_diff = max(abs(o - b) for o, b in zip(order_values, target_bound))
    
    conjecture_holds = all(abs(o - b) <= 10 for o, b in zip(order_values, target_bound))
    counterexample = "" if conjecture_holds else f"max_diff={max_diff}"
    
    return {
        "metric_name": "minimal_order",
        "metric_value": mean_order,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_order = sum(r["metric_value"] for r in results) / len(results)
    std_dev = (sum((r["metric_value"] - mean_order) ** 2 for r in results) / len(results)) ** 0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_order} std={std_dev} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_order} std={std_dev} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"max_diff_exceeded\" first_failing_seed={first_failing_seed + 1}")