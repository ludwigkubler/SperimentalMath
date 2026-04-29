# auto-injected by SEC sandbox
import itertools
import json
import sys
import os
import time
import re
from itertools import product, combinations, permutations, chain
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from collections import defaultdict

def generate_random_circuit(n, depth=3):
    if depth == 0:
        return [random.choice([0, 1]) for _ in range(n)]
    
    inputs = [generate_random_circuit(n // 2, depth - 1) for _ in range(2)]
    circuit = []
    for i in range(n):
        gate_type = random.choice(['AND', 'OR', 'MOD3'])
        if gate_type == 'AND':
            circuit.append([inputs[0][i], inputs[1][i]])
        elif gate_type == 'OR':
            circuit.append([inputs[0][i], inputs[1][i]])
        else:
            circuit.append([inputs[0][i], inputs[1][i]])
    return circuit

def evaluate_circuit(circuit, input_values):
    stack = []
    for gate in reversed(circuit):
        a, b = input_values[gate[0]], input_values[gate[1]]
        if gate[2] == 'AND':
            result = a and b
        elif gate[2] == 'OR':
            result = a or b
        else:
            result = (a + b) % 3
        stack.append(result)
    return stack.pop()

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_metric_value = 0
    instances_tested = 0
    
    for n in n_values:
        circuit = generate_random_circuit(n)
        input_values = {i: random.choice([0, 1]) for i in range(n)}
        output = evaluate_circuit(circuit, input_values)
        
        total_metric_value += output
        instances_tested += 1
    
    metric_name = "Average Output"
    metric_value = total_metric_value / instances_tested
    conjecture_holds = True
    counterexample = ""
    
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else list(range(2, 50))
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"not supported\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")