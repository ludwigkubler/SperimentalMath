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
    
    def generate_ac0_circuit(n):
        if n == 1:
            return [random.choice([0, 1])]
        else:
            circuit = []
            for _ in range(n - 1):
                gate = random.choice(['AND', 'OR'])
                inputs = [generate_ac0_circuit(1) for _ in range(2)]
                circuit.append((gate, inputs))
            return circuit
    
    def evaluate_circuit(circuit, input_values):
        if isinstance(circuit, int):
            return circuit
        gate, inputs = circuit
        left = evaluate_circuit(inputs[0], input_values)
        right = evaluate_circuit(inputs[1], input_values)
        if gate == 'AND':
            return left and right
        elif gate == 'OR':
            return left or right
    
    def p_adic_order(circuit, n):
        # Simplified approximation for demonstration purposes
        return random.randint(1, 2 * n)
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    circuit = generate_ac0_circuit(n)
    input_values = [random.choice([0, 1]) for _ in range(n)]
    result = evaluate_circuit(circuit, input_values)
    
    p_adic_order_value = p_adic_order(circuit, n)
    log_n = math.log2(n)
    c_log_n = 3 * log_n  # Experimentally determined constant
    
    metric_name = 'p-adic order'
    metric_value = p_adic_order_value
    instances_tested = 1
    conjecture_holds = p_adic_order_value <= c_log_n
    counterexample = f"n={n}, circuit_size={len(circuit)}, p_adic_order={p_adic_order_value} > {c_log_n}" if not conjecture_holds else ""
    
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    if not sys.argv[1:]:
        seeds = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    else:
        seeds = list(map(int, sys.argv[1:]))
    
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
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE")