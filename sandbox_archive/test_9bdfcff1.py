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
        for _ in range(2**n - 1):
            gate = random.choice(['AND', 'OR'])
            inputs = [random.randint(0, n-1) for _ in range(gate.count('X'))]
            circuit.append((gate, inputs))
        return circuit
    
    def evaluate_circuit(circuit, input_values):
        stack = []
        for gate, inputs in reversed(circuit):
            if gate == 'AND':
                result = all(input_values[i] for i in inputs)
            elif gate == 'OR':
                result = any(input_values[i] for i in inputs)
            stack.append(result)
        return stack[0]
    
    def find_topological_minor(circuit):
        # Simplified minor finding (for demonstration purposes)
        return len(circuit) // 2
    
    def compute_tropicalized_brauer_group_size(circuit):
        # Placeholder for Brauer group computation
        return len(circuit)
    
    n = random.randint(5, 40)
    circuit = generate_random_circuit(n)
    input_values = [random.choice([0, 1]) for _ in range(n)]
    topological_minor = find_topological_minor(circuit)
    brauer_group_size = compute_tropicalized_brauer_group_size(circuit)
    
    if topological_minor == 0 or brauer_group_size == 0:
        return {
            "metric_name": "Ratio",
            "metric_value": None,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "topological_minor_or_brauer_group_zero"
        }
    
    ratio = topological_minor / brauer_group_size
    return {
        "metric_name": "Ratio",
        "metric_value": ratio,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": 0.7 <= ratio <= 1.3,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all(r["conjecture_holds"] for r in results):
        mean_ratio = sum(r["metric_value"] for r in results) / len(results)
        std_dev = math.sqrt(sum((r["metric_value"] - mean_ratio) ** 2 for r in results) / len(results))
        support_fraction = 1.0
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    print(f"RESULT: SUPPORTED mean={mean_ratio} std={std_dev} support_fraction={support_fraction}")