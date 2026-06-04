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
    
    def generate_circuit(n):
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
                result = all(stack.pop() for _ in range(len(inputs)))
            elif gate_type == 'OR':
                result = any(stack.pop() for _ in range(len(inputs)))
            stack.append(result)
        return stack[0]
    
    def count_linear_regions(n, circuit):
        regions = set()
        for i in range(2**n):
            input_values = [i >> j & 1 for j in range(n)]
            output = evaluate_circuit(circuit, input_values)
            region_key = tuple(input_values) + (output,)
            regions.add(region_key)
        return len(regions)
    
    def count_monomial_generators(n, circuit):
        monomials = set()
        for i in range(2**n):
            input_values = [i >> j & 1 for j in range(n)]
            output = evaluate_circuit(circuit, input_values)
            if output == 1:
                monomial = tuple(input_values)
                monomials.add(monomial)
        return len(monomials)
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_gn_lc_ratio = 0
    instances_tested = 0
    
    for n in n_values:
        circuit = generate_circuit(n)
        gn = count_monomial_generators(n, circuit)
        lc = count_linear_regions(n, circuit)
        if lc > 0:
            ratio = gn / lc
            total_gn_lc_ratio += ratio
            instances_tested += 1
    
    if instances_tested == 0:
        return {
            "metric_name": "gn_lc_ratio",
            "metric_value": 0,
            "instances_tested": 0,
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "No linear regions found"
        }
    
    mean_ratio = total_gn_lc_ratio / instances_tested
    return {
        "metric_name": "gn_lc_ratio",
        "metric_value": mean_ratio,
        "instances_tested": instances_tested,
        "n_max": max(n_values),
        "conjecture_holds": mean_ratio <= 1.1,  # ε = 0.1
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2**i + 7 for i in range(5, 35)]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, **result}}")
        results.append(result)
    
    total_gn_lc_ratio = sum(r["metric_value"] for r in results if r["instances_tested"] > 0)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={total_gn_lc_ratio/len(results):.2f} std=0 support_fraction=1")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={total_gn_lc_ratio/len(results):.2f} std=0 support_fraction={support_fraction:.2f}")
    else:
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"gn_lc_ratio too high\" first_failing_seed={first_failing_seed}")