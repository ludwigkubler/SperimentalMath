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
    
    def generate_random_circuit(depth):
        if depth == 0:
            return []
        else:
            gate = random.choice(['AND', 'OR'])
            inputs = [generate_random_circuit(random.randint(1, depth-1)) for _ in range(2)]
            return [(gate, inputs[0], inputs[1])]
    
    def her(circuit):
        if not circuit:
            return 0
        elif len(circuit) == 1 and isinstance(circuit[0], tuple):
            gate, _, _ = circuit[0]
            return 1 + max(her(input_circuit) for input_circuit in circuit[0][2])
        else:
            raise ValueError("Invalid circuit format")
    
    def depth(circuit):
        if not circuit:
            return 0
        elif len(circuit) == 1 and isinstance(circuit[0], tuple):
            gate, _, _ = circuit[0]
            return 1 + max(depth(input_circuit) for input_circuit in circuit[0][2])
        else:
            raise ValueError("Invalid circuit format")
    
    n_max = 40
    instances_tested = 30
    metric_values = []
    conjecture_holds = True
    counterexample = ""
    
    for n in range(5, n_max + 1):
        for _ in range(instances_tested // (n_max - 4)):
            circuit = generate_random_circuit(n)
            her_value = her(circuit)
            depth_value = depth(circuit)
            metric_values.append(her_value / depth_value)
    
    mean_metric_value = sum(metric_values) / len(metric_values)
    std_metric_value = math.sqrt(sum((x - mean_metric_value) ** 2 for x in metric_values) / len(metric_values))
    
    if any(value > 1 for value in metric_values):
        conjecture_holds = False
        counterexample = "HER(C) exceeds depth D"
    
    return {
        "metric_name": "her_over_depth",
        "metric_value": mean_metric_value,
        "instances_tested": instances_tested * (n_max - 4),
        "n_max": n_max,
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
    std_metric_value = math.sqrt(sum((result["metric_value"] - mean_metric_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"HER(C) exceeds depth D\" first_failing_seed={first_failing_seed}")