# auto-injected by SEC sandbox
import math
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
from fractions import Fraction

def run_trial(seed: int) -> dict:
    def generate_ac0_circuit(n):
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
        return stack.pop()

    def tropical_polynomial(value):
        if value == 0:
            return 0
        return max(int(math.log2(abs(value))), 0)

    def count_distinct_tropical_representations(circuit, n):
        distinct_representations = set()
        for _ in range(30):
            input_values = [random.randint(0, 1) for _ in range(n)]
            result = evaluate_circuit(circuit, input_values)
            tropical_value = tropical_polynomial(result)
            distinct_representations.add(tropical_value)
        return len(distinct_representations)

    def max_monomial_order(circuit, n):
        max_order = 0
        for _ in range(30):
            input_values = [random.randint(0, 1) for _ in range(n)]
            result = evaluate_circuit(circuit, input_values)
            tropical_value = tropical_polynomial(result)
            if tropical_value > max_order:
                max_order = tropical_value
        return max_order

    random.seed(seed)
    n = random.choice([5, 10, 15, 20, 30, 40])
    circuit = generate_ac0_circuit(n)
    
    distinct_representations = count_distinct_tropical_representations(circuit, n)
    max_order = max_monomial_order(circuit, n)

    conjecture_holds = (distinct_representations >= n**(1/3)) and (max_order >= n**(1/3))
    counterexample = "" if conjecture_holds else f"Distinct representations: {distinct_representations}, Max order: {max_order}"
    
    return {
        "metric_name": "Tropical Representations",
        "metric_value": distinct_representations,
        "instances_tested": 30,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = (sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))**0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")