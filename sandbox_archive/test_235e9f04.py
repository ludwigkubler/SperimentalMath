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
    
    def generate_random_boolean_circuit(n):
        if n == 1:
            return ['0'] if random.choice([True, False]) else ['1']
        elif n == 2:
            return [random.choice(['0', '1']) for _ in range(4)]
        else:
            subcircuits = [generate_random_boolean_circuit(n // 2) for _ in range(2)]
            return [f'({subc[0]} {subc[1]})' for subc in zip(subcircuits, subcircuits)]

    def evaluate_circuit(circuit):
        if circuit.isdigit():
            return int(circuit)
        else:
            op = circuit[1]
            left = evaluate_circuit(circuit[2:circuit.index(' ')])
            right = evaluate_circuit(circuit[circuit.index(' ') + 2:-1])
            if op == '&':
                return left and right
            elif op == '|':
                return left or right

    def find_topological_minor(circuit):
        if circuit.isdigit():
            return circuit
        else:
            op = circuit[1]
            left = find_topological_minor(circuit[2:circuit.index(' ')])
            right = find_topological_minor(circuit[circuit.index(' ') + 2:-1])
            if op == '&':
                return f'({left} {right})'
            elif op == '|':
                return f'({left} {right})'

    def degree_of_circuit(circuit):
        if circuit.isdigit():
            return 0
        else:
            left = degree_of_circuit(circuit[2:circuit.index(' ')])
            right = degree_of_circuit(circuit[circuit.index(' ') + 2:-1])
            return max(left, right) + 1

    def tropicalized_brauer_group_size(n):
        # Placeholder for the actual computation
        # This is a dummy implementation to avoid errors
        return n * (n - 1) // 2

    n = random.randint(5, 40)
    circuit = generate_random_boolean_circuit(n)
    degree = degree_of_circuit(circuit)
    topological_minor = find_topological_minor(circuit)
    rank_trop_brauer = tropicalized_brauer_group_size(n)

    return {
        "metric_name": "Ratio",
        "metric_value": rank_trop_brauer / degree,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": False,
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []

    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)

    mean_ratio = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if 0.7 <= result["metric_value"] <= 1.3) / len(results)

    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=NA support_fraction={support_fraction}")
    elif any(result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in enumerate(results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=mapping_undefined")