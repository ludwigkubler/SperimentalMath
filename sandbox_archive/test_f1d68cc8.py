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
    for _ in range(n):
        gate_type = random.choice(['AND', 'OR'])
        if gate_type == 'AND':
            inputs = [random.randint(0, 1) for _ in range(random.randint(2, n))]
        else:
            inputs = [random.randint(0, 1) for _ in range(random.randint(2, n))]
        circuit.append((gate_type, inputs))
    return circuit

def compute_polynomial(circuit):
    # Compute the characteristic polynomial of the given circuit
    n = len(circuit)
    poly = {}
    for i in range(n):
        if circuit[i][0] == 'AND':
            inputs = circuit[i][1]
            coeff = 1
            for inp in inputs:
                coeff *= (-inp)
            poly[tuple(sorted(inputs))] = coeff
        else:
            inputs = circuit[i][1]
            coeff = -1
            for inp in inputs:
                coeff *= (1 - inp)
            poly[tuple(sorted(inputs))] = coeff
    return poly

def compute_grobner_basis(polynomial):
    # Compute Gröbner basis for the given polynomial
    basis = list(polynomial.items())
    while True:
        changed = False
        for i in range(len(basis)):
            for j in range(i + 1, len(basis)):
                if basis[i][0] > basis[j][0]:
                    basis[i], basis[j] = basis[j], basis[i]
                elif basis[i][0] == basis[j][0]:
                    lcm = 1
                    for k in range(len(basis[i][0])):
                        lcm *= math.lcm(basis[i][0][k], basis[j][0][k])
                    if lcm > basis[i][0]:
                        changed = True
                        new_basis = []
                        for term, coeff in basis:
                            if term != basis[i][0] and term != basis[j][0]:
                                new_basis.append((term, coeff))
                        new_basis.append((lcm, 1))
                        basis = new_basis
        if not changed:
            break
    return basis

def minimal_order(grobner_basis):
    # Determine the minimal order of the Gröbner basis
    orders = [len(term) for term, _ in grobner_basis]
    return max(orders)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_max = 40
    instances_tested = 0
    total_metric_value = 0.0
    conjecture_holds = True
    counterexample = ""

    for n in range(5, n_max + 1):
        circuit = generate_circuit(n)
        polynomial = compute_polynomial(circuit)
        grobner_basis = compute_grobner_basis(polynomial)
        order = minimal_order(grobner_basis)

        instances_tested += 1
        total_metric_value += order

        if order > n**2 * math.log(n):
            conjecture_holds = False
            counterexample = f"Circuit with {n} inputs has Gröbner basis of order {order}, which exceeds O({n}^2 log {n})"

    return {
        "metric_name": "Minimal Order of Gröbner Bases",
        "metric_value": total_metric_value / instances_tested,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [3, 5, 7, 11, 13, 17, 19, 23, 29, 31] * 3
    results = []

    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")

    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    std_metric_value = math.sqrt(sum((result["metric_value"] - mean_metric_value)**2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)

    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=unknown")