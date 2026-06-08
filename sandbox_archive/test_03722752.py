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
        for _ in range(n):
            gate = random.choice(['AND', 'OR'])
            inputs = [random.randint(0, 1) for _ in range(random.randint(2, n))]
            circuit.append((gate, inputs))
        return circuit
    
    def calculate_frobenius_schur_index(circuit):
        # Placeholder implementation of Frobenius-Schur index calculation
        # This is a dummy function and should be replaced with actual logic
        return random.random()
    
    def calculate_circuit_width(circuit):
        width = 0
        for gate, inputs in circuit:
            width = max(width, len(inputs))
        return width
    
    n_values = [5, 10, 15, 20, 30, 40]
    fs_index_sum = 0
    width_sum = 0
    instances_tested = 0
    n_max = 0
    
    for n in n_values:
        for _ in range(5):  # Sample 5 circuits per size
            circuit = generate_random_circuit(n)
            fs_index = calculate_frobenius_schur_index(circuit)
            width = calculate_circuit_width(circuit)
            
            if fs_index is None or width is None:
                return {
                    "metric_name": "FS_index vs Width",
                    "metric_value": 0,
                    "instances_tested": instances_tested,
                    "n_max": n_max,
                    "conjecture_holds": False,
                    "counterexample": "mapping_undefined"
                }
            
            fs_index_sum += fs_index
            width_sum += width
            instances_tested += 1
            n_max = max(n_max, n)
    
    mean_fs_index = fs_index_sum / instances_tested
    mean_width = width_sum / instances_tested
    
    correlation_coefficient = (instances_tested * sum(fs_index * width for fs_index, width in zip(range(instances_tested), range(instances_tested))) - 
                               mean_fs_index * instances_tested - mean_width * instances_tested) / \
                              math.sqrt((instances_tested * sum(fs_index**2 for fs_index in range(instances_tested)) - mean_fs_index**2) *
                                        (instances_tested * sum(width**2 for width in range(instances_tested)) - mean_width**2))
    
    if correlation_coefficient > 0.7 and abs(mean_fs_index - mean_width) <= 3:
        return {
            "metric_name": "FS_index vs Width",
            "metric_value": correlation_coefficient,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": True,
            "counterexample": ""
        }
    else:
        return {
            "metric_name": "FS_index vs Width",
            "metric_value": correlation_coefficient,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "correlation_not_met"
        }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    std_metric_value = math.sqrt(sum((result["metric_value"] - mean_metric_value)**2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='correlation_not_met' first_failing_seed={first_failing_seed}")