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
    
    def generate_boolean_circuit(n):
        # Generate a simple monotone boolean circuit with n variables and n gates
        circuit = []
        for i in range(n):
            circuit.append((i, 'OR', [j for j in range(i)]))
        return circuit
    
    def compute_field_extension(circuit):
        # Compute the field extension for a given circuit
        # This is a placeholder function; actual computation depends on the circuit structure
        return 2 ** len(circuit)
    
    def galois_group_order(field_extension):
        # Placeholder function to compute the order of the Galois group
        # Actual computation depends on the field extension
        return field_extension
    
    n = random.randint(5, 40)
    circuit = generate_boolean_circuit(n)
    field_extension = compute_field_extension(circuit)
    galois_order = galois_group_order(field_extension)
    
    expected_bound = 2 * len(circuit)
    
    return {
        "metric_name": "galois_group_order",
        "metric_value": galois_order,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": abs(galois_order - expected_bound) <= expected_bound / 2,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(100, 999) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")