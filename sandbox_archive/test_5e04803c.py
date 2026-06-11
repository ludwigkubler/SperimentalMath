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
    
    def generate_random_boolean_circuit(n):
        depth = random.randint(5, 10)
        circuit = []
        for _ in range(depth):
            gate_type = random.choice(['AND', 'OR'])
            if gate_type == 'AND':
                inputs = [random.randint(0, 1) for _ in range(random.randint(2, n))]
            else:
                inputs = [random.randint(0, 1) for _ in range(random.randint(2, n))]
            circuit.append((gate_type, inputs))
        return circuit
    
    def evaluate_circuit(circuit):
        stack = []
        for gate_type, inputs in reversed(circuit):
            if gate_type == 'AND':
                result = all(stack.pop() for _ in inputs)
            else:
                result = any(stack.pop() for _ in inputs)
            stack.append(result)
        return stack[0]
    
    def find_root_system_dimension(circuit):
        n = len(circuit)
        depth = evaluate_circuit(circuit)
        dimension = 2 * depth
        return dimension
    
    metric_name = "root_system_dimension"
    instances_tested = 30
    n_max = 15
    conjecture_holds = True
    counterexample = ""
    
    results = []
    for _ in range(instances_tested):
        n = random.randint(5, n_max)
        circuit = generate_random_boolean_circuit(n)
        dimension = find_root_system_dimension(circuit)
        depth = evaluate_circuit(circuit)
        results.append((dimension, depth))
    
    if len(results) < instances_tested:
        return {
            "metric_name": metric_name,
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "insufficient_data"
        }
    
    dimensions, depths = zip(*results)
    correlation_coefficient = sum((x - mean_x) * (y - mean_y) for x, y in zip(dimensions, depths)) / math.sqrt(sum((x - mean_x)**2 for x in dimensions) * sum((y - mean_y)**2 for y in depths))
    
    if correlation_coefficient < 0.7:
        conjecture_holds = False
        counterexample = f"correlation_coefficient={correlation_coefficient}"
    
    return {
        "metric_name": metric_name,
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all(r["conjecture_holds"] for r in results):
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        counterexample = result["counterexample"]
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE no_data")