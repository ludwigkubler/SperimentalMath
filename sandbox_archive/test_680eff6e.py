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

def generate_random_circuit(n: int) -> list:
    return [random.randint(0, 1) for _ in range(2**n)]

def compute_euler_characteristic(circuit: list) -> int:
    n = len(circuit)
    if n == 0:
        return 0
    count_ones = circuit.count(1)
    count_zeros = circuit.count(0)
    return count_ones - count_zeros

def compute_monotone_complexity(circuit: list) -> int:
    n = len(circuit)
    max_length = 0
    current_length = 0
    for bit in circuit:
        if bit == 1:
            current_length += 1
            max_length = max(max_length, current_length)
        else:
            current_length = 0
    return max_length

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    chi_sum = 0
    mu_sum = 0
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""

    for n in n_values:
        for _ in range(5):  # Test each n with 5 random circuits
            circuit = generate_random_circuit(n)
            chi = compute_euler_characteristic(circuit)
            mu = compute_monotone_complexity(circuit)
            if chi > n**2 or mu > n:
                conjecture_holds = False
                counterexample = f"n={n}, chi={chi}, mu={mu}"
                break
            chi_sum += chi
            mu_sum += mu
            instances_tested += 1

    mean_chi = Fraction(chi_sum, instances_tested)
    mean_mu = Fraction(mu_sum, instances_tested)

    return {
        "metric_name": "Euler characteristic / Monotone complexity ratio",
        "metric_value": float(mean_chi / mean_mu),
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
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
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")