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
        for _ in range(2**n):
            gate = random.choice(['AND', 'OR'])
            inputs = [random.randint(0, 1) for _ in range(n)]
            circuit.append((gate, inputs))
        return circuit
    
    def polynomial_representation(circuit):
        n = len(circuit[0][1])
        poly = [[0] * (2**n) for _ in range(2**n)]
        for gate, inputs in circuit:
            if gate == 'AND':
                for i in range(2**n):
                    if all(inputs[j] == 1 for j in range(n)):
                        poly[i][i] = 1
            elif gate == 'OR':
                for i in range(2**n):
                    if any(inputs[j] == 1 for j in range(n)):
                        poly[i][i] = 1
        return poly
    
    def frobenius_norm(poly):
        n = len(poly)
        norm = 0
        for i in range(n):
            for j in range(n):
                norm += poly[i][j]**2
        return math.sqrt(norm)
    
    def monotone_width(circuit):
        n = len(circuit[0][1])
        width = 0
        for _ in range(100):  # Sample 100 random assignments
            assignment = [random.randint(0, 1) for _ in range(n)]
            active_gates = set()
            for gate, inputs in circuit:
                if all(assignment[i] == inputs[j] for j, i in enumerate(inputs)):
                    active_gates.add(gate)
            width = max(width, len(active_gates))
        return width
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        for _ in range(5):  # Test each n 5 times
            circuit = generate_circuit(n)
            poly = polynomial_representation(circuit)
            norm = frobenius_norm(poly)
            width = monotone_width(circuit)
            results.append((norm, width))
    
    if not results:
        return {
            "metric_name": "Frobenius Norm vs Monotone Width",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    norms = [r[0] for r in results]
    widths = [r[1] for r in results]
    correlation = sum(norm * width for norm, width in zip(norms, widths)) / (sum(norm**2 for norm in norms) * sum(width**2 for width in widths))
    
    return {
        "metric_name": "Frobenius Norm vs Monotone Width",
        "metric_value": correlation,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": correlation >= 0.8,
        "counterexample": "" if correlation >= 0.8 else "correlation < 0.5"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all(r["conjecture_holds"] for r in results):
        mean_corr = sum(r["metric_value"] for r in results) / len(results)
        support_fraction = 1.0
        result = f"RESULT: SUPPORTED mean={mean_corr} std=0 support_fraction={support_fraction}"
    else:
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        result = f"RESULT: FALSIFIED counterexample='correlation < 0.5' first_failing_seed={first_failing_seed}"
    
    print(result)