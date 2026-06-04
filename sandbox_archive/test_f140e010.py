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
    
    def generate_monotone_circuit(n, w):
        circuit = []
        for _ in range(w):
            gate = random.choice(['AND', 'OR'])
            inputs = [random.randint(0, 1) for _ in range(n)]
            circuit.append((gate, inputs))
        return circuit
    
    def compute_minimal_order(circuit):
        order = 0
        for gate, inputs in circuit:
            if gate == 'AND':
                order += sum(inputs)
            elif gate == 'OR':
                order += max(inputs)
        return order
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        for _ in range(5):
            circuit = generate_monotone_circuit(n, random.randint(1, min(40, n)))
            order = compute_minimal_order(circuit)
            results.append({"n": n, "order": order})
    
    mean_order = sum(result["order"] for result in results) / len(results)
    std_dev = math.sqrt(sum((result["order"] - mean_order) ** 2 for result in results) / len(results))
    
    conjecture_holds = all(abs(order - (n // 2) ** 2) <= 10 for n, order in zip(n_values, [result["order"] for result in results]))
    counterexample = "" if conjecture_holds else f"order={max([result['order'] for result in results])} exceeds expected O(w(C)^2)"
    
    return {
        "metric_name": "minimal_order",
        "metric_value": mean_order,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    std_dev_metric_value = math.sqrt(sum((result["metric_value"] - mean_metric_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_dev_metric_value} support_fraction={support_fraction}")
    elif any(abs(result["metric_value"] - (n // 2) ** 2) > 10 for n, result in zip(n_values, results)):
        first_failing_seed = next(seed for seed, result in enumerate(results, start=1) if abs(result["metric_value"] - (n_values[result["instances_tested"] - 1] // 2) ** 2) > 10)
        print(f"RESULT: FALSIFIED counterexample='order exceeds expected O(w(C)^2)' first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction}")