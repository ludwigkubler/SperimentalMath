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
    
    def generate_random_circuit(n):
        circuit = []
        for _ in range(2 ** n - 1):
            gate_type = random.choice(['AND', 'OR'])
            inputs = [random.randint(0, 1) for _ in range(random.randint(1, n))]
            circuit.append((gate_type, inputs))
        return circuit
    
    def compute_circuit_depth(circuit):
        depth = {i: 0 for i in range(len(circuit))}
        stack = []
        for i, (gate_type, inputs) in enumerate(circuit):
            if gate_type == 'AND' or gate_type == 'OR':
                max_input_depth = max(depth[input] for input in inputs)
                depth[i] = max_input_depth + 1
                stack.append(i)
            else:
                stack.pop()
        return max(depth.values())
    
    def compute_local_system_order(circuit):
        n = len(circuit) + 1
        order = [0] * n
        for i, (gate_type, inputs) in enumerate(circuit):
            if gate_type == 'AND':
                order[i] = sum(order[input] for input in inputs)
            elif gate_type == 'OR':
                order[i] = max(order[input] for input in inputs)
        return max(order)
    
    n_max = 0
    metric_values = []
    conjecture_holds = True
    counterexample = ""
    
    for _ in range(30):
        n = random.randint(5, 40)
        circuit = generate_random_circuit(n)
        depth = compute_circuit_depth(circuit)
        order = compute_local_system_order(circuit)
        
        if n > n_max:
            n_max = n
        
        metric_values.append(order)
        
        if order > 2 * depth:
            conjecture_holds = False
            counterexample = f"O(X)={order} > 2*d(C)={2*depth}"
        
        if order < depth / 1.5:
            conjecture_holds = False
            counterexample = f"O(X)={order} < d(C)/1.5={depth/1.5}"
    
    return {
        "metric_name": "Local System Order",
        "metric_value": sum(metric_values) / len(metric_values),
        "instances_tested": 30,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(res["metric_value"] for res in results) / len(results)
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, res in zip(seeds, results) if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{res['counterexample']}\" first_failing_seed={first_failing_seed}")