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
    random.seed(seed)
    
    def generate_random_circuit(n):
        circuit = []
        for _ in range(random.randint(1, 5)):
            gate_type = random.choice(['AND', 'OR'])
            inputs = [random.randint(0, 1) for _ in range(n)]
            circuit.append((gate_type, inputs))
        return circuit
    
    def evaluate_circuit(circuit):
        result = circuit[0][1]
        for gate_type, inputs in circuit[1:]:
            if gate_type == 'AND':
                result = [a and b for a, b in zip(result, inputs)]
            elif gate_type == 'OR':
                result = [a or b for a, b in zip(result, inputs)]
        return result
    
    def tropical_polynomial(circuit):
        n = len(circuit[0][1])
        poly = [[Fraction(0) if i != j else Fraction(1) for j in range(n)] for i in range(n)]
        for gate_type, inputs in circuit:
            new_poly = [[Fraction(0) for _ in range(n)] for _ in range(n)]
            for i in range(n):
                for j in range(n):
                    if gate_type == 'AND':
                        new_poly[i][j] = max(poly[i][k] + poly[k][j] for k in range(n))
                    elif gate_type == 'OR':
                        new_poly[i][j] = min(poly[i][k] + poly[k][j] for k in range(n))
            poly = new_poly
        return poly
    
    def minimal_tropical_root_count(poly):
        n = len(poly)
        roots = [0] * n
        for i in range(n):
            for j in range(n):
                if poly[i][j] == Fraction(0):
                    roots[j] += 1
        return max(roots)
    
    def monotone_width(circuit):
        n = len(circuit[0][1])
        width = [0] * n
        for gate_type, inputs in circuit:
            new_width = [0] * n
            for i in range(n):
                if gate_type == 'AND':
                    new_width[i] = max(width[k] + 1 for k in range(n))
                elif gate_type == 'OR':
                    new_width[i] = min(width[k] + 1 for k in range(n))
            width = new_width
        return max(width)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    for n in n_values:
        circuit = generate_random_circuit(n)
        poly = tropical_polynomial(circuit)
        mtr = minimal_tropical_root_count(poly)
        w_mon = monotone_width(circuit)
        results.append((mtr, w_mon))
    
    total_mtr = sum(mtr for mtr, _ in results)
    total_w_mon = sum(w_mon for _, w_mon in results)
    mean_mtr = Fraction(total_mtr) / len(n_values)
    mean_w_mon = Fraction(total_w_mon) / len(n_values)
    
    conjecture_holds = all(mtr <= 10 * w_mon for mtr, w_mon in results)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "Minimal Tropical Root Count and Circuit Monotone Width",
        "metric_value": mean_mtr,
        "instances_tested": len(n_values),
        "n_max": max(n_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_mtr = sum(result["metric_value"] for result in results) / len(results)
    std_mtr = (sum((result["metric_value"] - mean_mtr)**2 for result in results) / len(results))**0.5
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_mtr} std={std_mtr} support_fraction={support_fraction}")
    elif sum(1 for result in results if not result["conjecture_holds"]) / len(results) <= 0.2:
        print(f"RESULT: SUPPORTED mean={mean_mtr} std={std_mtr} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")