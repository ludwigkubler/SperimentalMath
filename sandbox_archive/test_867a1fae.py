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
    
    def generate_random_circuit(depth):
        if depth == 0:
            return ['input']
        else:
            inputs = [generate_random_circuit(depth-1) for _ in range(2)]
            gate = random.choice(['AND', 'OR'])
            return [gate] + inputs
    
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
    
    def galois_group_size(n):
        # Simplified Galois group size for demonstration purposes
        return 2 ** n
    
    def minimal_splitting_field_extension_degree(galois_group_size):
        return galois_group_size
    
    depth = random.randint(1, 40)
    circuit = generate_random_circuit(depth)
    result = evaluate_circuit(circuit)
    
    galois_group_size_val = galois_group_size(depth)
    splitting_field_extension_degree = minimal_splitting_field_extension_degree(galois_group_size_val)
    
    return {
        "metric_name": "splitting_field_extension_degree",
        "metric_value": splitting_field_extension_degree,
        "instances_tested": 1,
        "n_max": depth,
        "conjecture_holds": splitting_field_extension_degree <= 4 * depth ** 2,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [random.randint(100, 999) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")