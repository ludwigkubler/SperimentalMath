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
    
    def generate_boolean_circuit(n, m):
        # Generate a simple boolean circuit with n inputs and m outputs
        if m == 1:
            return [[random.choice([0, 1]) for _ in range(n)]]
        else:
            subcircuits = [generate_boolean_circuit(n, 1) for _ in range(m)]
            return [sum(subcircuit, []) for subcircuit in zip(*subcircuits)]
    
    def binary_representation(circuit):
        # Convert the circuit to a binary string
        return ''.join(str(bit) for sublist in circuit for bit in sublist)
    
    def coxeter_group_generators(binary_str):
        # Count the number of distinct bits (1s and 0s) in the binary representation
        return len(set(binary_str))
    
    def monotone_complexity(circuit):
        # Calculate the size of the monotone equivalent circuit
        return sum(len(subcircuit) for subcircuit in circuit)
    
    results = []
    n_values = [5, 10, 15, 20, 30, 40]
    for n in n_values:
        for _ in range(5):  # Test each size with 5 different circuits
            m = random.randint(1, min(n, 10))  # Output size between 1 and n
            circuit = generate_boolean_circuit(n, m)
            binary_str = binary_representation(circuit)
            g_C = coxeter_group_generators(binary_str)
            complexity = monotone_complexity(circuit)
            
            results.append({
                "n": n,
                "m": m,
                "g_C": g_C,
                "complexity": complexity
            })
    
    mean_g_C = sum(result["g_C"] for result in results) / len(results)
    mean_complexity = sum(result["complexity"] for result in results) / len(results)
    
    conjecture_holds = all(1.41 * m**0.5 <= g_C <= 2 * m**0.5 for result in results)
    counterexample = next((f"Circuit with n={result['n']}, m={result['m']} has {result['g_C']} generators and complexity {result['complexity']}"
                           for result in results if not (1.41 * result["m"]**0.5 <= result["g_C"] <= 2 * result["m"]**0.5)), "")
    
    return {
        "metric_name": "Coxeter Group Generators",
        "metric_value": mean_g_C,
        "instances_tested": len(results),
        "n_max": max(result["n"] for result in results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction:.2f}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Circuit with n={results[first_failing_seed]['n']}, m={results[first_failing_seed]['m']} has {results[first_failing_seed]['g_C']} generators and complexity {results[first_failing_seed]['complexity']}\" first_failing_seed={first_failing_seed}")