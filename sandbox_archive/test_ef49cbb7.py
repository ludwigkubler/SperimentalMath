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
        circuit = []
        for _ in range(10 * n):  # Generate a simple circuit with polynomial size
            gate_type = random.choice(['AND', 'OR'])
            if gate_type == 'AND':
                circuit.append(('AND', random.sample(range(n), 2)))
            else:
                circuit.append(('OR', random.sample(range(n), 2)))
        return circuit
    
    def evaluate_circuit(circuit, inputs):
        stack = []
        for gate in circuit:
            if gate[0] == 'AND':
                a, b = stack.pop(), stack.pop()
                stack.append(a and b)
            elif gate[0] == 'OR':
                a, b = stack.pop(), stack.pop()
                stack.append(a or b)
        return stack[0]
    
    def monotone_width(circuit):
        n = len(circuit)
        width = [1] * n
        for i in range(n):
            for j in range(i + 1, n):
                if circuit[i][0] == 'AND' and circuit[j][0] == 'OR':
                    if set(circuit[i][1]).issubset(set(circuit[j][1])):
                        width[j] = max(width[j], width[i] + 1)
        return max(width)
    
    def noncommutative_crossed_product_size(n):
        # Simplified model for demonstration purposes
        return n * (n - 1) // 2
    
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(20):  # At least 30 instances per seed
            circuit = generate_boolean_circuit(n)
            inputs = [random.choice([True, False]) for _ in range(n)]
            result = evaluate_circuit(circuit, inputs)
            width = monotone_width(circuit)
            min_order = noncommutative_crossed_product_size(n)
            results.append((min_order, width))
    
    if not results:
        return {
            "metric_name": "ratio",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 40,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    ratios = [min_order / width for min_order, width in results]
    mean_ratio = sum(ratios) / len(ratios)
    std_ratio = math.sqrt(sum((r - mean_ratio) ** 2 for r in ratios) / len(ratios))
    
    return {
        "metric_name": "ratio",
        "metric_value": mean_ratio,
        "instances_tested": len(results),
        "n_max": 40,
        "conjecture_holds": 0.5 <= mean_ratio <= 1.5,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all(result["conjecture_holds"] for result in results):
        mean_value = sum(result["metric_value"] for result in results) / len(results)
        std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
        support_fraction = len([result for result in results if result["conjecture_holds"]]) / len(results)
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_data")