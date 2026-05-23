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
            gate = random.choice(['AND', 'OR'])
            inputs = [random.randint(0, 1) for _ in range(2)]
            circuit.append((gate, inputs))
        return circuit
    
    def evaluate_circuit(circuit, input_values):
        stack = list(input_values)
        for gate, inputs in circuit:
            if gate == 'AND':
                result = stack[inputs[0]] and stack[inputs[1]]
            elif gate == 'OR':
                result = stack[inputs[0]] or stack[inputs[1]]
            stack.append(result)
        return stack[-1]
    
    def construct_quandle_group(circuit):
        quandle = {}
        for i in range(2**len(circuit)):
            input_values = [(i >> j) & 1 for j in range(len(circuit))]
            output_value = evaluate_circuit(circuit, input_values)
            if output_value not in quandle:
                quandle[output_value] = set()
            quandle[output_value].add(i)
        return quandle
    
    def minimal_order(quandle):
        orders = [len(values) for values in quandle.values() if len(values) > 1]
        return min(orders) if orders else float('inf')
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_min_order = 0
    instances_tested = 0
    
    for n in n_values:
        for _ in range(5):
            circuit = generate_monotone_xor_circuit(n)
            quandle = construct_quandle_group(circuit)
            min_order_val = minimal_order(quandle)
            if min_order_val == float('inf'):
                continue
            total_min_order += min_order_val
            instances_tested += 1
    
    mean_min_order = total_min_order / instances_tested
    std_dev = math.sqrt(sum((x - mean_min_order) ** 2 for x in range(instances_tested)) / (instances_tested - 1))
    
    conjecture_holds = mean_min_order <= n_values[-1] ** 2 * 1.1 and std_dev <= 0.1 * mean_min_order
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "Minimal Order of Quandle Group",
        "metric_value": mean_min_order,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [2**i - 1 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / (len(results) - 1))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")