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

def is_prime(n):
    if n <= 1:
        return False
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True

def generate_primes(min_val, max_val):
    primes = []
    for num in range(min_val, max_val + 1):
        if is_prime(num):
            primes.append(num)
    return primes

def generate_bibd(v, k, lambd):
    blocks = set()
    while len(blocks) < v:
        block = set(random.sample(range(v), k))
        if all(block & b == set() for b in blocks):
            blocks.add(frozenset(block))
    blocks = [list(b) for b in blocks]
    incidence_matrix = [[1 if i in block else 0 for block in blocks] for i in range(v)]
    return incidence_matrix, len(blocks)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_tests = 30
    total_metric_value = 0
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""

    for _ in range(n_tests):
        v = random.randint(5, 40)
        k = random.randint(2, v // 2)
        lambd = random.randint(1, min(v - k + 1, 3))
        incidence_matrix, num_blocks = generate_bibd(v, k, lambd)

        if num_blocks != (v * (k - 1)) // (lambd * (k - 1)):
            counterexample = "Parameters do not form a valid BIBD"
            conjecture_holds = False
            break

        # Estimate ACC^0 circuit size using known lower bounds
        expected_circuit_size = v ** (2 - 1 / k)
        actual_circuit_size = num_blocks * k

        if actual_circuit_size < expected_circuit_size:
            counterexample = f"Expected at least {expected_circuit_size}, got {actual_circuit_size}"
            conjecture_holds = False
            break

        total_metric_value += actual_circuit_size
        instances_tested += 1

    return {
        "metric_name": "ACC^0 Circuit Size",
        "metric_value": total_metric_value / instances_tested if instances_tested > 0 else None,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else generate_primes(2, 30)
    results = []

    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_metric_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)

    if all(r["counterexample"] == "" for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(r["counterexample"] != "" for r in results):
        first_failing_seed = next((r["seed"] for r in results if r["counterexample"] != ""), None)
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")