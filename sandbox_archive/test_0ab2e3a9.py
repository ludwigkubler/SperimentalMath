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

def generate_circuit(depth):
    if depth == 0:
        return ['input']
    else:
        sub_depth = random.randint(1, max(0, depth-1))
        left = generate_circuit(sub_depth)
        right = generate_circuit(sub_depth)
        gate = random.choice(['AND', 'OR'])
        return [gate, left, right]

def evaluate_circuit(circuit):
    if circuit[0] == 'input':
        return random.randint(0, 1)
    else:
        op = circuit[0]
        left = evaluate_circuit(circuit[1])
        right = evaluate_circuit(circuit[2])
        if op == 'AND':
            return left and right
        elif op == 'OR':
            return left or right

def frobenius_coincidence(circuit):
    values = set()
    for _ in range(100):  # Sample 100 random inputs
        input_values = [evaluate_circuit(sub_circuit) for sub_circuit in circuit]
        output_value = evaluate_circuit(circuit)
        values.add((tuple(input_values), output_value))
    return len(values)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    depth_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for depth in depth_values:
        n_max = max(n_max, depth)
        instances_tested += 1
        circuit = generate_circuit(depth)
        coincidence_rank = frobenius_coincidence(circuit)
        results.append(coincidence_rank)
    
    mean_value = sum(results) / len(results)
    std_value = math.sqrt(sum((x - mean_value) ** 2 for x in results) / len(results))
    
    return {
        "metric_name": "Frobenius Coincidence Rank",
        "metric_value": mean_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": False,  # Mapping undefined for this conjecture
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 7 for i in range(5, 30)]
    
    results = []
    instances_tested = 0
    n_max = 0
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result["metric_value"])
        instances_tested += trial_result["instances_tested"]
        n_max = max(n_max, trial_result["n_max"])
    
    mean_value = sum(results) / len(results)
    std_value = math.sqrt(sum((x - mean_value) ** 2 for x in results) / len(results))
    support_fraction = sum(1 for r in results if r <= 1.25 * n_max**2) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if r > 1.25 * n_max**2)
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")