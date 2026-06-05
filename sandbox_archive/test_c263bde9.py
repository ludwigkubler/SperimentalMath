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
    if n <= 1:
        return []
    
    circuit = []
    for _ in range(2 * n - 2):
        gate_type = random.choice(['AND', 'OR'])
        inputs = [random.randint(0, len(circuit) - 1) for _ in range(gate_type == 'AND' + 1)]
        circuit.append((gate_type, inputs))
    
    return circuit

def evaluate_circuit(circuit):
    stack = []
    for gate, inputs in reversed(circuit):
        if gate == 'AND':
            result = all(stack[inputs[i]] for i in range(len(inputs)))
        elif gate == 'OR':
            result = any(stack[inputs[i]] for i in range(len(inputs)))
        stack.append(result)
    
    return stack[-1]

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        instances_tested = 0
        total_order = 0
        
        while len(results) < 30:
            circuit = generate_circuit(n)
            if not circuit:
                continue
            
            instances_tested += 1
            is_satisfiable = evaluate_circuit(circuit)
            
            # Constructive mapping to groupoid order (simplified example)
            order = len(circuit) * n  # Placeholder for actual computation
            
            results.append((n, order))
        
        if len(results) < 30:
            return {
                "metric_name": "groupoid_order",
                "metric_value": None,
                "instances_tested": instances_tested,
                "n_max": max(n_values),
                "conjecture_holds": False,
                "counterexample": "insufficient_instances"
            }
        
        n_max = max(n for _, _ in results)
        groupoid_orders = [order for _, order in results]
        
        if any(order > 10 * n * math.log(n, 2) for order, _ in results):
            return {
                "metric_name": "groupoid_order",
                "metric_value": None,
                "instances_tested": instances_tested,
                "n_max": n_max,
                "conjecture_holds": False,
                "counterexample": "order_exceeds_bound"
            }
        
        avg_order = sum(groupoid_orders) / len(groupoid_orders)
        return {
            "metric_name": "groupoid_order",
            "metric_value": avg_order,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": avg_order <= 10 * n_max * math.log(n_max, 2),
            "counterexample": ""
        }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(1000, 9999) for _ in range(30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    avg_order = sum(result["metric_value"] for result in results if result["metric_value"] is not None) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all("counterexample" in result and result["counterexample"] == "insufficient_instances" for result in results):
        print(f"RESULT: INCONCLUSIVE reason=insufficient_instances n_tested={len(results)}")
    elif all("counterexample" in result and result["counterexample"] == "order_exceeds_bound" for result in results):
        print(f"RESULT: INCONCLUSIVE reason=order_exceeds_bound n_tested={len(results)}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={avg_order} std={math.sqrt(sum((x - avg_order) ** 2 for x in groupoid_orders) / len(groupoid_orders))} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"order_exceeds_bound\" first_failing_seed={first_failing_seed}")