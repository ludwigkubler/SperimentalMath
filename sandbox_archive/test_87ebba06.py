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
    
    def generate_boolean_circuit(n):
        # Generate a random Boolean circuit with n inputs
        circuit = []
        for _ in range(2**n):
            gate_type = random.choice(['AND', 'OR', 'NOT'])
            if gate_type == 'NOT':
                input_index = random.randint(0, len(circuit) - 1)
                circuit.append(('NOT', input_index))
            else:
                input_indices = [random.randint(0, len(circuit) - 1) for _ in range(2)]
                circuit.append((gate_type, input_indices[0], input_indices[1]))
        return circuit
    
    def evaluate_circuit(circuit, inputs):
        stack = []
        for gate in reversed(circuit):
            if gate[0] == 'NOT':
                stack.append(not stack[gate[1]])
            else:
                a = stack[gate[2]]
                b = stack[gate[1]]
                if gate[0] == 'AND':
                    stack.append(a and b)
                elif gate[0] == 'OR':
                    stack.append(a or b)
        return stack[0]
    
    def formal_power_series(circuit, n):
        # Compute the formal power series for the circuit
        series = [0] * (2**n)
        for i in range(2**n):
            inputs = [(i >> j) & 1 for j in range(n)]
            result = evaluate_circuit(circuit, inputs)
            series[i] = result
        return series
    
    def minimal_p_adic_order(series, p):
        # Compute the minimal p-adic order of the formal power series
        for i in range(1, len(series)):
            if all(x % p != 0 for x in series[:i]):
                return i
        return len(series)
    
    n = random.randint(5, 40)
    circuit = generate_boolean_circuit(n)
    series = formal_power_series(circuit, n)
    p_adic_order = minimal_p_adic_order(series, 2)
    
    metric_value = p_adic_order / math.log(n) ** 2
    conjecture_holds = metric_value <= 1
    counterexample = "" if conjecture_holds else "p-adic order exceeds f(n)"
    
    return {
        "metric_name": "minimal_p_adic_order",
        "metric_value": metric_value,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    if len(sys.argv) > 1:
        seeds = [int(s) for s in sys.argv[1:]]
    else:
        primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
        seeds = random.sample(primes, 30)
    
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
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")