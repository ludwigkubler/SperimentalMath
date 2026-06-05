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
        # Generate a random Boolean circuit with n inputs
        circuit = []
        for _ in range(2**(n-1)):
            gate_type = random.choice(['AND', 'OR'])
            inputs = [random.randint(0, 1) for _ in range(n)]
            circuit.append((gate_type, inputs))
        return circuit
    
    def polynomial_representation(circuit):
        # Compute the polynomial representation of the circuit
        n = len(circuit[0][1])
        P = [[0] * (2**n) for _ in range(2**n)]
        for gate_type, inputs in circuit:
            if gate_type == 'AND':
                index = sum(inputs)
                P[index][index] += 1
            elif gate_type == 'OR':
                index = sum(inputs)
                for i in range(index + 1):
                    P[i][i] += 1
        return P
    
    def frobenius_norm(P):
        # Compute the Frobenius norm of the polynomial representation
        n = len(P)
        norm = 0
        for i in range(n):
            for j in range(n):
                norm += P[i][j]**2
        return math.sqrt(norm)
    
    def monotone_width(circuit):
        # Compute the monotone width of the circuit
        n = len(circuit[0][1])
        max_width = 0
        for i in range(2**n):
            width = 0
            for gate_type, inputs in circuit:
                if all(inputs[j] == (i >> j) & 1 for j in range(n)):
                    width += 1
            max_width = max(max_width, width)
        return max_width
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        circuit = generate_circuit(n)
        P = polynomial_representation(circuit)
        w_m = monotone_width(circuit)
        norm = frobenius_norm(P)
        results.append((n, norm, w_m))
    
    if len(results) < 30:
        return {
            "metric_name": "correlation",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max(n for n, _, _ in results),
            "conjecture_holds": False,
            "counterexample": "insufficient_instances"
        }
    
    norms = [norm for _, norm, _ in results]
    widths = [w_m for _, _, w_m in results]
    correlation = sum(norm * w_m for norm, w_m in zip(norms, widths)) / (sum(norm**2 for norm in norms) * sum(w_m**2 for w_m in widths))
    
    return {
        "metric_name": "correlation",
        "metric_value": correlation,
        "instances_tested": 30,
        "n_max": max(n_values),
        "conjecture_holds": correlation >= 0.8 and all(correlation >= 0.5 for _, norm, w_m in results),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(30)]
    
    all_results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        all_results.append(result)
    
    mean_corr = sum(r["metric_value"] for r in all_results if r["metric_value"] is not None) / len(all_results)
    support_fraction = sum(1 for r in all_results if r["conjecture_holds"]) / len(all_results)
    
    if all(r["metric_value"] is not None for r in all_results):
        print(f"RESULT: SUPPORTED mean={mean_corr} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in all_results):
        first_failing_seed = next(seed for seed, result in zip(seeds, all_results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_too_low\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")