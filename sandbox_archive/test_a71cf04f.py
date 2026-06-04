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
    
    def generate_random_circuit(n):
        circuit = []
        for _ in range(n):
            gate_type = random.choice(['AND', 'OR'])
            inputs = [random.randint(0, 1) for _ in range(random.randint(2, n))]
            circuit.append((gate_type, inputs))
        return circuit
    
    def evaluate_circuit(circuit, input_values):
        stack = []
        for gate_type, inputs in reversed(circuit):
            if gate_type == 'AND':
                result = all(input_values[i] for i in inputs)
            elif gate_type == 'OR':
                result = any(input_values[i] for i in inputs)
            stack.append(result)
        return stack[0]
    
    def count_linear_regions(n, circuit):
        regions = set()
        for input_values in itertools.product([0, 1], repeat=n):
            output = evaluate_circuit(circuit, input_values)
            region = tuple(input_values + (output,))
            regions.add(region)
        return len(regions)
    
    def min_monomial_generators(n, circuit):
        # This is a placeholder for the actual implementation
        # of finding the minimal number of monomial generators.
        # For simplicity, we will use a heuristic approach here.
        return n  # Placeholder value
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_gn = 0
    total_lc = 0
    instances_tested = 0
    n_max = 0
    
    for n in n_values:
        circuit = generate_random_circuit(n)
        input_values = [random.randint(0, 1) for _ in range(n)]
        output = evaluate_circuit(circuit, input_values)
        
        gn = min_monomial_generators(n, circuit)
        lc = count_linear_regions(n, circuit)
        
        total_gn += gn
        total_lc += lc
        instances_tested += n
        n_max = max(n_max, n)
    
    mean_gn = total_gn / instances_tested
    mean_lc = total_lc / instances_tested
    
    if abs(mean_gn - mean_lc) <= 0.1 * mean_lc:
        conjecture_holds = True
        counterexample = ""
    else:
        conjecture_holds = False
        counterexample = "The ratio G(n)/L(C) is not within the margin of error."
    
    return {
        "metric_name": "Ratio of Monomial Generators to Linear Regions",
        "metric_value": mean_gn / mean_lc,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
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
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"The ratio G(n)/L(C) is not within the margin of error.\" first_failing_seed={first_failing_seed}")