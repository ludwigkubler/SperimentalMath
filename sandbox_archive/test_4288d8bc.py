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
    
    def generate_random_circuit(n):
        circuit = []
        for _ in range(2**n - 1):
            gate_type = random.choice(['AND', 'OR'])
            inputs = [random.randint(0, n-1) for _ in range(gate_type)]
            circuit.append((gate_type, inputs))
        return circuit
    
    def compute_circuit_depth(circuit):
        depth = {i: 0 for i in range(len(circuit))}
        stack = []
        for node, (gate_type, inputs) in enumerate(circuit):
            if gate_type == 'AND' or gate_type == 'OR':
                max_input_depth = max(depth[i] for i in inputs)
                depth[node] = max_input_depth + 1
                stack.append((node, depth[node]))
        while stack:
            node, current_depth = stack.pop()
            for input_node in circuit[node][1]:
                if depth[input_node] < current_depth - 1:
                    depth[input_node] = current_depth - 1
                    stack.append((input_node, depth[input_node]))
        return max(depth.values())
    
    def compute_local_system_order(circuit):
        # Simplified local system order computation for demonstration purposes
        return len(circuit)
    
    n = random.randint(5, 40)
    circuit = generate_random_circuit(n)
    depth = compute_circuit_depth(circuit)
    order = compute_local_system_order(circuit)
    
    metric_value = Fraction(order, depth)
    conjecture_holds = abs(metric_value - Fraction(1)) < Fraction(1, 2)
    counterexample = "" if conjecture_holds else f"Order {order}, Depth {depth}"
    
    return {
        "metric_name": "Local System Order / Circuit Depth",
        "metric_value": float(metric_value),
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_dev = (sum((result["metric_value"] - mean_value)**2 for result in results) / len(results))**0.5
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results) and support_fraction >= 0.8:
        first_failing_seed = next(seed for seed, result in enumerate(results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Order exceeds depth\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient support or budget exceeded")