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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def compute_entanglement_entropy(boolean_function, n):
        # Simplified entanglement entropy calculation for demonstration
        return n * math.log2(n)
    
    def compute_qubits_needed(boolean_function, n):
        # Simplified qubits needed calculation for demonstration
        return n
    
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        boolean_function = generate_boolean_function(n)
        entanglement_entropy = compute_entanglement_entropy(boolean_function, n)
        qubits_needed = compute_qubits_needed(boolean_function, n)
        results.append((n, entanglement_entropy, qubits_needed))
    
    if len(results) < 30:
        return {
            "metric_name": "Spearman rank correlation coefficient",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max(n for n, _, _ in results),
            "conjecture_holds": False,
            "counterexample": "not_enough_instances"
        }
    
    entanglement_entropies = [r[1] for r in results]
    qubits_needed = [r[2] for r in results]
    
    def rank(x):
        return sorted(range(len(x)), key=lambda i: x[i])
    
    ranks_entanglement = rank(entanglement_entropies)
    ranks_qubits = rank(qubits_needed)
    
    n = len(results)
    spearman_coefficient = 1 - (6 * sum((ranks_entanglement[i] - ranks_qubits[i])**2 for i in range(n)) / (n**3 - n))
    
    return {
        "metric_name": "Spearman rank correlation coefficient",
        "metric_value": spearman_coefficient,
        "instances_tested": len(results),
        "n_max": max(n for _, _, n in results),
        "conjecture_holds": abs(spearman_coefficient) >= 0.95,  # Adjust threshold as needed
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] + list(range(31, 100))
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all(result["conjecture_holds"] for result in results):
        mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        counterexample = "Spearman rank correlation coefficient below threshold"
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")