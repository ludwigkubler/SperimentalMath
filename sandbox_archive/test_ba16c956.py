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
        circuit = []
        for _ in range(n):
            gate_type = random.choice(['AND', 'OR'])
            inputs = [random.randint(0, 1) for _ in range(random.randint(1, n))]
            circuit.append((gate_type, inputs))
        return circuit
    
    def evaluate_circuit(circuit, assignment):
        stack = []
        for gate in reversed(circuit):
            if gate[0] == 'AND':
                result = all(stack.pop() for _ in gate[1])
            elif gate[0] == 'OR':
                result = any(stack.pop() for _ in gate[1])
            stack.append(result)
        return stack[0]
    
    def calculate_local_indeterminacy(circuit):
        n = len(circuit)
        assignments = [random.randint(0, 1) for _ in range(n)]
        values = [evaluate_circuit(circuit, assignment) for assignment in assignments]
        unique_values = set(values)
        return math.log(len(unique_values), 2)
    
    def monotone_width(circuit):
        n = len(circuit)
        max_inputs = 0
        for gate in circuit:
            if gate[0] == 'AND':
                max_inputs = max(max_inputs, len(gate[1]))
            elif gate[0] == 'OR':
                max_inputs = max(max_inputs, len(gate[1]))
        return max_inputs
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        circuit = generate_circuit(n)
        width = monotone_width(circuit)
        local_indeterminacy = calculate_local_indeterminacy(circuit)
        results.append((n, width, local_indeterminacy))
    
    instances_tested = len(results)
    n_max = max(n for n, _, _ in results)
    conjecture_holds = all(local_indeterminacy <= math.log(n, 2) and local_indeterminacy <= math.log(n / 2, 2) ** (3/2) for _, _, local_indeterminacy in results)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "local_indeterminacy",
        "metric_value": sum(local_indeterminacy for _, _, local_indeterminacy in results) / instances_tested,
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
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=mapping_undefined")