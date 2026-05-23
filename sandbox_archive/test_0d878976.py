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
    
    def generate_monotone_xor_circuit(n):
        circuit = []
        for _ in range(n):
            gate_type = random.choice(['AND', 'OR'])
            inputs = [random.randint(0, 1) for _ in range(random.randint(2, n))]
            circuit.append((gate_type, inputs))
        return circuit
    
    def quandle_group_representation(circuit):
        # Simplified representation using a dictionary
        quandle = {}
        for gate_type, inputs in circuit:
            if gate_type == 'AND':
                key = tuple(sorted(inputs + [1]))
                if key not in quandle:
                    quandle[key] = len(quandle) + 1
            elif gate_type == 'OR':
                key = tuple(sorted(inputs + [0]))
                if key not in quandle:
                    quandle[key] = len(quandle) + 1
        return quandle
    
    def minimal_order(quandle):
        orders = list(quandle.values())
        return min(orders[1:], default=0)
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_min_orders = 0
    instances_tested = 0
    
    for n in n_values:
        for _ in range(5):  # Ensure at least 5 instances per size
            circuit = generate_monotone_xor_circuit(n)
            quandle = quandle_group_representation(circuit)
            min_order = minimal_order(quandle)
            total_min_orders += min_order
            instances_tested += 1
    
    mean_min_order = total_min_orders / instances_tested
    std_dev = math.sqrt(sum((x - mean_min_order) ** 2 for x in range(5, 41)) / (instances_tested - 1))
    
    conjecture_holds = mean_min_order <= n_values[-1] ** 2 and std_dev <= 0.1 * mean_min_order
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "Minimal Order of Quandle Group",
        "metric_value": mean_min_order,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_min_order = sum(r["metric_value"] for r in results) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean_min_order) ** 2 for r in results) / (len(results) - 1))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_min_order} std={std_dev} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_min_order} std={std_dev} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")