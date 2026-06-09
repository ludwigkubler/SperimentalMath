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
        for _ in range(2**n):
            gate = random.choice(['AND', 'OR'])
            inputs = [random.randint(0, 1) for _ in range(n)]
            circuit.append((gate, inputs))
        return circuit
    
    def quaternionic_degree(circuit):
        # Simplified mapping to a degree based on the number of gates
        return len(circuit)
    
    def communication_complexity_rank_variance(circuit):
        # Simplified mapping to a variance based on the number of inputs
        return len(set(input for _, input in circuit)) / len(circuit)
    
    n_values = [5, 10, 15, 20, 30, 40]
    metrics = []
    instances_tested = 0
    
    for n in n_values:
        for _ in range(5):  # Ensure at least 30 instances per seed
            circuit = generate_boolean_circuit(n)
            degree = quaternionic_degree(circuit)
            variance = communication_complexity_rank_variance(circuit)
            metrics.append((degree, variance))
            instances_tested += 1
    
    if not metrics:
        return {
            "metric_name": "correlation",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    correlation = sum((x - mean_x) * (y - mean_y) for x, y in metrics) / len(metrics)
    mean_x = sum(x for x, _ in metrics) / len(metrics)
    mean_y = sum(y for _, y in metrics) / len(metrics)
    
    return {
        "metric_name": "correlation",
        "metric_value": correlation,
        "instances_tested": instances_tested,
        "n_max": max(n_values),
        "conjecture_holds": abs(correlation) >= 0.7,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(res["metric_value"] for res in results if res["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((res["metric_value"] - mean_value)**2 for res in results if res["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        for res in results:
            if not res["conjecture_holds"]:
                print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={res['seed']}")
                break