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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_circuit(n):
        # Generate a random boolean circuit with n inputs
        if n == 1:
            return [[0], [1]]
        else:
            subcircuits = [generate_circuit(n // 2) for _ in range(2)]
            return [subcircuit + [n] for subcircuit in subcircuits]
    
    def compute_semgroup_size(circuit):
        # Compute the minimal order of the monoid generators |S(C)|
        n = len(circuit)
        if n == 1:
            return 1
        else:
            semgroup = set()
            for i in range(2 ** (n - 1)):
                state = [0] * (n - 1)
                for j in range(n):
                    if circuit[j][-1] == 1:
                        state[(i >> j) & 1] ^= 1
                semgroup.add(tuple(state))
            return len(semgroup)
    
    def compute_circuitmonowidth(circuit):
        # Compute the monotone width w(C)
        n = len(circuit)
        if n == 1:
            return 1
        else:
            width = 0
            for i in range(2 ** (n - 1)):
                state = [0] * (n - 1)
                for j in range(n):
                    if circuit[j][-1] == 1:
                        state[(i >> j) & 1] ^= 1
                width = max(width, sum(state))
            return width
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_semgroup_size = 0
    total_circuitmonowidth = 0
    instances_tested = 0
    
    for n in n_values:
        for _ in range(5):  # Test each size 5 times
            circuit = generate_circuit(n)
            semgroup_size = compute_semgroup_size(circuit)
            circuitmonowidth = compute_circuitmonowidth(circuit)
            if circuitmonowidth > 0:  # Avoid division by zero
                total_semgroup_size += semgroup_size
                total_circuitmonowidth += circuitmonowidth
                instances_tested += 1
    
    if total_circuitmonowidth == 0:
        return {
            "metric_name": "Semigroup Size / Circuit Monotone Width",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "Circuit Monotone Width is zero"
        }
    
    ratio = Fraction(total_semgroup_size, total_circuitmonowidth)
    return {
        "metric_name": "Semigroup Size / Circuit Monotone Width",
        "metric_value": float(ratio),
        "instances_tested": instances_tested,
        "n_max": max(n_values),
        "conjecture_holds": ratio <= 1,
        "counterexample": "" if ratio <= 1 else f"Ratio: {ratio}, Expected: ≤ 1"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all(result["conjecture_holds"] for result in results):
        mean_value = sum(result["metric_value"] for result in results) / len(results)
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_value} std=0 support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Ratio exceeded 1\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")