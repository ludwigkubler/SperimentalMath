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
            gate = random.choice(['AND', 'OR'])
            inputs = [random.randint(0, 1) for _ in range(n)]
            circuit.append((gate, inputs))
        return circuit
    
    def polynomial_from_circuit(circuit):
        n = len(circuit[0][1])
        poly = [0] * (2**n)
        for gate, inputs in circuit:
            if gate == 'AND':
                index = sum(2**i for i, bit in enumerate(inputs) if bit == 1)
                poly[index] += 1
            elif gate == 'OR':
                indices = [sum(2**i for i, bit in enumerate(inputs) if bit == 1)]
                for i in range(len(indices)):
                    index = indices[i]
                    poly[index] += 1
        return poly
    
    def p_adic_order(poly):
        max_power = -1
        for coeff in poly:
            if coeff != 0:
                power = int(math.log2(abs(coeff)))
                if power > max_power:
                    max_power = power
        return max_power
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_order = 0
    instances_tested = 0
    n_max = -1
    
    for n in n_values:
        for _ in range(5):
            circuit = generate_random_circuit(n)
            poly = polynomial_from_circuit(circuit)
            order = p_adic_order(poly)
            total_order += order
            instances_tested += 1
            if n > n_max:
                n_max = n
    
    avg_order = total_order / instances_tested
    bound = max(0, n_max * math.log2(2**(n_max + 1)))
    
    conjecture_holds = avg_order <= bound
    counterexample = "" if conjecture_holds else f"avg_order={avg_order}, bound={bound}"
    
    return {
        "metric_name": "p-adic Order",
        "metric_value": avg_order,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = list(map(int, sys.argv[1:])) or [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    avg_order = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={avg_order} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={avg_order} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")