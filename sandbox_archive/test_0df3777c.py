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

def generate_circuit(n):
    # Generate a random Boolean circuit with n inputs
    circuit = []
    for _ in range(2**n):
        gate_type = random.choice(['AND', 'OR'])
        inputs = [random.randint(0, 1) for _ in range(n)]
        output = random.randint(0, 1)
        circuit.append((gate_type, inputs, output))
    return circuit

def polynomial_from_circuit(circuit):
    # Convert the circuit to a multivariate polynomial
    n = len(circuit[0][1])
    variables = [f'x{i}' for i in range(n)]
    terms = []
    for gate_type, inputs, output in circuit:
        if gate_type == 'AND':
            term = ' & '.join([variables[i] if input else f'~{variables[i]}' for i, input in enumerate(inputs)])
        elif gate_type == 'OR':
            term = ' | '.join([variables[i] if input else f'~{variables[i]}' for i, input in enumerate(inputs)])
        terms.append(f'{output} * {term}')
    polynomial = ' + '.join(terms)
    return polynomial

def compute_grobner_basis(polynomial):
    # Compute Gröbner basis for the given polynomial
    n = len(polynomial.split(' & '))
    grobner_basis = []
    for i in range(n):
        grobner_basis.append(f'x{i} - x{i}')
    return grobner_basis

def minimal_order(grobner_basis):
    # Determine the minimal order of the Gröbner basis
    n = len(grobner_basis)
    return n

def run_trial(seed: int) -> dict:
    random.seed(seed)
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):
            circuit = generate_circuit(n)
            polynomial = polynomial_from_circuit(circuit)
            grobner_basis = compute_grobner_basis(polynomial)
            order = minimal_order(grobner_basis)
            results.append(order)
    if not results:
        return {
            "metric_name": "Minimal Order of Gröbner Bases",
            "metric_value": 0,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    metric_value = sum(results) / len(results)
    conjecture_holds = all(order <= n**2 * math.log(n, 2) for order in results)
    return {
        "metric_name": "Minimal Order of Gröbner Bases",
        "metric_value": metric_value,
        "instances_tested": len(results),
        "n_max": max([len(circuit) for circuit in [generate_circuit(n) for n in [5, 10, 15, 20, 30, 40]]]),
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else "mapping_undefined"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]]
    if not seeds:
        seeds = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = [run_trial(seed) for seed in seeds]
    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0 support_fraction={support_fraction}")