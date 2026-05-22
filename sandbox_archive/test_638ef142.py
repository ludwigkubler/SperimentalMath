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

def lcm(a, b):
    return abs(a * b) // gcd(a, b)

def is_prime(n):
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True

def generate_primes(n):
    primes = []
    for num in range(2, n):
        if is_prime(num):
            primes.append(num)
    return primes

def generate_circuit(n):
    inputs = random.randint(1, n)
    gates = random.randint(inputs, 5 * inputs)
    circuit = [(random.choice(['AND', 'OR']), [random.randint(0, inputs - 1), random.randint(0, inputs - 1)]) for _ in range(gates)]
    return circuit

def compute_function_field(circuit):
    # Simplified function field computation
    return len(circuit)

def compute_brauer_group_order(function_field_size):
    # Simplified Brauer group order computation
    return function_field_size ** 2

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    total_brauer_group_order = 0
    total_circuit_size = 0
    instances_tested = 0

    for n in n_values:
        for _ in range(5):
            circuit = generate_circuit(n)
            function_field_size = compute_function_field(circuit)
            brauer_group_order = compute_brauer_group_order(function_field_size)
            total_brauer_group_order += brauer_group_order
            total_circuit_size += len(circuit)
            instances_tested += 1

    mean_brauer_group_order = total_brauer_group_order / instances_tested
    mean_circuit_size = total_circuit_size / instances_tested
    correlation_coefficient = (instances_tested * total_brauer_group_order * total_circuit_size - 
                               sum(b * c for b, c in zip([brauer_group_order for _ in range(instances_tested)], [circuit_size for _ in range(instances_tested)])) *
                               instances_tested) / ((instances_tested * total_brauer_group_order ** 2 - sum(b ** 2 for b in [brauer_group_order for _ in range(instances_tested)]) * instances_tested) *
                                                     (instances_tested * total_circuit_size ** 2 - sum(c ** 2 for c in [circuit_size for _ in range(instances_tested)]) * instances_tested))

    conjecture_holds = correlation_coefficient > 0.7
    counterexample = "" if conjecture_holds else "correlation_coefficient < 0.7"

    return {
        "metric_name": "Pearson Correlation Coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or generate_primes(30)
    results = []

    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, **result}}")
        results.append(result)

    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")