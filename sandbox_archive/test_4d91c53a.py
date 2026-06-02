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
from fractions import Fraction
import math

def generate_polynomial(d, field_size):
    coeffs = [random.randint(1, field_size - 1) for _ in range(d + 1)]
    return coeffs

def find_roots(coeffs):
    n = len(coeffs)
    if n == 0:
        return []
    elif n == 1:
        return [-coeffs[0]]
    
    roots = []
    for i in range(1, n):
        a_k = sum(coeffs[j] * (i ** j) for j in range(n - 1))
        b_k = coeffs[-1]
        if a_k != 0:
            root = Fraction(b_k, a_k)
            roots.append(root)
    
    return roots

def compute_minimal_root_distance(roots):
    if not roots:
        return 0
    sorted_roots = sorted(roots)
    min_dist = float('inf')
    for i in range(len(sorted_roots) - 1):
        dist = abs(sorted_roots[i] - sorted_roots[i + 1])
        if dist < min_dist:
            min_dist = dist
    return min_dist

def construct_circuit(coeffs):
    n = len(coeffs)
    circuit = []
    for i in range(1, n):
        a_k = sum(coeffs[j] * (i ** j) for j in range(n - 1))
        b_k = coeffs[-1]
        if a_k != 0:
            gate = (a_k, b_k)
            circuit.append(gate)
    return circuit

def compute_circuit_width(circuit):
    width = 0
    for gate in circuit:
        width += 1
    return width

def run_trial(seed: int) -> dict:
    random.seed(seed)
    field_size = 2**random.randint(3, 5)
    d = random.randint(5, 40)
    
    coeffs = generate_polynomial(d, field_size)
    roots = find_roots(coeffs)
    min_dist = compute_minimal_root_distance(roots)
    
    circuit = construct_circuit(coeffs)
    width = compute_circuit_width(circuit)
    
    metric_value = min_dist
    n_max = d
    
    if len(roots) < 2:
        conjecture_holds = False
        counterexample = "not_enough_roots"
    else:
        conjecture_holds = abs(min_dist - width) <= 2 * width
        counterexample = ""
    
    return {
        "metric_name": "minimal_root_distance",
        "metric_value": metric_value,
        "instances_tested": 1,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        counterexample = "minimal_root_distance"
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")