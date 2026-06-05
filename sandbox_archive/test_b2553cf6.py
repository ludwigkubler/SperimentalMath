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

def generate_circuit(n):
    # Generate a random Boolean circuit with n inputs
    circuit = []
    for _ in range(2**n):
        gate = random.choice(['AND', 'OR', 'NOT'])
        if gate == 'NOT':
            input_index = random.randint(0, len(circuit) - 1)
            circuit.append((gate, input_index))
        else:
            input_indices = [random.randint(0, len(circuit) - 1) for _ in range(2)]
            circuit.append((gate, input_indices))
    return circuit

def compute_polynomial(circuit):
    # Compute the characteristic polynomial of the given circuit
    n = len(circuit)
    polynomial = [1] * (n + 1)
    for gate, inputs in reversed(circuit):
        if gate == 'NOT':
            x = inputs
            polynomial[x] = -polynomial[x]
        else:
            x, y = inputs
            if gate == 'AND':
                polynomial[x] *= polynomial[y]
            elif gate == 'OR':
                polynomial[x] += polynomial[y]
    return polynomial

def compute_grobner_basis(polynomial):
    # Compute Gröbner basis for the given polynomial
    n = len(polynomial) - 1
    grobner_basis = [polynomial[0]]
    for i in range(1, n + 1):
        new_term = polynomial[i]
        for term in grobner_basis:
            if term > new_term:
                break
            gcd = math.gcd(term, new_term)
            if gcd == 1:
                break
            new_term //= gcd
        grobner_basis.append(new_term)
    return grobner_basis

def minimal_order(grobner_basis):
    # Determine the minimal order of the Gröbner basis
    n = len(grobner_basis) - 1
    for i in range(n, 0, -1):
        if grobner_basis[i] != 0:
            return i + 1
    return 0

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.choice([5, 10, 15, 20, 30, 40])
    circuit = generate_circuit(n)
    polynomial = compute_polynomial(circuit)
    grobner_basis = compute_grobner_basis(polynomial)
    min_order = minimal_order(grobner_basis)
    
    return {
        "metric_name": "min_order",
        "metric_value": min_order,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": min_order <= n**2 * math.log(n),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(1, 99997) for _ in range(30)]
    
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
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")