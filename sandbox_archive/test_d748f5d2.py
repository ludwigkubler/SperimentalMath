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

def generate_random_circuit(n, m):
    if n <= 0 or m <= 0:
        return None
    circuit = []
    for _ in range(m):
        gate_type = random.randint(1, 3)  # 1: AND, 2: OR, 3: NOT
        if gate_type == 3:
            inputs = [random.randint(0, 1)]
        else:
            inputs = [random.randint(0, 1) for _ in range(gate_type - 1)]
        circuit.append((gate_type, inputs))
    return circuit

def evaluate_circuit(circuit):
    if not circuit:
        return None
    stack = []
    for gate_type, inputs in reversed(circuit):
        if gate_type == 3:  # NOT
            result = 1 - inputs[0]
        else:
            if len(inputs) != gate_type - 1:
                return None
            if gate_type == 1:  # AND
                result = all(inputs)
            elif gate_type == 2:  # OR
                result = any(inputs)
            else:
                return None
        stack.append(result)
    return stack.pop()

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    m_values = [n // 2 for n in n_values]
    
    results = []
    for n, m in zip(n_values, m_values):
        if n * m == 0:
            continue
        circuit = generate_random_circuit(n, m)
        if not circuit:
            continue
        result = evaluate_circuit(circuit)
        if result is None:
            continue
        results.append(result)
    
    if not results:
        return {
            "metric_name": "min_order",
            "metric_value": 0,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "empty_circuit"
        }
    
    min_order = len(results)
    expected_bound = Fraction(m ** (2/3) * n ** (1/3)).limit_denominator()
    support_fraction = sum(1 for result in results if abs(result - expected_bound) <= 2 * expected_bound / 3) / len(results)
    
    return {
        "metric_name": "min_order",
        "metric_value": min_order,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": support_fraction >= Fraction(9, 10),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if not results:
        print("RESULT: INCONCLUSIVE no_trials_run")
        sys.exit(0)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if support_fraction >= Fraction(9, 10):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        counterexample = "unknown"
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_support")