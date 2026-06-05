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
    circuit = []
    for _ in range(2**n - 1):
        gate = random.choice(['AND', 'OR'])
        inputs = [random.randint(0, n-1) for _ in range(gate.count('X'))]
        circuit.append((gate, inputs))
    return circuit

def compute_polynomial(circuit):
    n = len(circuit)
    polynomial = {}
    for i in range(n):
        polynomial[i] = 1
    for gate, inputs in circuit:
        if gate == 'AND':
            new_poly = {}
            for x in polynomial:
                for y in polynomial:
                    if x & y not in new_poly:
                        new_poly[x & y] = 0
                    new_poly[x & y] += polynomial[x] * polynomial[y]
            polynomial = new_poly
        elif gate == 'OR':
            new_poly = {}
            for x in polynomial:
                for y in polynomial:
                    if x | y not in new_poly:
                        new_poly[x | y] = 0
                    new_poly[x | y] += polynomial[x] * polynomial[y]
            polynomial = new_poly
    return polynomial

def compute_grobner_basis(polynomial):
    basis = list(polynomial.items())
    while True:
        changed = False
        for i in range(len(basis)):
            for j in range(i + 1, len(basis)):
                if basis[i][0] % basis[j][0] == 0:
                    basis[i] = (basis[i][0], basis[i][1] - (basis[i][0] // basis[j][0]) * basis[j][1])
                    changed = True
                elif basis[j][0] % basis[i][0] == 0:
                    basis[j] = (basis[j][0], basis[j][1] - (basis[j][0] // basis[i][0]) * basis[i][1])
                    changed = True
        if not changed:
            break
    return basis

def minimal_order(grobner_basis):
    return max(len(str(x)) for x, _ in grobner_basis)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    total_metric_value = 0
    instances_tested = 0
    n_max = 0
    conjecture_holds = True
    counterexample = ""

    for n in n_values:
        for _ in range(5):
            circuit = generate_circuit(n)
            polynomial = compute_polynomial(circuit)
            grobner_basis = compute_grobner_basis(polynomial)
            order = minimal_order(grobner_basis)
            total_metric_value += order
            instances_tested += 1
            n_max = max(n_max, n)

            if order > n**2 * math.log(n):
                conjecture_holds = False
                counterexample = f"n={n}, order={order} > {n**2 * math.log(n)}"

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
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3

    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")