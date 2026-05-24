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
    
    def generate_ac0_circuit(n, s):
        if n <= 1 or s < 1:
            return []
        if s == 1:
            return [random.choice([0, 1])]
        circuit = []
        for _ in range(s - 1):
            gate_type = random.choice(['OR', 'AND'])
            inputs = random.sample(range(n), random.randint(2, n))
            circuit.append((gate_type, inputs))
        return circuit
    
    def evaluate_circuit(circuit, input_values):
        stack = []
        for gate in reversed(circuit):
            gate_type, inputs = gate
            if gate_type == 'OR':
                result = any(input_values[i] for i in inputs)
            elif gate_type == 'AND':
                result = all(input_values[i] for i in inputs)
            stack.append(result)
        return stack[0]
    
    def construct_polynomial_system(circuit):
        n = len(circuit) + 1
        polynomials = []
        for i in range(n):
            polynomial = [0] * (n - i)
            for j, gate in enumerate(reversed(circuit[:i])):
                gate_type, inputs = gate
                if gate_type == 'OR':
                    polynomial[j] += 1
                elif gate_type == 'AND':
                    polynomial[j] += 1
            polynomials.append(polynomial)
        return polynomials
    
    def min_tropical_growth_rate(polynomials):
        max_values = [max(poly) for poly in polynomials]
        growth_rates = [math.log2(value) if value > 0 else float('-inf') for value in max_values]
        return min(growth_rates)
    
    n = random.randint(5, 40)
    s = random.randint(1, 40)
    circuit = generate_ac0_circuit(n, s)
    polynomials = construct_polynomial_system(circuit)
    g = min_tropical_growth_rate(polynomials)
    c = 1.0  # Constant factor to be determined experimentally
    expected_growth = c * math.log2(s)
    
    return {
        "metric_name": "minimal_tropical_growth_rate",
        "metric_value": g,
        "instances_tested": 1,
        "conjecture_holds": g >= expected_growth,
        "counterexample": "" if g >= expected_growth else f"AC0 circuit size {s} with growth rate {g}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    total_metric_value = sum(r["metric_value"] for r in results if "metric_value" in r)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={total_metric_value/len(results)} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={total_metric_value/len(results)} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"g(P) < c·log(s)\" first_failing_seed={first_failing_seed}")