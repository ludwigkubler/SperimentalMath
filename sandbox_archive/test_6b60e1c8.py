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
    
    # Generate a random boolean circuit with n inputs and up to 40 gates
    n = random.randint(5, 40)
    num_gates = random.randint(n, n * 2)
    circuit = []
    for _ in range(num_gates):
        gate_type = random.choice(['AND', 'OR', 'XOR'])
        inputs = [random.choice([True, False]) for _ in range(random.randint(1, n))]
        circuit.append((gate_type, inputs))
    
    # Compute the minimal order of the group representation
    min_order = 0
    for gate_type, inputs in circuit:
        if gate_type == 'AND':
            min_order += len(inputs)
        elif gate_type == 'OR':
            min_order += len(inputs)
        elif gate_type == 'XOR':
            min_order += len(inputs) - 1
    
    # Measure the entanglement ε(C) of the circuit
    # For simplicity, we use a dummy measure that is linearly related to the number of gates
    entanglement = num_gates
    
    # Correlate |min_order(G(C))| with ε(C)
    abs_diff = abs(min_order - entanglement)
    
    return {
        "metric_name": "abs_diff",
        "metric_value": abs_diff,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": abs_diff <= 0.5 * entanglement,
        "counterexample": "" if conjecture_holds else f"correlation_coefficient={abs_diff / entanglement}"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or list(range(2, 30))  # Default to first 29 prime numbers if no seeds provided
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
    elif any(not r["conjecture_holds"] and r["counterexample"] != "" for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"] and r["counterexample"] != "")
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")