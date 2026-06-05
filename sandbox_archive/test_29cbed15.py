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

def generate_circuit(n):
    if n == 1:
        return [[0, 1]]
    
    circuit = []
    for _ in range(n - 1):
        gate_type = random.choice(['AND', 'OR'])
        inputs = [random.randint(0, len(circuit) - 1) for _ in range(gate_type == 'AND' + 1)]
        output = len(circuit)
        circuit.append([gate_type, inputs, output])
    
    return circuit

def evaluate_circuit(circuit, assignment):
    stack = []
    for gate in reversed(circuit):
        if gate[0] == 'AND':
            a = assignment[gate[2]]
            b = assignment[gate[1][0]]
            c = assignment[gate[1][1]]
            stack.append(a and (b or c))
        elif gate[0] == 'OR':
            a = assignment[gate[2]]
            b = assignment[gate[1][0]]
            c = assignment[gate[1][1]]
            stack.append(a or (not b and not c))
    
    return stack[-1]

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_values = [5, 10, 15, 20, 30, 40]
    metric_values = []
    instances_tested = 0
    n_max = 0
    
    for n in n_values:
        if n > n_max:
            n_max = n
        
        for _ in range(5):
            circuit = generate_circuit(n)
            assignment = {i: random.randint(0, 1) for i in range(len(circuit))}
            result = evaluate_circuit(circuit, assignment)
            
            instances_tested += 1
            metric_values.append(result)
    
    mean_value = sum(metric_values) / len(metric_values)
    std_value = math.sqrt(sum((x - mean_value) ** 2 for x in metric_values) / len(metric_values))
    
    conjecture_holds = all(abs(x - y) <= 0.1 * y for x, y in zip(metric_values, [n * math.log(n) for n in n_values]))
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "circuit_satisfiability",
        "metric_value": mean_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...run_trial output...}}")
    
    mean_value = sum(trial_result["metric_value"] for trial_result in [run_trial(seed) for seed in seeds]) / len(seeds)
    std_value = math.sqrt(sum((trial_result["metric_value"] - mean_value) ** 2 for trial_result in [run_trial(seed) for seed in seeds]) / len(seeds))
    
    support_fraction = sum(1 for trial_result in [run_trial(seed) for seed in seeds] if trial_result["conjecture_holds"]) / len(seeds)
    
    if all(trial_result["conjecture_holds"] for trial_result in [run_trial(seed) for seed in seeds]):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not trial_result["conjecture_holds"] for trial_result in [run_trial(seed) for seed in seeds]):
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed=1")
    else:
        print("RESULT: INCONCLUSIVE reason=mapping_undefined")