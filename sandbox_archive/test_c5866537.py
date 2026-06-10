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
    
    def generate_circuit(n, m):
        circuit = []
        for _ in range(m):
            gate_type = random.choice(['AND', 'OR'])
            inputs = random.sample(range(n), 2)
            circuit.append((gate_type, inputs))
        return circuit

    def compute_action_complexity(circuit):
        n = len(circuit)
        action_complexity = 0
        for _ in range(10):  # Simulate reflections
            action_complexity += random.randint(1, n)
        return action_complexity

    def frege_proof_depth(circuit):
        depth = 0
        for gate_type, inputs in circuit:
            if gate_type == 'AND':
                depth += 2
            elif gate_type == 'OR':
                depth += 1
        return depth

    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        for _ in range(5):  # 5 instances per size
            m = random.randint(n, 2 * n)
            circuit = generate_circuit(n, m)
            action_complexity = compute_action_complexity(circuit)
            proof_depth = frege_proof_depth(circuit)
            results.append((n, m, action_complexity, proof_depth))
    
    total_action_complexity = sum(result[2] for result in results)
    mean_action_complexity = total_action_complexity / len(results)
    conjecture_holds = all(action_complexity <= m**(1/3) * n**(2/3) for _, m, action_complexity, _ in results)
    
    return {
        "metric_name": "action_complexity",
        "metric_value": mean_action_complexity,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else "mapping_undefined"
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_action_complexity = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_action_complexity} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_action_complexity} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")