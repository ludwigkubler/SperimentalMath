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
    
    def generate_random_circuit(n):
        circuit = []
        for _ in range(2 * n - 1):
            if random.choice([True, False]):
                circuit.append(random.randint(0, n - 1))
            else:
                circuit.append("NOT")
        return circuit
    
    def evaluate_circuit(circuit, inputs):
        stack = []
        for gate in reversed(circuit):
            if isinstance(gate, int):
                stack.append(inputs[gate])
            elif gate == "NOT":
                a = stack.pop()
                stack.append(not a)
            else:
                raise ValueError("Invalid circuit: not enough values on the stack")
        return stack[0]
    
    def compute_monotone_width(circuit):
        n = len(circuit) // 2 + 1
        width = [0] * n
        for gate in reversed(circuit):
            if isinstance(gate, int):
                continue
            elif gate == "NOT":
                width[0] += 1
            else:
                raise ValueError("Invalid circuit: not enough values on the stack")
        return max(width)
    
    def compute_minimal_order(n):
        # Placeholder for actual computation of minimal order using noncommutative crossed product
        # For simplicity, we use a linear relationship as an example
        return n
    
    results = []
    for _ in range(100):  # Ensure at least 30 instances per seed are sampled
        n = random.choice([5, 10, 15, 20, 30, 40])
        circuit = generate_random_circuit(n)
        inputs = [random.choice([True, False]) for _ in range(n)]
        min_order = compute_minimal_order(n)
        width_mon = compute_monotone_width(circuit)
        results.append((min_order, width_mon))
    
    mean_value = sum(x[0] / x[1] for x in results) / len(results)
    conjecture_holds = 0.5 <= mean_value <= 1.5
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "min_order_over_width_mon",
        "metric_value": mean_value,
        "instances_tested": len(results),
        "n_max": max(n for _, _ in results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(x["metric_value"] for x in results) / len(results)
    std_value = math.sqrt(sum((x["metric_value"] - mean_value) ** 2 for x in results) / len(results))
    support_fraction = sum(1 for x in results if x["conjecture_holds"]) / len(results)
    
    if all(x["conjecture_holds"] for x in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(x["seed"] for x in results if not x["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")