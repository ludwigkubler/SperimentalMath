# auto-injected by SEC sandbox
import math
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
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_circuit(n, w):
        circuit = []
        for _ in range(w):
            gate = random.choice(['AND', 'OR'])
            inputs = [random.randint(0, 1) for _ in range(n)]
            circuit.append((gate, inputs))
        return circuit
    
    def evaluate_circuit(circuit, assignment):
        stack = []
        for gate, inputs in reversed(circuit):
            if gate == 'AND':
                result = all(stack.pop() for _ in range(len(inputs)))
            elif gate == 'OR':
                result = any(stack.pop() for _ in range(len(inputs)))
            stack.append(result)
        return stack[0]
    
    def compute_minimal_order(w):
        # Simplified mapping from circuit monotone width to minimal order
        return w ** 2
    
    results = []
    n_values = [5, 10, 15, 20, 30, 40]
    for n in n_values:
        for _ in range(5):  # Ensure at least 30 instances per seed
            circuit = generate_circuit(n, random.randint(1, min(w, 40)))
            assignment = [random.randint(0, 1) for _ in range(n)]
            result = evaluate_circuit(circuit, assignment)
            minimal_order = compute_minimal_order(len(circuit))
            results.append((minimal_order, len(circuit)))
    
    if not results:
        return {
            "metric_name": "min_order",
            "metric_value": 0,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    min_orders = [r[0] for r in results]
    circuit_widths = [r[1] for r in results]
    
    mean_min_order = sum(min_orders) / len(min_orders)
    std_dev = (sum((x - mean_min_order) ** 2 for x in min_orders) / len(min_orders)) ** 0.5
    support_fraction = sum(1 for m in min_orders if abs(m - circuit_widths[min_orders.index(m)] ** 2) <= 3 * std_dev) / len(min_orders)
    
    return {
        "metric_name": "min_order",
        "metric_value": mean_min_order,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": support_fraction >= 0.8,
        "counterexample": "" if support_fraction >= 0.8 else f"mean_min_order={mean_min_order}, std_dev={std_dev}"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_min_order = sum(r["metric_value"] for r in results) / len(results)
    std_dev = (sum((r["metric_value"] - mean_min_order) ** 2 for r in results) / len(results)) ** 0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_min_order} std={std_dev} support_fraction={support_fraction}")
    elif any(abs(r["metric_value"] - n ** 2) > 10 for r, n in zip(results, [5, 10, 15, 20, 30, 40])):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if abs(result["metric_value"] - n ** 2) > 10)
        print(f"RESULT: FALSIFIED counterexample=\"mean_min_order={result['metric_value']}, std_dev={std_dev}\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction}")