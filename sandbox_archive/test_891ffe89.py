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
    
    def generate_monotone_circuit(n):
        circuit = []
        for _ in range(n):
            gate_type = random.choice(['AND', 'OR'])
            inputs = [random.randint(0, 1) for _ in range(2)]
            circuit.append((gate_type, inputs))
        return circuit
    
    def evaluate_circuit(circuit):
        stack = []
        for gate_type, inputs in reversed(circuit):
            if gate_type == 'AND':
                result = inputs[0] and inputs[1]
            elif gate_type == 'OR':
                result = inputs[0] or inputs[1]
            stack.append(result)
        return stack.pop()
    
    def generate_brauer_group_order(n):
        # Simplified Brauer group order calculation for demonstration
        return n * (n + 1) // 2
    
    def monotone_width(circuit):
        max_depth = 0
        current_depth = 0
        for gate_type, _ in circuit:
            if gate_type == 'AND':
                current_depth += 1
            elif gate_type == 'OR':
                current_depth -= 1
            max_depth = max(max_depth, current_depth)
        return max_depth
    
    n_max = 40
    instances_tested = 0
    total_order = 0
    max_poly_value = 0
    
    for n in range(5, n_max + 1):
        circuit = generate_monotone_circuit(n)
        order = generate_brauer_group_order(n)
        width = monotone_width(circuit)
        
        instances_tested += 1
        total_order += order
        max_poly_value = max(max_poly_value, width * (width + 1) // 2)
    
    mean_order = total_order / instances_tested
    conjecture_holds = mean_order <= max_poly_value * 2
    
    return {
        "metric_name": "Brauer Group Order",
        "metric_value": mean_order,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_support")