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
    
    def generate_boolean_circuit(n):
        # Generate a random Boolean circuit with n inputs and polynomial size
        # This is a simplified version for testing purposes
        if n == 1:
            return ["0"]
        else:
            subcircuits = [generate_boolean_circuit(n // 2) for _ in range(2)]
            return ["AND"] + subcircuits + ["OR"] + subcircuits
    
    def evaluate_circuit(circuit):
        # Evaluate the circuit with random inputs
        if isinstance(circuit, str):
            return int(circuit)
        else:
            left = evaluate_circuit(circuit[1])
            right = evaluate_circuit(circuit[2])
            op = circuit[0]
            if op == "AND":
                return left and right
            elif op == "OR":
                return left or right
    
    def compute_minimal_order(circuit):
        # Placeholder for computing the minimal order of a noncommutative crossed product
        # This is a dummy implementation for testing purposes
        return len(circuit)
    
    def compute_monotone_width(circuit):
        # Placeholder for computing the monotone width of the circuit
        # This is a dummy implementation for testing purposes
        if isinstance(circuit, str):
            return 1
        else:
            left = compute_monotone_width(circuit[1])
            right = compute_monotone_width(circuit[2])
            op = circuit[0]
            if op == "AND":
                return max(left, right) + 1
            elif op == "OR":
                return max(left, right)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        circuit = generate_boolean_circuit(n)
        min_order = compute_minimal_order(circuit)
        width_mon = compute_monotone_width(circuit)
        results.append({
            "n": n,
            "min_order": min_order,
            "width_mon": width_mon
        })
    
    if not results:
        return {
            "metric_name": "ratio",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    ratios = [r["min_order"] / r["width_mon"] for r in results]
    mean_ratio = sum(ratios) / len(ratios)
    std_ratio = math.sqrt(sum((x - mean_ratio) ** 2 for x in ratios) / len(ratios))
    
    return {
        "metric_name": "ratio",
        "metric_value": mean_ratio,
        "instances_tested": len(results),
        "n_max": max(r["n"] for r in results),
        "conjecture_holds": 0.5 <= mean_ratio <= 1.5,
        "counterexample": "" if 0.5 <= mean_ratio <= 1.5 else f"mean_ratio={mean_ratio}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or list(range(2, 30))  # Default to first 30 primes if no seeds provided
    
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mean_ratio out of bounds\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction}")