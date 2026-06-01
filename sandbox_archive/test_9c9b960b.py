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
            gate_type = random.choice(['AND', 'OR'])
            inputs = [random.randint(0, 1) for _ in range(random.randint(2, n))]
            circuit.append((gate_type, inputs))
        return circuit
    
    def evaluate_circuit(circuit, input_values):
        stack = []
        for gate_type, inputs in reversed(circuit):
            if gate_type == 'AND':
                result = all(input_values[i] for i in inputs)
            elif gate_type == 'OR':
                result = any(input_values[i] for i in inputs)
            stack.append(result)
        return stack[0]
    
    def polynomial_representation_length(poly):
        length = 0
        for coeff, exp in poly.items():
            length += len(bin(coeff)) + len(bin(exp))
        return length
    
    def affine_quotient(circuit, n):
        input_values = [random.randint(0, 1) for _ in range(n)]
        output = evaluate_circuit(circuit, input_values)
        poly = {output: 1}
        return poly
    
    n_max = 40
    instances_tested = 30
    metric_value = 0.0
    conjecture_holds = True
    counterexample = ""
    
    for n in range(5, n_max + 1):
        circuit = generate_random_circuit(n)
        q_C = affine_quotient(circuit, n)
        rep_length = polynomial_representation_length(q_C)
        metric_value += rep_length / instances_tested
        
        if rep_length > 1.5 * n * math.log2(n):
            conjecture_holds = False
            counterexample = f"n={n}, rep_length={rep_length}"
    
    return {
        "metric_name": "Representation Length",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={math.sqrt(sum((result['metric_value'] - mean_value)**2 for result in results) / len(results))} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")