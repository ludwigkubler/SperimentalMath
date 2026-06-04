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
    
    def count_linear_regions(n, circuit):
        regions = set()
        for input_values in itertools.product([0, 1], repeat=n):
            output = evaluate_circuit(circuit, input_values)
            region = tuple(input_values + (output,))
            regions.add(region)
        return len(regions)
    
    def count_monomial_generators(n, circuit):
        # Placeholder function for counting monomial generators
        # This is a dummy implementation and should be replaced with actual logic
        return n
    
    n_values = [5, 10, 15, 20, 30, 40]
    G_n_sum = 0
    L_C_sum = 0
    instances_tested = 0
    
    for n in n_values:
        circuit = generate_boolean_circuit(n)
        input_values = [random.randint(0, 1) for _ in range(n)]
        output = evaluate_circuit(circuit, input_values)
        G_n = count_monomial_generators(n, circuit)
        L_C = count_linear_regions(n, circuit)
        
        if G_n is None or L_C is None:
            return {
                "metric_name": "G(n)/L(C)",
                "metric_value": float('nan'),
                "instances_tested": instances_tested,
                "n_max": n,
                "conjecture_holds": False,
                "counterexample": "mapping_undefined"
            }
        
        G_n_sum += G_n
        L_C_sum += L_C
        instances_tested += 1
    
    if instances_tested < 30:
        return {
            "metric_name": "G(n)/L(C)",
            "metric_value": float('nan'),
            "instances_tested": instances_tested,
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "not_enough_instances"
        }
    
    G_n_avg = G_n_sum / instances_tested
    L_C_avg = L_C_sum / instances_tested
    
    if abs(G_n_avg - L_C_avg) <= 0.1:
        return {
            "metric_name": "G(n)/L(C)",
            "metric_value": G_n_avg,
            "instances_tested": instances_tested,
            "n_max": max(n_values),
            "conjecture_holds": True,
            "counterexample": ""
        }
    else:
        return {
            "metric_name": "G(n)/L(C)",
            "metric_value": G_n_avg,
            "instances_tested": instances_tested,
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": f"G(n)={G_n_avg}, L(C)={L_C_avg}"
        }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    G_n_avg = sum(r["metric_value"] for r in results if not math.isnan(r["metric_value"])) / len(results)
    L_C_avg = sum(r["instances_tested"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.9:
        print(f"RESULT: SUPPORTED mean={G_n_avg} std={L_C_avg} support_fraction={support_fraction}")
    elif any(not math.isnan(r["metric_value"]) and abs(r["metric_value"] - G_n_avg) > 0.1 for r in results):
        first_failing_seed = next(i for i, r in enumerate(results) if not math.isnan(r["metric_value"]) and abs(r["metric_value"] - G_n_avg) > 0.1)
        print(f"RESULT: FALSIFIED counterexample=G(n)={G_n_avg} first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_support")