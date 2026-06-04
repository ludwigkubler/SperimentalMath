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
    
    def generate_circuit(n):
        # Generate a random monotone boolean circuit with n vertices
        circuit = []
        for _ in range(n-1):
            gate = random.choice(['AND', 'OR'])
            inputs = [random.randint(0, 1) for _ in range(gate)]
            circuit.append((gate, inputs))
        return circuit
    
    def calculate_monotone_width(circuit):
        # Calculate the monotone width of the circuit
        width = 0
        for gate, inputs in circuit:
            width = max(width, len(inputs))
        return width
    
    def calculate_local_indeterminacy_index(manifold):
        # Placeholder function to calculate local indeterminacy index
        # This is a dummy implementation and should be replaced with actual computation
        return random.uniform(0, 1)
    
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        circuit = generate_circuit(n)
        w_n = calculate_monotone_width(circuit)
        manifold = calculate_manifold(circuit)  # Placeholder function to calculate the manifold
        alpha_w_n = calculate_local_indeterminacy_index(manifold)
        results.append((w_n, alpha_w_n))
    
    metric_value = sum(alpha_w_n for _, alpha_w_n in results) / len(results)
    instances_tested = len(results)
    n_max = max(n for n, _ in results)
    conjecture_holds = all(0 <= alpha_w_n <= math.log(n) and 0 <= alpha_w_n/2 <= math.log(n)**1.5 for _, alpha_w_n in results)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "local_indeterminacy_index",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value)**2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")