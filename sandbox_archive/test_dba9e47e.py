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

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def p_adic_valuation(n, p):
    if n == 0:
        return float('inf')
    count = 0
    while n % p == 0:
        n //= p
        count += 1
    return count

def min_p_adic_valuation(roots):
    return min(p_adic_valuation(root, 2) for root in roots if root != 0)

def generate_polynomial(d, coeff_range):
    coeffs = [random.randint(coeff_range[0], coeff_range[1]) for _ in range(d + 1)]
    return coeffs

def evaluate_polynomial(poly, x):
    result = 0
    power_of_x = 1
    for coeff in poly:
        result += coeff * power_of_x
        power_of_x *= x
    return result

def construct_ac0_circuit(poly, max_gates):
    n = len(poly) - 1
    if n > max_gates:
        return None
    circuit = []
    for i in range(n):
        circuit.append((poly[i], 'add'))
    return circuit

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_trials = 30
    total_metric_value = 0
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""

    for _ in range(n_trials):
        d = random.randint(1, 40)
        coeff_range = (-10, 10)
        poly = generate_polynomial(d, coeff_range)
        roots = []
        for x in range(-10, 11):
            if evaluate_polynomial(poly, x) == 0:
                roots.append(x)

        val_p = min_p_adic_valuation(roots)
        circuit = construct_ac0_circuit(poly, d)
        if circuit is None:
            conjecture_holds = False
            counterexample = "AC0 circuit size exceeds max_gates"
            break

        mean_circuit_size = sum(len(gate) for gate in circuit) / len(circuit)
        total_metric_value += val_p * mean_circuit_size
        instances_tested += 1

    if conjecture_holds:
        return {
            "metric_name": "min_p_adic_valuation * mean_circuit_size",
            "metric_value": total_metric_value / instances_tested,
            "instances_tested": instances_tested,
            "conjecture_holds": True,
            "counterexample": ""
        }
    else:
        return {
            "metric_name": "min_p_adic_valuation * mean_circuit_size",
            "metric_value": total_metric_value / instances_tested,
            "instances_tested": instances_tested,
            "conjecture_holds": False,
            "counterexample": counterexample
        }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []

    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")

        if not trial_result["conjecture_holds"]:
            break

    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    std_metric_value = math.sqrt(sum((result["metric_value"] - mean_metric_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)

    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in enumerate(results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"AC0 circuit size exceeds max_gates\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=unknown")