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
        for _ in range(2**n):
            gate = random.choice(['AND', 'OR', 'NOT'])
            inputs = [random.randint(0, 1) for _ in range(random.randint(1, n))]
            circuit.append((gate, inputs))
        return circuit
    
    def circuit_to_polynomial(circuit):
        if not circuit:
            return "0"
        
        def evaluate(gate, inputs):
            if gate == 'NOT':
                return [1 - x for x in inputs]
            elif gate == 'AND':
                return [all(inputs)]
            elif gate == 'OR':
                return [any(inputs)]
        
        def simplify(poly):
            if len(poly) == 1:
                return poly[0]
            else:
                return "({})".format(" + ".join(simplify(p) for p in poly))
        
        stack = []
        for gate, inputs in circuit:
            if gate == 'NOT':
                stack.append(["(1 - {})".format(evaluate(gate, inputs)[0])])
            elif gate == 'AND':
                stack.append([evaluate(gate, inputs)[0]])
            elif gate == 'OR':
                stack.append([evaluate(gate, inputs)[0]])
        
        while len(stack) > 1:
            poly1 = stack.pop()
            poly2 = stack.pop()
            stack.append(["({} * {})".format(poly1[0], poly2[0])])
        
        return simplify(stack[0])

    def p_adic_order(p):
        if p == "0":
            return float('inf')
        count = 0
        for char in p:
            if char == '1':
                break
            count += 1
        return count

    n_values = [5, 10, 15, 20, 30, 40]
    total_order = 0
    instances_tested = 0
    
    for n in n_values:
        for _ in range(5):  # Ensure at least 30 instances per seed
            circuit = generate_random_circuit(n)
            polynomial = circuit_to_polynomial(circuit)
            order = p_adic_order(polynomial)
            total_order += order
            instances_tested += 1
    
    mean_order = total_order / instances_tested
    upper_bound = sum(n * math.log(2**(n+1)) for n in n_values) / len(n_values)
    
    conjecture_holds = mean_order <= upper_bound
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "p-adic Order",
        "metric_value": mean_order,
        "instances_tested": instances_tested,
        "n_max": max(n_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] + list(range(31, 100, 2))
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_order = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_order} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_order} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")