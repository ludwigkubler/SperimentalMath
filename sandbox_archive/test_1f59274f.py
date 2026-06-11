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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_boolean_circuit(n, d):
        if n == 1:
            return ['0', '1']
        else:
            inputs = generate_boolean_circuit(n // 2, d - 1)
            outputs = []
            for i in range(len(inputs)):
                if random.randint(0, 1) == 0:
                    outputs.append('AND')
                else:
                    outputs.append('OR')
            return [f'({inputs[i]} {outputs[i]} {inputs[i + len(inputs)//2]})' for i in range(len(inputs))]
    
    def evaluate_circuit(circuit):
        if isinstance(circuit, str):
            if circuit == '0':
                return 0
            elif circuit == '1':
                return 1
            else:
                left, op, right = circuit.split()
                if op == 'AND':
                    return evaluate_circuit(left) * evaluate_circuit(right)
                elif op == 'OR':
                    return evaluate_circuit(left) + evaluate_circuit(right) - evaluate_circuit(left) * evaluate_circuit(right)
        else:
            return sum(evaluate_circuit(subcircuit) for subcircuit in circuit)
    
    def hodge_de_rham_dimension(circuit):
        # Simplified version of Hodge-De Rham dimension calculation
        return len(set(evaluate_circuit(circuit)))
    
    def entanglement_complexity(n, d):
        # Simplified version of entanglement complexity calculation
        return n * d
    
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):  # Sample 5 instances per size
            circuit = generate_boolean_circuit(n, random.randint(1, 4))
            hdim = hodge_de_rham_dimension(circuit)
            e_phi = entanglement_complexity(n, len(circuit.split()))
            results.append((hdim, e_phi))
    
    if not results:
        return {
            "metric_name": "Pearson correlation coefficient",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "No instances generated"
        }
    
    hdims = [r[0] for r in results]
    e_phis = [r[1] for r in results]
    
    n = len(hdims)
    mean_hdim = sum(hdims) / n
    mean_e_phi = sum(e_phis) / n
    
    covariance = sum((hdims[i] - mean_hdim) * (e_phis[i] - mean_e_phi) for i in range(n)) / n
    variance_hdim = sum((hdims[i] - mean_hdim) ** 2 for i in range(n)) / n
    variance_e_phi = sum((e_phis[i] - mean_e_phi) ** 2 for i in range(n)) / n
    
    pearson_corr = covariance / (math.sqrt(variance_hdim) * math.sqrt(variance_e_phi))
    
    return {
        "metric_name": "Pearson correlation coefficient",
        "metric_value": pearson_corr,
        "instances_tested": len(results),
        "n_max": max(n for n, _ in results),
        "conjecture_holds": pearson_corr >= 0.8 and pearson_corr <= -0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 7 for i in range(5, 35)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"n_max\": {result['n_max']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    if all(r["conjecture_holds"] for r in results):
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
        support_fraction = len([r for r in results if r["conjecture_holds"]]) / len(results)
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(r["metric_value"] < 0.5 or r["metric_value"] > -0.8 for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Pearson correlation coefficient out of bounds\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient evidence")